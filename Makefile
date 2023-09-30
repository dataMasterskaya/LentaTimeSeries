build_gateway:
	docker build --tag ts_api -f backend_Dockerfile .

run_gateway:
	docker run --rm -it -p 8010:8000 --name lenta_api ts_api

build_ml:
	docker build --tag ts_ml -f ml_Dockerfile .

run_ml:
	docker run --rm -it --name lenta_ml ts_m