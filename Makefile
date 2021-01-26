PKG_VERSION := $(shell poetry version | awk '{print $$2}')

release:
	git tag "$(PKG_VERSION)"
	git push -u origin "$(PKG_VERSION)"
