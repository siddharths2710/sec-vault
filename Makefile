.PHONY: install clean distclean pypi-publish snap-publish pypi-test install

pypi-publish: install
	pip3 install twine setuptools wheel
	python3 setup.py sdist bdist_wheel
	twine upload dist/*

snap-publish: install
	snapcraft
	SNAP = $(shell ls sec-vault_*.snap | xargs)
	snapcraft login
	snapcraft register sec-vault
	snapcraft upload --release=edge $(SNAP)

pypi-test: install
	python3 setup.py develop
	python3 setup.py build
	python3 setup.py install

install:
	pip3 install -r sec_vault/requirements/test.txt
	apt install snapcraft

test:
	export PYTHONDONTWRITEBYTECODE=1 && pytest

distclean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.snap
	rm sec_vault/sec_vault.egg-info

clean:
	python setup.py clean --all
	find . -name "*.pyc" -exec rm -rf {} \;
