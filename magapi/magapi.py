import argparse

from author import Author
from constants import PAPER, AUTHOR, AFFILIATION, STUDY_FIELD
from paper import Paper
from study_field import StudyField


def parse_args():
    parser = argparse.ArgumentParser(prog='mag_api',
                                     description='Download publications',
                                     argument_default=argparse.SUPPRESS)
    parser.add_argument(
        'key',
        type=str,
        help="Key from Microsoft Academic Knowledge API. Visit https://msr-apis.portal.azure-api.net/ to get your key"
    )
    parser.add_argument(
        '--entity',
        default='paper',
        help='Entity type to download',
        choices=['paper', 'author', 'affiliation', 'study field'])
    parser.add_argument(
        '--save',
        default=False,
        action='store_true',
        help="Path to store the file. By default it will be in Downloads"
    )
    parser.add_argument(
        '--format',
        type=str,
        default='csv',
        choices=['csv', 'json']
    )
    parser.add_argument(
        '--count',
        type=int,
        default=100,
        help="Number documents to download"
    )
    parser.add_argument(
        '--AA.AfId',
        type=str,
        help='Author affiliation id')
    parser.add_argument(
        '--AA.AfN',
        type=str,
        help='Author affiliation name, comma separated values for more than one value')
    parser.add_argument(
        '--AA.AuId',
        type=str,
        help='Author Id from Microsoft Academic. Comma separated ids')
    parser.add_argument(
        '--AA.AuN',
        type=str,
        help='Author name. Comma separated names for multiple authors')
    parser.add_argument(
        '--D',
        type=str,
        help='Date published in YYYY-MM-DD format')
    parser.add_argument(
        '--F.FN',
        type=str,
        help="Field of study. Comma separated values for more than one field"
    )
    parser.add_argument(
        '--Id',
        type=int,
        help="Paper ID from Microsoft Academic"
    )
    parser.add_argument(
        '--Ti',
        type=str,
        help="Paper title"
    )
    parser.add_argument(
        '--Y',
        type=str,
        help="Publication Year. It can also accepts >, < and <>"
    )
    parser.add_argument(
        '--citations',
        action='store_true',
        default=False,
        help="This field returns all the cited papers for given titles or paper ids"
    )
    parser.add_argument(
        '--AuN',
        type=str,
        default=False,
        help="Author name/s to download authors profile"
    )
    parser.add_argument(
        '--FN',
        type=str,
        default=False,
        help="Author name/s to download authors profile"
    )

    args = parser.parse_args()
    return args

def dispatch_entity(entity_type):
    assert entity_type in [PAPER, AUTHOR, AFFILIATION, STUDY_FIELD], "Provided entity is not available"
    if entity_type == PAPER:
        return Paper
    elif entity_type == STUDY_FIELD:
        return StudyField
    elif entity_type == AUTHOR:
        return Author



if __name__ == "__main__":
    args = parse_args()
    entity_class = dispatch_entity(args.entity)
    data_downloader = entity_class(args)
    data_downloader()
