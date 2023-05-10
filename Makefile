allure:
	pytest -s ./tests --alluredir=allureress || true
	allure serve ./allureress

coverage:
	coverage erase
	coverage run --source=./fastapi_gateway_auto_generate -m pytest -s
	coverage html
