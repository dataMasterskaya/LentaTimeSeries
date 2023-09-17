from fastapi import FastAPI
import uvicorn
import requests
import json
from model import predictions
import logging

app = FastAPI()

app_logger = logging.getLogger(__name__)
app_logger.setLevel(logging.INFO)
app_handler = logging.StreamHandler()
app_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
app_handler.setFormatter(app_formatter)
app_logger.addHandler(app_handler)


@app.get("/")
def main() -> dict:
    """main handler"""
    app_logger.info(f'successfully started')
    return {"status": "OK", "message": "it's alive"}


@app.get("/categories")
def get_cat() -> dict:
    """returns whole categories data"""
    resp = json.load(open("categories.json"))
    app_logger.info(f'categories data loaded')
    return {"status": "OK", "data": resp}


@app.get("/sales")
def get_sales(tc_id="vykhino", item_id="fresh_eggs") -> dict:
    """returns sales data for the store and item_id"""
    data = json.load(open("sales.json"))
    resp = []
    for d in data["data"]:
        if d["store"] == tc_id and d["sku"] == item_id:
            resp.append(d["fact"])
    if len(resp) == 0:
        resp = 'no match'
    app_logger.info(f'{len(resp)} matches found')

    return {"status": "OK", "trade_centre": tc_id, "item": item_id, "data": resp}


@app.get("/stores")
def get_stores(city='moscow', cat=3) -> dict:
    """returns list of stores in the city and list of stores with single type_format"""
    data = json.load(open('stores.json'))
    city_l = []
    type_l = []
    for d in data["data"]:
        if d["city"] == city:
            city_l.append(d)
        if d["type_format"] == cat:
            type_l.append(d)
    if len(city_l) == 0:
        city_l = 'no match'
    if len(type_l) == 0:
        type_l = 'no match'
    app_logger.info(f'load stores for {city} of {cat} category')
    return {"status": "OK", "city": city, "city_query": city_l, "type": cat, "type_query": type_l}


@app.get("/forecast")
def get_predictions() -> dict:
    """collect data from database and ask to model"""
    cat = requests.get("http://localhost:8000/categories")
    sales = requests.get("http://localhost:8000/sales")
    stores = requests.get("http://localhost:8000/stores")
    if cat.status_code == 200 and sales.status_code == 200 and stores.status_code == 200:
        app_logger.info(f'prediction model running')
        result = predictions(cat.json(), sales.json(), stores.json())
        status = 'success'
    else:
        app_logger.error(f'some error with handlers')
        result = 'error'
        status = 'fail'
    return {"status": status, "data": result}


# а вот тут я запутался в методах post и get
@app.get("/save")
def save_forecast() -> dict:
    """save forecast results in file"""
    forecast = requests.get("http://localhost:8000/forecast")
    if forecast.status_code == 200:
        result = forecast.json()
        json.dump(result, open('forecast_archive.json', 'a'))
        app_logger.info(f'successfully added')
        status = 'success'
    else:
        app_logger.error(f'model is not available')
        status = 'fail'
    return {"status": status}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
