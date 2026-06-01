import type {
  EngineDesc,
  RocketPart,
  RocketRecipe,
  TankDesc,
} from "@/assets/types";
import { useMemo } from "react";

const useCalculateMass = (
  recipe: RocketRecipe,
  loadingParts: boolean,
  engine: EngineDesc | null,
  commandsList: RocketPart[],
  extraModulesList: RocketPart[],
  fuelTanksList: TankDesc[],
  oxidizerTanksList: TankDesc[],
  thrustersList: RocketPart[],
) => {
  return useMemo(() => {
    let dryMass = 0;
    let propellantMass = 0;
    if (loadingParts) return { dryMass, propellantMass };

    const commandMass = commandsList[0]?.mass ?? 0;
    const extraModulesMass = extraModulesList.reduce(
      (sum, module) => sum + module.mass * (recipe.modules[module.key] ?? 0),
      0,
    );
    const fuelTanksMass = fuelTanksList.reduce(
      (sum, tank) => sum + tank.mass * recipe.fuel_system[tank.key].tank_count,
      0,
    );
    const oxidizerTanksMass = oxidizerTanksList.reduce(
      (sum, tank) => sum + tank.mass * recipe.fuel_system[tank.key].tank_count,
      0,
    );
    const thrusterMass = thrustersList.reduce(
      (sum, thruster) => sum + thruster.mass * recipe.engine_system.thrusters,
      0,
    );
    const engineMass = engine?.mass ?? 0;
    dryMass =
      commandMass +
      extraModulesMass +
      fuelTanksMass +
      oxidizerTanksMass +
      thrusterMass +
      engineMass;

    let engineFuelMass = recipe.engine_system.internal_fuel ?? 0;
    const fuelMass = fuelTanksList.reduce(
      (sum, tank) => sum + recipe.fuel_system[tank.key].fuel_amount,
      0,
    );
    const oxidizerMass = oxidizerTanksList.reduce(
      (sum, tank) => sum + recipe.fuel_system[tank.key].fuel_amount,
      0,
    );
    propellantMass = engineFuelMass + fuelMass + oxidizerMass;
    return { dryMass, propellantMass };
  }, [recipe]);
};

export default useCalculateMass;
