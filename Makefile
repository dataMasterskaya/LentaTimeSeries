build:
	docker build --tag timeseries .

run:
	docker run --rm -it -p 8010:8000 --name lenta timeseries