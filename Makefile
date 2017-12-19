test:
	bash tests/functional/run.sh ${FILTER}

unit:
	bash tests/unit/run.sh

entr:
	find -name "*.py" -o -name "*.sh" | entr -c make test FILTER=${FILTER}

.PHONY: test entr
