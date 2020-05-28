import requests
from pathlib import Path
import pandas as pd
from tabulate import tabulate
from .exceptions import MAGPaperSaveException, MAGRequestsException
from .logger import get_logger

logger = get_logger(__name__)

class RequestMixin(object):
    def send_request(self, api):
        try:
            response = requests.get(api)
            if response.ok:
                return response
            else:
                raise MAGRequestsException(response.text)
        except requests.exceptions.Timeout:
            logger.exception("Timeout happened while calling the api")
        except requests.exceptions.TooManyRedirects:
            logger.exception("URL is bad")
        except requests.exceptions.RequestException as e:
            logger.exception("Unexpected error happened")
            raise SystemExit(e)

    def save(self, format, entity, data):
        path = f'{Path.home()}/Downloads/{entity}.{format}'
        if format == 'csv':
            data.to_csv(path)
        elif format == 'json':
            data.to_json(path, orient='records')
        else:
            raise MAGPaperSaveException(f"{format} is not supported")
        logger.info(f'Downloading papers into path {path}')

    def show(self, entity, data, expr):
        """
        Write download details of the data downloaded before actually downloading the data.
        :return:
        """
        if data is None:
            logger.info("Download is unsuccessful, please check your arguments")
        elif not data.empty:
            logger.info(f'Executed Microsoft Academic API is {expr}')
            logger.info(f'Number of {entity}s downloaded are {len(data)}')
            print(tabulate(data, headers='keys', tablefmt='psql'))