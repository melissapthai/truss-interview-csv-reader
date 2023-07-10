default: setup

.PHONY: setup
setup:
	@echo "Creating virtual environment and installing dependencies..."
	python3 -m venv venv
	./venv/bin/activate
	pip install -r requirements.txt

.PHONY: clean
clean:
	@echo "Cleaning..."
	rm -rf __pycache__
	rm -rf venv