.PHONY: console-install console-run console-test console-lint

console-install:
	python3 -m pip install -e 'apps/streamlit[dev]'

console-run:
	streamlit run apps/streamlit/app.py

console-test:
	pytest tests/unit/streamlit

console-lint:
	ruff check apps/streamlit tests/unit/streamlit
