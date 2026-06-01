"""Test Module for JSON ↔ Domain conversions"""
# filename: tests\test_json_conversions.py

import pytest
from json_conversions import from_recipe, write_recipe
from schema import RocketRecipe, EngineRecipe, FuelDTO
from rocket import Rocket
from components import (
    SteamEngine,
    PetroleumEngine,
)

class TestJsonConversions:

    @pytest.fixture
    def sample_recipe(self):
        """A valid RocketRecipe: steam engine, 2 thrusters, 3 research, 1 sightseeing."""
        engine_recipe = EngineRecipe(
            engine="steam_engine",
            thrusters=2,
            uses_internal_fuel=True,
            internal_fuel=30.0,
        )

        fuel_recipe = {
        "fuel_tank": FuelDTO(),
        "oxylite_tank": FuelDTO(tank_count=1, fuel_amount=10.0),
        "lox_tank": FuelDTO()
        }
        modules = {
            "command": 1,
            "research": 3,
            "sightseeing": 1,
        }
        return RocketRecipe(
            engine_system=engine_recipe,
            fuel_system=fuel_recipe,
            modules=modules,
        )

    # ------------------------------------------------------------------
    # from_recipe tests
    # ------------------------------------------------------------------
    def test_from_recipe_basic_conversion(self, sample_recipe):
        """Recipe → Rocket must preserve engine fuel, oxylite, and extra modules."""
        rocket = from_recipe(sample_recipe)

        assert rocket.engine is SteamEngine
        assert rocket.fuel_amount == 30.0
        assert rocket.fuel_system.oxylite_amount == 10.0
        assert rocket.modules.modules["research"] == 3
        assert rocket.modules.modules["sightseeing"] == 1
        assert rocket.engine_system.thruster_count == 2

    def test_from_recipe_no_engine(self):
        """A recipe with no engine creates a rocket with no engine."""
        recipe = RocketRecipe(
            engine_system=EngineRecipe(engine=None),
            fuel_system={}
        )
        rocket = from_recipe(recipe)
        assert rocket.engine is None

    # ------------------------------------------------------------------
    # write_recipe tests
    # ------------------------------------------------------------------
    def test_write_recipe_conversion(self):
        """Domain rocket → DTO: use petroleum engine, one fuel tank, 50 fuel."""
        rocket = Rocket()
        rocket.engine_system.set_engine(PetroleumEngine)
        rocket.fuel_system.add_fuel_tank()
        rocket.set_fuel(50.0)

        recipe = write_recipe(rocket)

        assert recipe.engine_system.engine == "petrol_engine"
        assert recipe.fuel_system["fuel_tank"].fuel_amount == 50.0
        assert recipe.fuel_system["fuel_tank"].tank_count == 1
        assert recipe.fuel_system["oxylite_tank"].tank_count == 0

    # ------------------------------------------------------------------
    # Round‑trip invariance
    # ------------------------------------------------------------------
    def test_conversion_round_trip(self, sample_recipe):
        """Recipe → Rocket → Recipe must produce identical data."""
        rocket = from_recipe(sample_recipe)
        new_recipe = write_recipe(rocket)
        # They should be exactly the same dict
        reconstructed_rocket = from_recipe(new_recipe)
        assert reconstructed_rocket.engine is rocket.engine
        assert reconstructed_rocket.fuel_amount == rocket.fuel_amount
        assert reconstructed_rocket.fuel_system.oxylite_amount == rocket.fuel_system.oxylite_amount
        assert reconstructed_rocket.engine_system.thruster_count == rocket.engine_system.thruster_count
        assert reconstructed_rocket.modules.modules == rocket.modules.modules