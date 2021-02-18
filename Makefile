.PHONY: all
all: .installed.cfg

py38/bin/pip:
	python3.8 -m venv py38

py38/bin/buildout: py38/bin/pip requirements.txt
	./py38/bin/pip install -r requirements.txt

.installed.cfg: py38/bin/buildout
	./py38/bin/buildout -Nt 10
