.PHONY: install clean distclean TAGS info

install:
	pip3 install -r sec_vault/requirements/test.txt

test:
	export PYTHONDONTWRITEBYTECODE=1
	pytest

distclean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.snap
	rm sec_vault/sec_vault.egg-info

clean:
	python setup.py clean --all
	find . -name "*.pyc" -exec rm -rf {} \;
