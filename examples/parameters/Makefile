build:
	datacker datacker_parameters pie.ipynb -r requirements.txt

run:
	docker run --env NOTEBOOK_NAME=pie \
		--env PARAMETERS='{ "sizes": [40, 10, 20, 30], "explode": [0.1, 0, 0, 0] }' \
		--env PARAM_labels='["Cat", "Cactus", "Cattle", "Camel"]' \
		--mount type=bind,src=$(CURDIR)/output,dst=/output \
		datacker_parameters
