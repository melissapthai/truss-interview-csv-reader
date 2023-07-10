default: setup

.PHONY: setup
setup:
	@echo "Creating virtual environment and installing dependencies..."
	python3 -m venv venv && \
	source venv/bin/activate && \
	pip install -r requirements.txt

.PHONY: reset
reset:
	@echo "Resetting environment..."
	rm -rf __pycache__
	rm -rf venv