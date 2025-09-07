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

## Makefile (optional) / (opcional)

If you prefer shortcuts:  
Si preferís atajos:

```bash
make venv
make run
make run-interactive
make clean
```

---

## GitHub Actions (CI)

The workflow will:
1) Set up Python  
2) Install dependencies  
3) Run the demo  
4) Upload `outputs/` as build artifacts

Open **Actions** tab in GitHub to download them per run.

---

## License

MIT (optional). Feel free to add a license of your choice.

---

# 2) `Makefile`

> Guárdalo en la raíz del repo: `Makefile`

```make
# Makefile for quantization-lab

PYTHON := python
PIP := pip
VENV := .venv
ACT := source $(VENV)/bin/activate
OUT := outputs

.PHONY: venv run run-interactive pdf clean clean-outputs freeze

venv:
    @test -d $(VENV) || python3 -m venv $(VENV)
    @$(ACT) && $(PIP) install -U pip && $(PIP) install -r requirements.txt
    @echo "✅ venv ready"

run:
    @mkdir -p $(OUT)
    @$(ACT) && $(PYTHON) quantization_demo.py --Ts 0.5 0.1 --L 4 --xmin 0 --xmax 4 --period 2 --outdir $(OUT) --no-show
    @echo "✅ run finished; see '$(OUT)/'"

run-interactive:
    @mkdir -p $(OUT)
    @$(ACT) && $(PYTHON) quantization_demo.py --interactive
    @echo "✅ interactive finished; see '$(OUT)/'"

pdf:
    @mkdir -p $(OUT)
    @$(ACT) && $(PYTHON) quantization_demo.py --Ts 0.5 0.1 --L 4 --xmin 0 --xmax 4 --period 2 --outdir $(OUT) --no-show
    @echo "✅ PDF ready at '$(OUT)/report.pdf'"

freeze:
    @$(ACT) && $(PIP) freeze > requirements.lock.txt
    @echo "✅ requirements.lock.txt generated"

clean-outputs:
    @rm -rf $(OUT)
    @echo "🧹 outputs/ cleaned"

clean: clean-outputs
    @find . -name "__pycache__" -type d -exec rm -rf {} +
    @find . -name "*.pyc" -delete
    @echo "🧹 project cleaned"
    
# 3) GitHub Actions – CI
Crea las carpetas y archivo: `.github/workflows/ci.yml`

```yaml
name: Quantization Lab CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]
  workflow_dispatch:

jobs:
  build-and-run:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install -U pip
          pip install -r requirements.txt

      - name: Run quantization demo (non-interactive)
        run: |
          python quantization_demo.py --Ts 0.5 0.1 --L 4 --xmin 0 --xmax 4 --period 2 --outdir outputs --no-show

      - name: Upload outputs as artifact
        uses: actions/upload-artifact@v4
        with:
          name: quantization-outputs
          path: outputs/
          
          
# Crear carpetas del workflow si no existen
mkdir -p .github/workflows

# (Pega/guarda los 3 archivos anteriores)

git add README.md Makefile .github/workflows/ci.yml
git commit -m "docs: bilingual README; chore: Makefile; ci: GitHub Actions to run demo & upload artifacts"
git push
