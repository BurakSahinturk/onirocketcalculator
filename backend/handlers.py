"""FastAPI exception handlers"""
# filename: handlers.py

# ------------------------------------------------------------------
# 1. Imports
# ------------------------------------------------------------------
from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions import *

BAD_REQUEST_EXCEPTIONS = (
    NotAnEngineError,
    HasNoEngineError,
    InvalidAmountError,
    CapacityError,
    InvalidOxidizerTypeError,
    WrongModuleTypeError,
    WrongEngineTypeError,
    LimitExceededError,
    UnknownComponentError,
)

NOT_FOUND_EXCEPTIONS = (
    NoModulesError,
)

BAD_CALCULATION_EXCEPTIONS = (
    FruitlessCalculation,
)

async def bad_request_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"detail": { "code": exc.code if isinstance(exc, RocketError) else "UNKNOWN_ERROR", "message": str(exc), }},
    )

async def not_found_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content={"detail": { "code": exc.code if isinstance(exc, RocketError) else "UNKNOWN_ERROR", "message": str(exc), }},
    )
async def bad_calculation(request: Request, exc: Exception):
    return JSONResponse(
        status_code=416, # I know this is wrong. Just appreciate the joke
        content={"detail": { "code": exc.code if isinstance(exc, RocketError) else "UNKNOWN_ERROR", "message": str(exc), }},
    )