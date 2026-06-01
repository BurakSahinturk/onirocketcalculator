import type { RocketRecipe } from "@/assets/types";
import { Stack } from "@chakra-ui/react";
import RocketPartImage from "./RocketPartImage";

// ─── Types & Interfaces ────────────────────────────────────────────────────────
interface RocketImageProps {
  recipe: RocketRecipe;
}

const imageMapping = {
  command: "Command_Capsule",
  steam_engine: "Steam_Engine",
  bio_engine: "Biodiesel_Engine",
  petrol_engine: "Petroleum_Engine",
  h2_engine: "Hydrogen_Engine",
  fuel_tank: "Liquid_Fuel_Tank",
  oxylite_tank: "Solid_Oxidizer_Tank",
  lox_tank: "Liquid_Oxidizer_Tank",
  thruster: "Solid_Fuel_Thruster",
  research: "Research_Module",
  solid_cargo: "Cargo_Bay",
  liquid_cargo: "Liquid_Cargo_Tank",
  gas_cargo: "Gas_Cargo_Canister",
  bio_cargo: "Biological_Cargo_Bay",
  sightseeing: "Sight-Seeing_Module",
} as const;

type ImageKey = keyof typeof imageMapping;

const RocketImage = ({ recipe }: RocketImageProps) => {
  return (
    <>
      <Stack gap={0} justifyContent={"center"} justifyItems={"anchor-center"}>
        {
          // Command Capsule and Extra Modules
          Object.entries(recipe.modules).flatMap(([key, count]) => {
            const fileName = imageMapping[key as ImageKey];
            return Array.from({ length: count }).map((_, index) => (
              <RocketPartImage key={key + index} fileName={fileName} />
            ));
          })
        }
        {
          // Tanks
          Object.entries(recipe.fuel_system).map(([tank, tankRecipe]) => {
            const fileName = imageMapping[tank as ImageKey];
            return Array.from({ length: tankRecipe.tank_count }).map(
              (_, index) => (
                <RocketPartImage key={tank + index} fileName={fileName} />
              ),
            );
          })
        }
        {
          // Thrusters
          Array.from({ length: recipe.engine_system.thrusters }).map(
            (_, index) => (
              <RocketPartImage
                key={index}
                fileName={imageMapping["thruster"]}
              />
            ),
          )
        }
        {
          // Engine
          recipe.engine_system.engine && (
            <RocketPartImage
              fileName={imageMapping[recipe.engine_system.engine as ImageKey]}
            />
          )
        }
      </Stack>
    </>
  );
};

export default RocketImage;
