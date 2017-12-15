test:
	bash tests/functional/run.sh

entr:
	find -name "*.py" -o -name "*.sh" | entr -c make test

.PHONY: test entr
