clean-workspace:
	rm -rf .mypy_cache
	rm -rf tests/.pytest_cache

run-mypy:
	pipenv run mypy vrp.py

run-tests:
	pipenv run pytest