run: venv
	$(VENV)/fastapi run main.py

dev: venv
	$(VENV)/fastapi dev main.py

install: venv
	$(VENV)/pip install -r requirements.txt

include Makefile.venv
