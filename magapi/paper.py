import pandas as pd
from .constants import BASE_URL, PAPER_ATTRIBUTES
from .exceptions import MAGArgumentsException
from .logger import get_logger
from .utils import RequestMixin

logger = get_logger(__name__)


class Paper(RequestMixin):
    """
    Paper class provides all the methods to download the data using the user
    given attributes. When the class instance is called, the sequence of operations are as follows
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


    def _process_list_attrs(self, arg, values):
        values = values.split(',')
        exprs = []
        if arg == 'Y':
            values = [int(val) for val in values]
            exprs.append(f'{arg}={values}')
        else:
            for val in values:
                if val.isdigit():
                    exprs.append(f'{arg}={int(val)}')
                else:
                    exprs.append(f"{arg}='{val.lower()}'")
        return f'Or({",".join(exprs)})'

    def _process_single_attrs(self, arg, val):
        print(arg, val)
        if val.isdigit():
            return f'{arg}={int(val)}'
        else:
            return f"{arg}='{val.lower()}'"

    def _get_paper_ids(self):
        titles = self.args["Ti"].split(",")
        expr_list = []
        for title in titles:
            expr_list.append(f"Ti=='{title.lower()}'")
        expr = f"Or({expr_list[0]})" if len(expr_list) == 1 else "Or(" + ",".join(expr_list) + ")"
        api = f"{BASE_URL}={expr}&count={self.args['count']}&attributes=Id&subscription-key={self.args['key']}"
        response = self.send_request(api)
        response_json = response.json()
        paper_ids = [paper_id["Id"] for paper_id in response_json["entities"] if "entities" in response_json and len(response_json["entities"]) > 0]
        return paper_ids

    def _process_args(self):
        composite_attributes = []
        plain_attributes = []
        if self.args["citations"]:
            if not 'Ti' in self.args: raise MAGArgumentsException("When the argument Citations is true, One or more titles must be given using option --Ti")
            paper_ids = self._get_paper_ids()
            for paper_id in paper_ids:
                plain_attributes.append(f"RId={paper_id}")
            return plain_attributes, composite_attributes
        for arg, val in self.args.items():
            if arg in ['key', 'count', 'entity', 'format', 'save', 'citations']:
                continue
            elif '.' in arg:
                if isinstance(val, str) and ',' in val:
                    expr = f"Composite({self._process_list_attrs(arg, val)})"
                    composite_attributes.append(expr)
                else:
                    expr = f"Composite({self._process_single_attrs(arg, val)})"
                    composite_attributes.append(expr)
            else:
                if isinstance(val, str) and ',' in val:
                    plain_attributes.append(self._process_list_attrs(arg, val))
                elif isinstance(val, str) and \
                        ('>' in val or '<' in val or '>=' in val or '<=' in val):
                    plain_attributes.append(f'{arg}{val}')
                else:
                    plain_attributes.append(self._process_single_attrs(arg, val))
        return plain_attributes, composite_attributes

    def _prepare_api(self):
        plain_attributes, composite_attributes = self._process_args()
        comp_expr = ''
        plain_expr = ''
        if len(composite_attributes) == 1:
            comp_expr = composite_attributes[0]
        elif len(composite_attributes) > 1:
            comp_expr = 'And(' + ','.join(composite_attributes) + ')'

        if len(plain_attributes) == 1:
            plain_expr = plain_attributes[0]
        elif len(plain_attributes) > 1:
            plain_expr = ','.join(plain_attributes)

        if plain_expr and comp_expr:
            expr = f'And({plain_expr},{comp_expr})'
        elif plain_expr:
            expr = f'And({plain_expr})'
        else:
            expr = f'And({comp_expr})'

        api = f"{BASE_URL}={expr}&count={self.args['count']}&attributes={PAPER_ATTRIBUTES}&subscription-key={self.args['key']}"
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
        df.rename(columns={"Y": "Year", "D": "Date", "ECC": "Citations",
                           "DN": "Title", "PB": "Publisher", "J": "Journal name", "AA": "Authors"},
                            inplace=True)
        df['Authors'] = df['Authors'].apply(lambda x: ','.join(author["DAuN"] for author in x))
        df['Journal name'] = df['Journal name'].apply(lambda x: x["JN"] if isinstance(x, dict) else None)

        self.data = df
        self.expr = response_json["expr"]


