# -*- coding: utf-8-unix -*-

check:
	flake8 .

clean:
	rm -rf dist
	rm -rf __pycache__

install:
	pip install --break-system-packages .

.PHONY: check clean install
