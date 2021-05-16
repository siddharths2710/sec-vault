.PHONY: install clean distclean install publish-package publish-snap make-snap make-package test lint

publish-package: make-package
	python -m pip install twine setuptools wheel
	python setup.py sdist bdist_wheel
	twine upload dist/*

publish-snap: make-snap
	SNAP = $(shell ls sec-vault_*.snap | xargs)
	snapcraft register sec-vault
	snapcraft upload --release=edge $(SNAP)

make-package: install
	python setup.py develop
	python setup.py build
	python setup.py install

make-snap: install
	snapcraft

install:
	python -m pip install --upgrade pip
	python -m pip install -r sec_vault/requirements.txt
	apt install snapcraft

test:
	export PYTHONDONTWRITEBYTECODE=1 && pytest

lint:
	pylint

distclean:
	rm -rf *.snap
	rm -rf dist/
	rm -rf build/
	rm -rf sec_vault/sec_vault.egg-info/
	rm -rf .eggs/

clean:
	python setup.py clean --all
	find . -name "*.pyc" -o -name ".pytest_cache" -exec rm -rf {} \;
