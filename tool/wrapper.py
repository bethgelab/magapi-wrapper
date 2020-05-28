import argparse

from magapi import *


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
        help="Flag to enable saving data to file. By default it will be in Downloads"
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
        metavar="count",
        default=100,
        help="Number documents to be downloaded"
    )
    parser.add_argument(
        '--AA.AfId',
        type=str,
        metavar="affiliation_id",
        help='Author affiliation id')
    parser.add_argument(
        '--AA.AfN',
        type=str,
        metavar="affiliation_name",
        help='Author affiliation name, comma separated values for more than one value')
    parser.add_argument(
        '--AA.AuId',
        type=str,
        help='Author Id from Microsoft Academic, comma separated ids for more than one. You can get the ID from https://academic.microsoft.com')
    parser.add_argument(
        '--AA.AuN',
        type=str,
        metavar="author_name",
        help='Author name. Comma separated names for multiple authors')
    parser.add_argument(
        '--D',
        type=str,
        metavar="publication_date",
        help='Date published in YYYY-MM-DD format. Which accepts <, > and range')
    parser.add_argument(
        '--F.FN',
        type=str,
        metavar="study_field",
        help="Field of study. Comma separated values for more than one field"
    )
    parser.add_argument(
        '--Id',
        type=int,
        metavar="paper_id",
        help="Paper ID from Microsoft Academic Graph. You can get the ID from https://academic.microsoft.com"
    )
    parser.add_argument(
        '--Ti',
        type=str,
        metavar="title",
        help="Paper title. This will not accept only English characters"
    )
    parser.add_argument(
        '--Y',
        type=str,
        metavar="publication_year",
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
        metavar="author_name",
        help="Author name/s to download authors profile"
    )
    parser.add_argument(
        '--FN',
        type=str,
        metavar="field_name",
        help="Field of study to download Study field statistics"
    )

    args = parser.parse_args()
    return args

def dispatch_entity(entity_type):
    assert entity_type in [PAPER, AUTHOR, STUDY_FIELD], "Provided entity is not available"
    if entity_type == PAPER:
        return Paper
    elif entity_type == STUDY_FIELD:
        return StudyField
    elif entity_type == AUTHOR:
        return Author

def display_warning(args):
    args = vars(args)
    if ("AuN" in args) and (args["entity"] != "author"):
        print("When AuN is given, entity must be author")
        raise SystemExit()
    if ("FN" in args) and (args["entity"] != "study field"):
        print("When FN is given, entity must be study field")
        raise SystemExit()


def main():
    args = parse_args()
    display_warning(args)
    entity_class = dispatch_entity(args.entity)
    data_downloader = entity_class(args)
    data_downloader()


if __name__ == "__main__":
    main()
