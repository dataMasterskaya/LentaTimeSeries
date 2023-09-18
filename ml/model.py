import json
import logging
import numpy as np


m_logger = logging.getLogger(__name__)
m_logger.setLevel(logging.DEBUG)
handler_m = logging.StreamHandler()
formatter_m = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler_m.setFormatter(formatter_m)
m_logger.addHandler(handler_m)


def predictions(cats: dict, sales: dict, stores: dict) -> json:
    """some ML magic here"""
    luck = np.random.rand(1)[0]
    if luck < .5:
        m_logger.error(f'something went wrong')
        result = ':('
    else:
        m_logger.info(f'success')
        result = {"data": [
        {"store": stores["city"].upper(),
         "sku": len(cats) + len(sales),
         "forecast_date": "2023-09-01",
         "forecast": {"2023-09-01": 111,
                      "2023-09-02": 111,
                      "2023-09-03": 111,
                      "2023-09-04": 111,
                      "2023-09-05": 111}
        }
        ]
        }
    return json.dumps(result)
