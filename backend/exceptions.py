"""Custom Exception Definitions"""
# filename: exceptions.py


class RocketError(Exception):
    """Base exception for all rocket domain errors."""

    code = "ROCKET_ERROR"

    def __init__(self, message: str = "Rocket error"):
        super().__init__(message)


class NotAnEngineError(RocketError):
    """Raised when the given object is not a recognized Engine Component."""

    code = "NOT_AN_ENGINE"


class HasNoEngineError(RocketError):
    """Raised when the rocket has no engines."""

    code = "HAS_NO_ENGINE"


class InvalidAmountError(RocketError):
    """Raised when the given amount is an invalid value."""

    code = "INVALID_AMOUNT"


class CapacityError(RocketError):
    """Raised when the rocket has not enough fuel capacity."""

    code = "INSUFFICIENT_CAPACITY"


class LimitExceededError(RocketError):
    """Raised when a rocket has reached the maximum number of modules."""

    code = "LIMIT_EXCEEDED"


class NoModulesError(RocketError):
    """Raised when the rocket has no instances of the extra module that is trying to be removed."""

    code = "NO_MODULES"


class WrongModuleTypeError(RocketError):
    """Raised when the module type is invalid."""

    code = "WRONG_MODULE_TYPE"


class FruitlessCalculation(RocketError):
    """Raised when trying to configure a rocket for an unachievable range."""

    code = "FRUITLESS_CALCULATION"


class InvalidOxidizerTypeError(RocketError):
    """Raised when an oxidizer type is invalid."""

    code = "INVALID_OXIDIZER_TYPE"


class WrongEngineTypeError(RocketError):
    """Raised when an engine type is invalid."""

    code = "WRONG_ENGINE_TYPE"


class UnknownComponentError(RocketError):
    """Raised when a component's external key is not recognised."""

    code = "UNKNOWN_COMPONENT"