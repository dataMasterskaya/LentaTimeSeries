import argparse
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import requests
import json
import numpy as np
# from model import predictions
import logging

app = FastAPI()

app_logger = logging.getLogger(__name__)
app_logger.setLevel(logging.INFO)
app_handler = logging.StreamHandler()
app_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
app_handler.setFormatter(app_formatter)
app_logger.addHandler(app_handler)


@app.get("/")
def main():
    """main handler"""
    html_content = """
            <body>
            <form action="/forecast" method="post">
            <input name="write forecast">
            <input type="submit", value="Write Forecast">
            </form>
            </body>
            """
    app_logger.info(f'successfully started')
    return HTMLResponse(content=html_content)


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


@app.get("/predict")
def get_predictions() -> dict:
    """collect data from database and ask to model"""
    cat = requests.get("http://localhost:8000/categories")
    sales = requests.get("http://localhost:8000/sales")
    stores = requests.get("http://localhost:8000/stores")
    if cat.status_code == 200 and sales.status_code == 200 and stores.status_code == 200:
        app_logger.info(f'prediction model running')
        result = 42  # predictions(cat.json(), sales.json(), stores.json())
        status = 'success'
    else:
        app_logger.error(f'some error with handlers')
        result = 'error'
        status = 'fail'
    return {"status": status, "data": result}


@app.post("/forecast")
def save_forecast() -> dict:
    """save forecast results in file"""
    label = np.random.randint(100)
    forecast = {"data": [
        {"store": "sdfds1",
         "forecast_date": "2023-09-01",
         "forecast": {"sku": "sdf",
                      "sales_units": {"2023-09-01": label,
                                      "2023-09-02": 0,
                                      "2023-09-03": 0,
                                      "2023-09-04": 0,
                                      "2023-09-05": 0,
                                      }}}]}
    json.dump(forecast, open('forecast_archive.json', 'w'))
    app_logger.info(f'successfully added')
    status = 'success'
    return {"status": status}


@app.get("/forecast")
def load_forecast() -> dict:
    """save forecast results in file"""
    try:
        f = open('forecast_archive.json', 'r')
        result = json.load(f)
        app_logger.info(f'successfully loaded')
        status = 'success'
    except:
        result = 'no data'
        app_logger.error(f'archive not available')
        status = 'fail'
    return {"status": status, "data": result}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=8000, type=int, dest="port")
    parser.add_argument("--host", default="localhost", type=str, dest="host")
    args = vars(parser.parse_args())
    uvicorn.run(app, **args)
