import argparse
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import json
import numpy as np
import logging
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI()

_logger = logging.getLogger(__name__)


@app.get("/")
def main():
    """main handler"""
    html_content = """
            <h1>Sales forecast system.</h1>
            """
    _logger.info(f'successfully started')
    return HTMLResponse(content=html_content)


@app.get("/categories")
def get_cat() -> dict:
    """returns whole categories data"""
    resp = json.load(open("categories.json"))
    _logger.info(f'categories data loaded')
    resp["status"] = "OK"
    return resp


@app.get("/sales")
def get_sales(store=None, sku=None) -> dict:
    """returns sales data for the store and item_id"""
    data = json.load(open("sales.json"))["data"]
    if store is not None:
        data = [el for el in data if el["store"] == store]
    if sku is not None:
        data = [el for el in data if el["sku"] == sku]
    return {"status": "OK", "data": data}


@app.get("/shops")
def get_stores(city=None, cat=None) -> dict:
    """returns list of stores in the city and list of stores with single type_format"""
    data = json.load(open('stores.json'))
    data["status"] = "OK"
    return data


class Forecast(BaseModel):
    data: List

@app.post("/forecast")
def save_forecast(data: Forecast) -> dict:
    """save forecast results in file"""
    print(data)
    label = np.random.randint(100)
    forecast = {"data": [
        {"store": "sdfds1",
         "forecast_date": "2023-09-01",
         "forecast": {"sku": "sdf",
                      "sales_units": {"2023-09-01": 0,
                                      "2023-09-02": 0,
                                      "2023-09-03": 0,
                                      "2023-09-04": 0,
                                      "2023-09-05": 0,
                                      "2023-09-06": 0,
                                      "2023-09-07": 0,
                                      "2023-09-08": 0,
                                      "2023-09-09": 0,
                                      "2023-09-10": 0,
                                      "2023-09-11": 0,
                                      "2023-09-12": 0,
                                      "2023-09-13": 0,
                                      "2023-09-14": 0
                                      }}}]}
<<<<<<< HEAD
    json.dump(forecast, open('forecast_archive.json', 'a'))
    app_logger.info(f'successfully added')
=======
    json.dump(forecast, open('forecast_archive.json', 'w'))
    _logger.info(f'successfully added')
>>>>>>> 29a5b356633578b740106c532deba9fd004d17ee
    status = 'success'
    return {"status": status}


@app.get("/forecast")
def load_forecast() -> dict:
    """load forecast results from file"""
    try:
        f = open('forecast_archive.json', 'r')
        result = json.load(f)
        _logger.info(f'successfully loaded')
        status = 'success'
    except FileNotFoundError:
        result = 'no data'
        _logger.error(f'archive not available')
        status = 'fail'
    return {"status": status, "data": result}


def setup_logging():
    app_logger = logging.getLogger(__name__)
    app_logger.setLevel(logging.INFO)
    app_handler = logging.StreamHandler()
    app_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    app_handler.setFormatter(app_formatter)
    app_logger.addHandler(app_handler)


if __name__ == "__main__":
    setup_logging()
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=8000, type=int, dest="port")
    parser.add_argument("--host", default="0.0.0.0", type=str, dest="host")
    args = vars(parser.parse_args())
    uvicorn.run(app, **args)
