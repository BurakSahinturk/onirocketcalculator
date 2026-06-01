"""Conversions for Domain -> REST"""
# filename: json_conversions

# ------------------------------------------------------------------
# 1. Imports
# ------------------------------------------------------------------
from components import FuelTank
from rocket import Rocket
from schema import EngineRecipe, FuelDTO, RocketRecipe
from component_registry import registry


# ------------------------------------------------------------------
# 2. From Metadata Recipe to Domain Object
# ------------------------------------------------------------------
def write_recipe(rocket: Rocket) -> RocketRecipe:
    engine_recipe = EngineRecipe(
        engine=registry.get_key(rocket.engine) if rocket.engine else None,
        thrusters=rocket.engine_system.thruster_count,
        internal_fuel=rocket.engine_system.fuel,
        internal_capacity=rocket.engine_system.capacity)
    fuel_recipe = {tank.KEY: FuelDTO(tank_count=data.tank_count, fuel_amount=data.fuel_amount) for tank, data in rocket.fuel_system.tanks_data.items()}
    modules = {key: value for key, value in rocket.modules.modules.items() if value > 0}
    return RocketRecipe(engine_system=engine_recipe, fuel_system=fuel_recipe, modules=modules)

# ------------------------------------------------------------------
# 3. From Domain Object to Metadata
# ------------------------------------------------------------------
def from_recipe(recipe: RocketRecipe) -> Rocket:
    rocket = Rocket()
    engine_sys = recipe.engine_system
    fuel_sys = recipe.fuel_system

    # --- Engine System ---
    engine_name = engine_sys.engine
    if engine_name is not None:
        engine = registry.get_engine(engine_name)
        rocket.engine_system.set_engine(engine)
    for _ in range(engine_sys.thrusters):
        rocket.engine_system.add_thruster()
    rocket.set_fuel(engine_sys.internal_fuel)
    
    # --- Fuel System ---
    for tank_key, data in fuel_sys.items():
        tank = registry.get_tank(tank_key)
        for _ in range(data.tank_count):
            rocket.fuel_system.add_tank(tank)
        rocket.fuel_system.set_fuel_by_tank(tank, data.fuel_amount)

    for module_name in recipe.modules:
        if recipe.modules[module_name]:
            if module_name == "command":
                continue
            module = registry.get_extra_module(module_name)
            for _ in range(recipe.modules[module_name]):
                rocket.modules.add_module(module)
    return rocket