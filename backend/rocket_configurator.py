"""Fuel Tank count and exact fuel amount calculator for given rocket and desired range"""
# filename: rocket_configurator.py

# ------------------------------------------------------------------
# 1. Imports
# ------------------------------------------------------------------
from rocket import Rocket
from component_bases import OxidizerType, OxidizerEfficiency
from components import FuelTank
from exceptions import FruitlessCalculation, HasNoEngineError

# Phase 1: Deleting all fuel tanks and resetting fuel to 0 for a fresh start
# Added Rocket method Rocket.strip_tanks() to do the job.
# Phase 2: Adding tanks 1 by 1, until the desired range is achieved
def add_fuel_tanks(rocket:Rocket, desired_range: float, oxidizer_type: OxidizerType|None = None) -> Rocket:
        """Calculates how many fuel tanks are necessary to achieve the desired range with the given modules, engine and fuel type, and adds them to the rocket"""
        if rocket.engine is None:
            raise HasNoEngineError("Engine is required to calculate")
        elif rocket.engine.USE_INTERNAL_FUEL:
            return rocket #Steam engines don't get fuel tanks
        else:
            current_range = 0
            while current_range < desired_range:
                old_range=current_range
                rocket.fuel_system.add_fuel_tank()
                rocket.set_fuel(rocket.fuel_capacity)
                if oxidizer_type == OxidizerType.OXYLITE:
                    if rocket.fuel_capacity > rocket.oxylite_capacity:
                        rocket.fuel_system.add_oxylite_tank()
                    rocket.set_oxylite(rocket.fuel_capacity)
                elif oxidizer_type == OxidizerType.LOX:
                    if rocket.fuel_capacity > rocket.lox_capacity:
                        rocket.fuel_system.add_lox_tank()
                    rocket.set_lox(rocket.fuel_capacity)
                current_range = rocket.calculate_range()
                if current_range <= old_range:
                    raise FruitlessCalculation(f"Current rocket configuration can not reach {desired_range}km range")
        return rocket

# Phase 3: Calculating the exact fuel & oxidizer amount with binary search.            
def set_fuel_for_range(rocket: Rocket, desired_range: float, oxidizer_type: OxidizerType|None = None) -> Rocket:
        """Calculates the exact amount of 
        fuel that is necessary to achieve the desired range."""
        if rocket.engine is None:
            raise HasNoEngineError("This rocket is supposed own an engine")
        oxi_eff = OxidizerEfficiency[oxidizer_type] if oxidizer_type else 1 
        high = rocket.fuel_capacity
        if rocket.engine.USE_INTERNAL_FUEL:
            low = 0
        else:
            low = max(0, rocket.fuel_capacity - FuelTank.CAPACITY)
        i = 0

        while not (desired_range < rocket.calculate_range() <= desired_range + rocket.engine.EFFICIENCY * oxi_eff):
            i += 1
            # Extra safety net if something goes wrong
            if i >= 30:
                raise FruitlessCalculation("Binary search failed to converge")
            if (high - low) < 1:
                break
            mid = int((high + low) / 2)
            rocket.set_fuel(mid)
            if oxidizer_type == OxidizerType.OXYLITE:
                rocket.set_oxylite(mid)
            if oxidizer_type == OxidizerType.LOX:
                rocket.set_lox(mid)
            if desired_range < rocket.calculate_range():
                high = mid
            elif desired_range > rocket.calculate_range():
                low = mid

        # Start from up and go down step by step until it fails.
        while rocket.fuel_amount > 0 and rocket.calculate_range() >= desired_range:
            rocket.set_fuel(rocket.fuel_amount - 1)
            if oxidizer_type == OxidizerType.OXYLITE:
                rocket.set_oxylite(rocket.fuel_amount)
            if oxidizer_type == OxidizerType.LOX:
                rocket.set_lox(rocket.fuel_amount)

        # Step one step back up to find the sweet spot
        rocket.set_fuel(rocket.fuel_amount + 1)
        if oxidizer_type == OxidizerType.OXYLITE:
            rocket.set_oxylite(rocket.fuel_amount)
        if oxidizer_type == OxidizerType.LOX:
            rocket.set_lox(rocket.fuel_amount)
        
        return rocket

# Orchestration
def configure_rocket_for_range(rocket: Rocket, desired_range: float, oxidizer_type: OxidizerType | None = None) -> Rocket:
        if rocket.engine is None:
            raise HasNoEngineError("An engine is required to calculate distance")
        rocket.fuel_system.reset_fuel_system()
        if rocket.engine_system.uses_internal_fuel:
            # Steam Engines need no fuel tanks.
            rocket = set_fuel_for_range(rocket, desired_range)
        else:
            # If Engine is not Steam Engine, default oxidizer is oxylite
            if oxidizer_type is None:
                oxidizer_type = OxidizerType.OXYLITE
            rocket = add_fuel_tanks(rocket, desired_range, oxidizer_type)
            rocket = set_fuel_for_range(rocket, desired_range, oxidizer_type)
        return rocket