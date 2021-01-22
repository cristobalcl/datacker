
PKG_VERSION := $(shell poetry version | awk '{print $$2}')

build:
	docker build -t cristobalcl/datacker:latest -t cristobalcl/datacker:$(PKG_VERSION) .

push:
	docker push cristobalcl/datacker:latest
