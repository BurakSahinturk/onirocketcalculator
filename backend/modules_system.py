"""Modules Subsystem of Rockets"""
# filename: modules_system.py

# ------------------------------------------------------------------
# 1. Imports
# ------------------------------------------------------------------
from component_bases import Component, ExtraModule
from components import CommandCapsule
from component_registry import registry
from config import MAX_EXTRA_MODULE_COUNT
from exceptions import NoModulesError, LimitExceededError, WrongModuleTypeError

extra_modules = registry.list_extra_modules()

class ModuleSystem:
    def __init__(self) -> None:
        self._modules:dict[type[Component], int] = {}
        # Command Capsule is required
        self._modules[CommandCapsule] = 1
        for module in extra_modules:
            self._modules[module] = 0

    @property
    def mass(self) -> float:
        mass = 0
        for module, count in self._modules.items():
            mass += module.MASS * count 
        return mass
    
    def add_module(self, module: type[ExtraModule]) -> None:
        if not issubclass(module, ExtraModule):
            raise WrongModuleTypeError("This method is for extra modules only")
        if module not in extra_modules:
            raise WrongModuleTypeError(f"Unkown Extra Module: {module}")
        if sum(self._modules.values()) >= MAX_EXTRA_MODULE_COUNT:
            raise LimitExceededError("A too heavy rocket will be impossible to fly")
        self._modules[module] += 1

    def remove_module(self, module: type[ExtraModule]) -> None:
        if not issubclass(module, ExtraModule):
            raise WrongModuleTypeError("This method is for extra modules only")
        if module not in self._modules:
            raise WrongModuleTypeError(f"Unkown Extra Module: {module}")
        if self._modules[module] <= 0:
            raise NoModulesError("No module to remove")        
        self._modules[module] -= 1
    
    @property
    def modules(self) -> dict[str, int]:
        return {module.KEY: self._modules[module] for module in self._modules}
