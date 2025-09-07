#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


# ----------------------------
# Señal y cuantizadores
# ----------------------------

def x_t(t: np.ndarray, T: float) -> np.ndarray:
    """x(t) = t^2 en [0,T), periódica en T."""
    tt = np.mod(t, T)
    return tt**2


def build_levels(L: int, xmin: float, xmax: float) -> tuple[np.ndarray, float]:
    """
    Niveles uniformes *incluyendo extremos* (mid-tread en los niveles):
      levels = {xmin, xmin+Δ, ..., xmax} con Δ = (xmax-xmin)/(L-1)
    """
    if L < 2:
        raise ValueError("L debe ser >= 2")
    Δ = (xmax - xmin) / (L - 1)
    levels = xmin + Δ * np.arange(L)
    return levels, Δ


def q_round_levels(x: np.ndarray, levels: np.ndarray) -> np.ndarray:
    """Redondea al nivel más cercano (mid-tread sobre niveles dados)."""
    # Para vectorizar: elegir el índice del nivel más cercano para cada x
    idx = np.argmin(np.abs(levels[None, :] - x[..., None]), axis=-1)
    return levels[idx]


def q_trunc_levels(x: np.ndarray, levels: np.ndarray, xmin: float, Δ: float) -> np.ndarray:
    """
    Truncamiento (tipo floor) hacia el nivel inferior (mid-rise por intervalos).
    - Mapea x al índice k = floor((x-xmin)/Δ), satura a [0, L-1], y devuelve levels[k].
    """
    L = len(levels)
    k = np.floor((x - xmin) / Δ).astype(int)
    k = np.clip(k, 0, L - 1)
    return levels[k]


# ----------------------------
# Métricas
# ----------------------------

def snr_db(Px: float, Pe: float) -> float:
    if Pe <= 0:
        return float("inf")
    return 10.0 * np.log10(Px / Pe)


def analyze_case(Ts: float, T: float, levels: np.ndarray, xmin: float, Δ: float):
    """
    Devuelve:
      df: tabla con n, t, x, xhat_round, e_round, xhat_trunc, e_trunc
      stats: dict con Px, Pe_round, Pe_trunc, SNRs
    """
    # una duración de un período: muestras en [0,T)
    N = int(np.round(T / Ts))
    n = np.arange(N)
    t = n * Ts
    x = x_t(t, T)

    xr = q_round_levels(x, levels)
    xt = q_trunc_levels(x, levels, xmin, Δ)
    er = xr - x
    et = xt - x

    Px = float(np.mean(x**2))
    Per = float(np.mean(er**2))
    Pet = float(np.mean(et**2))

    stats = {
        "Ts": Ts,
        "Px": Px,
        "Pe_round": Per,
        "Pe_trunc": Pet,
        "SNR_round_dB": snr_db(Px, Per),
        "SNR_trunc_dB": snr_db(Px, Pet),
    }

    df = pd.DataFrame({
        "n": n,
        "t [s]": t,
        "x[n] = t^2": x,
        "x̂_R[n] (round)": xr,
        "e_R[n]": er,
        "x̂_T[n] (trunc)": xt,
        "e_T[n]": et,
    })

    return df, stats


# ----------------------------
# Figuras
# ----------------------------

def fig_curve_round(levels: np.ndarray, xmin: float, xmax: float):
    x_axis = np.linspace(xmin, xmax, 600)
    y = q_round_levels(x_axis, levels)
    fig = plt.figure(figsize=(6, 4))
    plt.step(x_axis, y, where="mid")
    plt.title("Curva E/S - Cuantizador por redondeo")
    plt.xlabel("Entrada x")
    plt.ylabel("Salida Q_round(x)")
    plt.grid(True)
    plt.tight_layout()
    return fig


def fig_curve_trunc(levels: np.ndarray, xmin: float, xmax: float, Δ: float):
    x_axis = np.linspace(xmin, xmax, 600)
    y = q_trunc_levels(x_axis, levels, xmin, Δ)
    fig = plt.figure(figsize=(6, 4))
    plt.step(x_axis, y, where="post")
    plt.title("Curva E/S - Cuantizador por truncamiento")
    plt.xlabel("Entrada x")
    plt.ylabel("Salida Q_trunc(x)")
    plt.grid(True)
    plt.tight_layout()
    return fig


def fig_signals(df: pd.DataFrame, Ts: float, variant: str):
    t = df["t [s]"].values
    x = df["x[n] = t^2"].values
    if variant == "round":
        xq = df["x̂_R[n] (round)"].values
        title = f"Muestreo y cuantización (round) - Ts={Ts}s"
    else:
        xq = df["x̂_T[n] (trunc)"].values
        title = f"Muestreo y cuantización (trunc) - Ts={Ts}s"

    fig = plt.figure(figsize=(7, 4))
    markerline1, stemlines1, baseline1 = plt.stem(t, x, basefmt=" ")
    markerline2, stemlines2, baseline2 = plt.stem(t, xq, basefmt=" ")
    plt.setp(markerline1, markersize=6)
    plt.setp(markerline2, markersize=6)
    plt.title(title)
    plt.xlabel("t [s]")
    plt.ylabel("Amplitud")
    plt.grid(True)
    plt.tight_layout()
    return fig


