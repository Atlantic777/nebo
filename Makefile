test:
	bash tests/functional/run.sh ${FILTER}

entr:
	find -name "*.py" -o -name "*.sh" | entr -c make test FILTER=${FILTER}

.PHONY: test entr
