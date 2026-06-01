"""FastAPI configuration"""
# filename: api.py

# ------------------------------------------------------------------
# 1. Imports
# ------------------------------------------------------------------
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from component_bases import OxidizerType
from config import get_settings
from handlers import BAD_REQUEST_EXCEPTIONS, BAD_CALCULATION_EXCEPTIONS, NOT_FOUND_EXCEPTIONS
from handlers import bad_request_handler, bad_calculation, not_found_handler
from json_conversions import from_recipe, write_recipe
from rocket import Rocket
from rocket_service import RocketService
from schema import ConfigurationRequest, ReferenceData, RocketRecipe

# ------------------------------------------------------------------
# 2. FastAPI initialization
# ------------------------------------------------------------------
version = "0.2.0"

def get_service():
    return RocketService()

app = FastAPI()
app.title = "Oxygen Not Included Rocket Calculator"
app.version = version
settings = get_settings()


# ------------------------------------------------------------------
# 3. Exception Handlers
# ------------------------------------------------------------------
for exc in BAD_REQUEST_EXCEPTIONS:
    app.add_exception_handler(exc, bad_request_handler)

for exc in BAD_CALCULATION_EXCEPTIONS:
    app.add_exception_handler(exc, bad_calculation)

for exc in NOT_FOUND_EXCEPTIONS:
    app.add_exception_handler(exc, not_found_handler)


# ------------------------------------------------------------------
# 4. CORS Middleware
# ------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],   # React dev server – change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------
# 5. Endpoints
# ------------------------------------------------------------------
@app.get("/")
def home():
    """Tag"""
    return {"message": "ONI Calculator", "version": version}

@app.get("/health")
def health():
    """For checking if FastAPI is alive"""
    return {"status": "ok"}

@app.get("/reference-data", response_model=ReferenceData)
def get_rocket_reference_data(service: RocketService = Depends(get_service)) -> ReferenceData:
    """To get Bootstrap Reference Data"""
    return ReferenceData(
        constants=service.supply_constants(),
        commands=service.supply_commands(),
        engines=service.supply_engines(),
        fuel_tanks=service.supply_fuel_tanks(),
        oxidizer_tanks=service.supply_oxidizer_tanks(),
        extra_modules=service.supply_extra_modules(),
        thrusters=service.supply_thrusters()
        )

    
    
@app.post("/range")
def calculate_range(rocket_recipe: RocketRecipe, service: RocketService = Depends(get_service)) -> float:
    """Recieves Rocket -in the form of recipe- from Frontend, converts to domain object, calculates and returns the range rocket can make to"""
    rocket = from_recipe(rocket_recipe)
    return service.calculate_range(rocket)

@app.post("/configure", response_model=RocketRecipe)
def configure_for_range(configuration_request:ConfigurationRequest, service: RocketService = Depends(get_service) ) -> RocketRecipe:
    """Recieves Rocket -in the form of recipe-, a desired range, and preferred oxidizer type from Frontend, converts to domain object, mutates the rocket to reach the desired goal, and writes and returns the recipe for the rocket."""
    recipe: RocketRecipe = configuration_request.rocket_recipe
    desired_range: float = configuration_request.desired_range
    oxidizer: OxidizerType | None = configuration_request.oxidizer
    rocket: Rocket = from_recipe(recipe)
    rocket = service.configure_rocket_for_range(rocket, desired_range, oxidizer)
    return write_recipe(rocket)