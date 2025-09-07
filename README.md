# Quantization Lab (Python) / Laboratorio de Cuantización

**EN** – Educational project in Python implementing a hands-on **sampling & uniform quantization** lab:
- Periodic signal \(x(t)=t^2\) on \([0, T)\)
- Uniform quantization with levels in \([X_{\min}, X_{\max}]\)
- Two quantizers:
  - **Round-to-nearest** (mid-tread on levels)
  - **Truncation to lower level** (mid-rise by intervals)
- Error tables, **SNR**, **I/O curves**, and **PDF** report with all plots
- CLI interactive mode to experiment with parameters

**ES** – Proyecto educativo en Python que implementa un **laboratorio de muestreo y cuantización uniforme**:
- Señal periódica \(x(t)=t^2\) en \([0, T)\)
- Cuantización uniforme con niveles en \([X_{\min}, X_{\max}]\)
- Dos cuantizadores:
  - **Redondeo al nivel más cercano** (mid-tread sobre niveles)
  - **Truncamiento al nivel inferior** (mid-rise por intervalos)
- Tablas de error, **SNR**, **curvas E/S**, y **PDF** con todas las figuras
- Modo interactivo por CLI para probar parámetros

---

## Installation / Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

> If your `quantization_demo.py` shows a `SyntaxError` on line 1, ensure it **does not** start with `---`.  
> Si `quantization_demo.py` muestra `SyntaxError` en la línea 1, asegurate de que **no** empiece con `---`.

---

## Usage / Uso

### Quick run / Ejecución rápida
```bash
python quantization_demo.py --Ts 0.5 0.1 --L 4 --xmin 0 --xmax 4 --period 2 --outdir outputs --no-show
```

### Interactive mode / Modo interactivo
```bash
python quantization_demo.py --interactive
```

Generated files live in `outputs/`:
- CSV tables per `Ts`
- I/O curves (`curve_round.png`, `curve_trunc.png`)
- Sampled + quantized signals (`signals_*`)
- `report.pdf` (all figures)

---
