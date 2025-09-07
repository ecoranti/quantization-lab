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
