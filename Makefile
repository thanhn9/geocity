
install:
	pip install -r requirements.txt

uninstall:
	yes | pip uninstall -r requirements.txt

test:
	python tests/apitest.py

run:
	python api/restapi.py

start: | install test run
