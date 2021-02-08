# Meta
NAME := testapi


# Install dependencies
.PHONY: deps
deps:
	pip install -r requirements.txt
	pip install -e .


# Run all unit tests
.PHONY: test
test:
	pytest tests/* -s
