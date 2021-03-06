DOC_DIR = ./docs
package = scraper
RM = rm -rf


# A shell pipeline that'll correctly get the next patch version
next_version = $(shell \
	python3 -c 'import '$(package)'; print('$(package)'.__version__)' | \
	cut -d "+" -f 1 | \
	awk -F "." '{patch = $$3 + 1; print($$1 "." $$2 "." patch) }' )


test:
	py.test -m 'not plumbing'

# Alias for test
tests: test

full_tests:
	py.test

tag:
	@git diff-index --quiet HEAD -- || (printf 'Please commit your changes first.\n\n'; exit 1)
	@echo New version: $(next_version)
	git tag -a "$(next_version)" -m "version $(next_version)"
	git push 
	git push --tags

clean:
	$(RM) $(DOC_DIR)/_build/html
	$(RM) coverage_report
	$(RM) *.egg-info
	$(RM) build
	$(RM) dist
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

coverage:
	coverage run -m pytest
	coverage html
	coverage report
	firefox coverage_report/index.html
	$(RM) .coverage

build_docs: clean
	sphinx-apidoc -o docs -T $(package)
	$(MAKE) --directory=$(DOC_DIR) html

docs: build_docs
	firefox $(DOC_DIR)/_build/html/index.html &

api-docs:
	sphinx-apidoc -o $(DOC_DIR) mini_wiki 

bdist: build_docs
	python3 setup.py bdist

sdist: build_docs
	python3 setup.py sdist

.PHONY: docs clean coverage test tag sdist bdist
