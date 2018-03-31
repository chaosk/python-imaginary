
yapf:
	yapf -i -p --recursive .

mypy:
	mypy --html-report=mypy_html src/imaginary

isort:
	isort -y
