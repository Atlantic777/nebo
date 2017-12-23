test:
	bash tests/functional/run.sh ${FILTER}

unit:
	bash tests/unit/run.sh

entr:
	find -name "*.py" -o -name "*.sh" | entr -c make test FILTER=${FILTER}

release:
	tar --exclude='private' --exclude='.git' -cjf /tmp/latest.tar.bz2 ../nebo && \
	# aws s3 mb 's3://nhardi-mrkirm2-releases'
	aws s3 cp /tmp/latest.tar.bz2 's3://nhardi-mrkirm2-releases/latest.tar.bz2'

.PHONY: test unit entr release
