class MAGException(Exception):
    """Base exception for MAG API"""


class MAGPaperSaveException(MAGException):
    """Exception when saving the publications"""


class MAGRequestsException(MAGException):
    """Exception in API Request"""


class MAGArgumentsException(MAGException):
    """Exception due to user arguments"""