# ----------------------------
# CLI
# ----------------------------

def parse_args():
    p = argparse.ArgumentParser(
        description="Quantization Lab: x(t)=t^2, cuantización por redondeo vs truncamiento")
    p.add_argument("--Ts", type=float, nargs="+", default=[0.5, 0.1],
                   help="Lista de Ts en segundos (p.ej. --Ts 0.5 0.1)")
    p.add_argument("--L", type=int, default=4, help="Número de niveles (incluyendo extremos)")
    p.add_argument("--xmin", type=float, default=0.0, help="Amplitud mínima")
    p.add_argument("--xmax", type=float, default=4.0, help="Amplitud máxima")
    p.add_argument("--period", type=float, default=2.0, help="Período T de la señal")
    p.add_argument("--outdir", type=str, default="outputs", help="Directorio de salida")
    p.add_argument("--no-show", action="store_true", help="No abrir ventanas de gráficos")
    p.add_argument("--interactive", action="store_true", help="Modo interactivo por consola")
    return p.parse_args()


def interactive_overrides(args):
    print("\n=== Modo interactivo ===")
    try:
        Ts_str = input(f"Ts (separar por espacios) [{ ' '.join(map(str, args.Ts)) }]: ").strip()
        if Ts_str:
            args.Ts = [float(x) for x in Ts_str.split()]
        L_str = input(f"L (niveles) [{args.L}]: ").strip()
        if L_str:
            args.L = int(L_str)
        xmin_str = input(f"Xmin [{args.xmin}]: ").strip()
        if xmin_str:
            args.xmin = float(xmin_str)
        xmax_str = input(f"Xmax [{args.xmax}]: ").strip()
        if xmax_str:
            args.xmax = float(xmax_str)
        T_str = input(f"T (período) [{args.period}]: ").strip()
        if T_str:
            args.period = float(T_str)
        out_str = input(f"Directorio de salida [{args.outdir}]: ").strip()
        if out_str:
            args.outdir = out_str
    except Exception as e:
        print(f"Aviso: entrada inválida, usando valores por defecto. Detalle: {e}")
    return args


def main():
    args = parse_args()
    if args.interactive:
        args = interactive_overrides(args)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # Construir niveles
    levels, Δ = build_levels(args.L, args.xmin, args.xmax)

    # Guardar niveles y Δ
    with open(outdir / "levels.txt", "w", encoding="utf-8") as f:
        f.write(f"Levels (L={args.L}): {levels.tolist()}\n")
        f.write(f"Δ = {Δ}\n")

    # Curvas E/S
    figs = []
    figs.append(fig_curve_round(levels, args.xmin, args.xmax))
    figs[-1].savefig(outdir / "curve_round.png", dpi=160)
    figs.append(fig_curve_trunc(levels, args.xmin, args.xmax, Δ))
    figs[-1].savefig(outdir / "curve_trunc.png", dpi=160)

    # Análisis por Ts
    all_stats = []
    for Ts in args.Ts:
        df, stats = analyze_case(Ts, args.period, levels, args.xmin, Δ)
        # CSV
        csv_path = outdir / f"table_Ts_{Ts}.csv"
        df.to_csv(csv_path, index=False)
        # Figuras de señales
        fr = fig_signals(df, Ts, "round")
        fr.savefig(outdir / f"signals_round_Ts_{Ts}.png", dpi=160)
        figs.append(fr)
        ft = fig_signals(df, Ts, "trunc")
        ft.savefig(outdir / f"signals_trunc_Ts_{Ts}.png", dpi=160)
        figs.append(ft)
        # Resumen por consola
        print(f"\n=== Ts = {Ts} s ===")
        print(df.round(4).to_string(index=False))
        print(
            f"SNR_round = {stats['SNR_round_dB']:.3f} dB | "
            f"SNR_trunc = {stats['SNR_trunc_dB']:.3f} dB "
            f"(Px={stats['Px']:.6f}, PeR={stats['Pe_round']:.6f}, PeT={stats['Pe_trunc']:.6f})"
        )
        all_stats.append(stats)

    # Guardar reporte PDF con todas las figuras
    pdf_path = outdir / "report.pdf"
    with PdfPages(pdf_path) as pdf:
        for fig in figs:
            pdf.savefig(fig)
    print(f"\nArchivos generados en: {outdir.resolve()}")
    print(f"- Curvas E/S: curve_round.png, curve_trunc.png")
    print(f"- Tablas CSV: table_Ts_*.csv")
    print(f"- Señales: signals_*_Ts_*.png")
    print(f"- Reporte PDF: {pdf_path.name}")

    if not args.no_show:
        plt.show()


if __name__ == "__main__":
    main()
