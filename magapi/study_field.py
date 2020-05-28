import pandas as pd

from .constants import BASE_URL, STUDY_FIELD_ATTRIBUTES
from .logger import get_logger
from .utils import RequestMixin

logger = get_logger(__name__)


class StudyField(RequestMixin):
    """
    StudyField class provides all the methods to download the study field and its statistics for given study field name/s.
    When the class instance is called, the sequence of operations are as follows
    1) Prepare expr string and then form API
    2) Download data from Microsoft Academic Knowledge Graph and store in pandas dataframe
    3) Display details
    4) Save the data in the specified format if the save option is enabled..
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
        fields = self.args["FN"].split(",")
        for field in fields:
            plain_attributes.append(f"FN='{field.lower()}'")
        expr = f"Or({plain_attributes[0]})" if len(plain_attributes) == 1 else f"Or(" + ','.join(plain_attributes) + ")"
        api = f"{BASE_URL}={expr}&count={self.args['count']}&attributes={STUDY_FIELD_ATTRIBUTES}&subscription-key={self.args['key']}"
        return api

    def process_json(self, row):
        if isinstance(row, float):
            return None
        else:
           return "\n".join([field["FN"] for field in row])


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
        "Id,PC,FP.FN,ECC,DFN,FC.FN"
        df.rename(columns={"FP": "Parent Field", "FC": "Child Field", "PC": "Publications", "ECC": "Citations", "DFN": "Field Name"},
                            inplace=True)
        df['Parent Field'] = df['Parent Field'].apply(self.process_json)
        df['Child Field'] = df['Child Field'].apply(self.process_json)
        self.data = df
        self.expr = response_json["expr"]


