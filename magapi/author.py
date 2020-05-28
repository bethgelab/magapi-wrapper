import pandas as pd

from .constants import BASE_URL, AUTHOR_ATTRIBUTES
from .logger import get_logger
from .utils import RequestMixin

logger = get_logger(__name__)


class Author(RequestMixin):
    """
    Author class provides all the methods to download author/s profile for given author name/s.
    When the class instance is called, the sequence of operations are as follows
    1) Prepare expr string and then form API
    2) Download data from Microsoft Academic Knowledge Graph and store in pandas dataframe
    3) Display details
    4) Save the data in the specified format.
    :param args: dict, User provided attribute values.
    """
    def __init__(self, args):
        self.args = vars(args)
        self.data = None
        self.expr = None

    def __call__(self):
        self._download()
        self.show(self.args["entity"], self.data, self.expr)
        if self.args["save"]:
            self.save(self.args['format'], self.args["entity"], self.data)


    def _prepare_api(self):
        plain_attributes = []
        author_names = self.args["AuN"].split(",")
        for author in author_names:
            plain_attributes.append(f"AuN='{author.lower()}'")
        expr = f"Or({plain_attributes[0]})" if len(plain_attributes) == 1 else f"Or(" + ','.join(plain_attributes) + ")"
        api = f"{BASE_URL}={expr}&count={self.args['count']}&attributes={AUTHOR_ATTRIBUTES}&subscription-key={self.args['key']}"
        return api

    def _download(self):
        api = self._prepare_api()
        response = self.send_request(api)
        response_json = response.json()
        if "entities" in response_json and response_json["entities"]:
            entities = response_json["entities"]
        else:
            logger.info("There are no publications to download for the given arguments")
            raise SystemExit()
        df = pd.DataFrame(entities)
        df.drop(columns=['logprob','prob'], inplace=True)
        df.rename(columns={"LKA": "Affiliation", "PC": "Publications", "ECC": "Citations", "DAuN": "Name"},
                            inplace=True)
        df['Affiliation'] = df['Affiliation'].apply(lambda x: x["AfN"] if isinstance(x, dict) else None)
        self.data = df
        self.expr = response_json["expr"]


