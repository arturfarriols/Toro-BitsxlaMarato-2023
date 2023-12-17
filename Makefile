SHELL := /bin/bash

# TODO: Use docker image to run FE & BE without SO dependency commands
#.PHONY: all
#all: frontend backend
	

backend-setup:
	@echo *** Running Backend ***
	python -m venv .venv &&	source ./.venv/bin/activate && pip install -r pp.txt

.PHONY: backend
backend: backend-setup
	@source ./.venv/bin/activate && cd src && python -m backend.main


.PHONY: frontend
frontend: 
	@echo *** Running Frontend ***
	@cd src/frontend && npm run dev
