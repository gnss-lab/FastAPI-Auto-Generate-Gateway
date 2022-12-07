allure:
	pytest -s ./tests --alluredir=allureress || true
	allure serve ./allureress

coverage:
	coverage erase
	coverage run --include=dadata/* -m pytest -ra
	coverage report -m
