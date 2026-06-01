import type {
  EngineDesc,
  EngineRecipe,
  GameConstants,
  languageType,
  ModuleKey,
  RocketPart,
  RocketRecipe,
  TankDesc,
  TankKey,
  TankRecipe,
} from "@/assets/types";
import { Box, Stack } from "@chakra-ui/react";
import ExtraModulesForm from "./FormSubComponents/ExtraModulesForm";
import EngineForm from "./FormSubComponents/EngineForm";
import FuelForm from "./FormSubComponents/FuelForm";

// ─── Types & Interfaces ────────────────────────────────────────────────────────
interface RocketFormProps {
  recipe: RocketRecipe;
  engine: EngineDesc | null;
  enginesList: EngineDesc[];
  fuelTanksList: TankDesc[];
  oxidizerTanksList: TankDesc[];
  thrustersList: RocketPart[];
  onUpdateRecipe: (
    key: keyof RocketRecipe,
    value: EngineRecipe | Record<string, number> | Record<string, TankRecipe>,
  ) => void;
  extraModulesList: RocketPart[];
  gameConstants: GameConstants;
  lisan: languageType;
}

const RocketForm = ({
  recipe,
  engine,
  enginesList,
  fuelTanksList,
  oxidizerTanksList,
  thrustersList,
  onUpdateRecipe,
  extraModulesList,
  gameConstants,
  lisan,
}: RocketFormProps) => {
  const updateFuelSystem = (
    tank: TankKey,
    property: keyof TankRecipe,
    value: number,
  ) => {
    const oldTankData = recipe.fuel_system[tank];

    const updatedTank = {
      ...oldTankData,
      [property]: value,
    };

    if (property === "tank_count") {
      const tankMeta = [...fuelTanksList, ...oxidizerTanksList].find(
        (t) => t.key === tank,
      );

      const maxCapacity = value * (tankMeta?.capacity ?? 0);

      updatedTank.fuel_amount = Math.min(updatedTank.fuel_amount, maxCapacity);
    }
    const newFuelSystem = {
      ...recipe.fuel_system,
      [tank]: updatedTank,
    };

    onUpdateRecipe("fuel_system", newFuelSystem);
  };

  const updateEngineSystem = (
    key: keyof EngineRecipe,
    value: number | string | null,
  ) => {
    const newEngineSys = {
      ...recipe.engine_system,
      [key]: value,
    } as EngineRecipe;
    onUpdateRecipe("engine_system", newEngineSys);
  };

  const updateModules = (key: ModuleKey, value: number) => {
    const newModulesList = { ...recipe.modules, [key]: value };
    onUpdateRecipe("modules", newModulesList);
  };

  return (
    <Stack divideY="2px">
      <Box py={2}>
        <EngineForm
          engine={engine}
          enginesList={enginesList}
          thrustersList={thrustersList}
          engineRecipe={recipe.engine_system}
          onUpdateEngineSystem={updateEngineSystem}
          maxThrusters={gameConstants.MAX_THRUSTERS}
          lisan={lisan}
        />
      </Box>
      <Box py={2}>
        <FuelForm
          fuelTanksList={fuelTanksList}
          oxidizerTanksList={oxidizerTanksList}
          fuelRecipe={recipe.fuel_system}
          onUpdateFuelSystem={updateFuelSystem}
          maxFuelTanks={gameConstants.MAX_FUEL_TANKS}
          maxOxiTanks={gameConstants.MAX_OXI_TANKS}
          lisan={lisan}
        />
      </Box>
      <Box flexGrow={1}>
        <ExtraModulesForm
          extraModulesList={extraModulesList}
          moduleCounts={recipe.modules}
          onUpdateModules={updateModules}
          maxModules={gameConstants.MAX_MODULE_COUNT}
          lisan={lisan}
        />
      </Box>
    </Stack>
  );
};

export default RocketForm;
