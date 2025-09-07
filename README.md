# Quantization Lab (Python)

Ejercicios de muestreo y cuantización (round vs trunc) con:
- Señal periódica: x(t) = t^2 en [0,2), T=2
- L niveles uniformes entre Xmin y Xmax
- Dos cuantizadores:
  - `round`: al nivel más cercano (mid-tread sobre niveles dados)
  - `trunc`: al nivel inferior (tipo floor; mid-rise en intervalos)
- Curvas E/S, tablas de muestras y errores, y SNR promedio por período

## Requisitos
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
