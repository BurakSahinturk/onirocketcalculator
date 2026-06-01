import type { RocketRecipe } from "@/assets/types";
import { useState } from "react";

const useRecipe = () => {
  const [recipe, setRecipe] = useState<RocketRecipe>({
    engine_system: {
      engine: null,
      thrusters: 0,
      internal_fuel: 0,
    },

    fuel_system: {
      fuel_tank: { tank_count: 0, fuel_amount: 0 },
      oxylite_tank: { tank_count: 0, fuel_amount: 0 },
      lox_tank: { tank_count: 0, fuel_amount: 0 },
    },

    modules: {
      command: 1,
      research: 0,
      sightseeing: 0,
      solid_cargo: 0,
      liquid_cargo: 0,
      gas_cargo: 0,
      bio_cargo: 0,
    },
  });

  return { recipe, setRecipe };
};

export default useRecipe;
