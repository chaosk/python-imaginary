
test:
	pytest

isort:
	isort -y

yapf:
	yapf -i -p --recursive .

mypy:
	mypy --html-report=mypy_html src/imaginary

flake8:
	flake8
