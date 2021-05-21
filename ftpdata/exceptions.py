import traceback


class UnknownError(Exception):
    """알 수 없는 에러"""
    def __init__(self, err):
        msg = f"Unknown Error:: {traceback.format_exc()}"
        super().__init__(msg)


class NoSuchDirectoryError(FileNotFoundError):
    """ When Directory could not be found from source """


class PresetValidationError(Exception):
    """ When Preset File fails validation """


class DialectValidationError(Exception):
    """ Dialect for create_engine is not valid """


class AuthenticationError(Exception):
    """ Auth fail """
