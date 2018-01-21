test:
	bash tests/functional/run.sh ${FILTER}

entr:
	find -name "*.py" -o -name "*.sh" | entr -c make test FILTER=${FILTER}

release:
	tar --exclude='private' --exclude='.git' --exclude="__pycache__" -cjf /tmp/latest.tar.bz2 ../nebo && \
	aws s3 cp /tmp/latest.tar.bz2 's3://nhardi-mrkirm2-releases/latest.tar.bz2'

docs:
	pdflatex --output-directory=docs docs/report.tex 

.PHONY: test entr release docs
