.PHONY: install clean distclean pypi-publish snap-publish pypi-test install

pypi-publish: install
	python -m pip install twine setuptools wheel
	python setup.py sdist bdist_wheel
	twine upload dist/*

snap-publish: install
	snapcraft
	SNAP = $(shell ls sec-vault_*.snap | xargs)
	snapcraft login
	snapcraft register sec-vault
	snapcraft upload --release=edge $(SNAP)

pypi-test: install
	python setup.py develop
	python setup.py build
	python setup.py install

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
	find . -name "*.pyc" -exec rm -rf {} \;
