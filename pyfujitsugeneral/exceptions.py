"""Exceptions for FGLair Home Assistant Integration."""

class FGLairBaseException(Exception):
    """Base FGLair component Exception."""

    def __init__(self, *args: object, **kwargs: object):
        if args:
            self.message = args[0]
            super().__init__(*args)
        else:
            self.message = None

        self.custom_kwarg = kwargs.get("custom_kwarg")

    def __str__(self) -> str:
        if self.message:
            return f"FGLairBaseException, {self.message} "
        return "FGLairBaseException has been raised"

    def __repr__(self) -> str:
        if self.message:
            return f"FGLairBaseException, {self.message} "
        return "FGLairBaseException has been raised"


class FGLairGeneralException(FGLairBaseException):
    """Raise my general exception."""


class FGLairMethodException(FGLairBaseException):
    """Raise wrong method usage exception."""

    def __init__(self) -> None:
        super().__init__("Vane position not supported")


class FGLairVanePositionNotSupportedException(FGLairBaseException):
    def __init__(self) -> None:
        super().__init__("Vane position not supported")


class FGLairTemperatureOutOfRangeException(FGLairBaseException):
    def __init__(self) -> None:
        super().__init__("Temperature out of range!")


class FGLairOperationModeNoneException(FGLairBaseException):
    def __init__(self) -> None:
        super().__init__("operation_mode cannot be None!")


class FGLairMethodOrDirectionOutOfRangeException(FGLairBaseException):
    def __init__(self) -> None:
        super().__init__("Wrong usage of the method or direction out of range!")
