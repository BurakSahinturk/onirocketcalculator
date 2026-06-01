import type { EngineDesc, languageType, TankRecipe } from "@/assets/types";
import { Alert, Box, Flex, Text } from "@chakra-ui/react";

// ─── Types & Interfaces ────────────────────────────────────────────────────────
interface StatsProps {
  dryMass: number;
  propellantMass: number;
  range: number;
  engine: EngineDesc | null;
  fuels: Record<string, TankRecipe>;
  lisan: languageType;
}

// ─── Translatable Text ─────────────────────────────────────────────────────────
const dryMassText = {
  En: "Dry Mass: ",
  Tr: "Kuru Kütle: ",
};
const propellantText = {
  En: "Propellant Mass: ",
  Tr: "Yakıt Kütlesi: ",
};
const wetMassText = {
  En: "Wet Mass: ",
  Tr: "Toplam Kütle: ",
};
const rangeText = {
  En: "Range: ",
  Tr: "Menzil: ",
};
const missingEngineText = {
  En: "Select an Engine to calculate range",
  Tr: "Menzili hesab edebilmek için motör seçin",
};
const notEnoughSteamText = {
  En: "Steam Engine's fuel must be added as 'internal fuel'",
  Tr: "Buhar motoruna yakıt motör içi kısmından eklenmeli",
};
const notEnoughFuelText = {
  En: "Insufficient fuel for lift-off",
  Tr: "Kalkış için kafi yakıt mevcut değil",
};
const notEnoughOxidizerText = {
  En: "Insufficient oxidizer for lift-off",
  Tr: "Kalkış için kafi oksitleyici mevcut değil",
};
const fuelsNotEqualText = {
  En: "For a most efficient flight, fuel and oxidizer amounts must be equal",
  Tr: "En efektif uçuş için, yakıt ve oksitleyici miktarları eşit olmalı",
};
const oxiOnSteamText = {
  En: "Steam engines does not use oxidizers",
  Tr: "Buhar motoru oksitleyici kullanmaz.",
};

const Stats = ({
  dryMass,
  propellantMass,
  range,
  engine,
  fuels,
  lisan,
}: StatsProps) => {
  const fuelAmount: number = fuels["fuel_tank"].fuel_amount;
  const oxyliteAmount: number = fuels["oxylite_tank"].fuel_amount;
  const loxAmount: number = fuels["lox_tank"].fuel_amount;
  const oxiAmount = oxyliteAmount + loxAmount;

  const getEngineAlert = () => {
    let message = undefined;
    if (engine === null) {
      message = missingEngineText[lisan];
    } else if (engine.uses_internal_fuel && range <= 0) {
      message = notEnoughSteamText[lisan];
    } else {
      return null;
    }
    return (
      <Alert.Root status="error" size="sm">
        <Alert.Indicator />
        <Alert.Description>{message}</Alert.Description>
      </Alert.Root>
    );
  };

  const getFuelAlert = () => {
    if (engine?.uses_internal_fuel) return null;
    if (range > 0) {
      return null;
    }
    if (fuelAmount <= oxiAmount) {
      return (
        <Alert.Root status="error" size="sm">
          <Alert.Indicator />
          <Alert.Description>{notEnoughFuelText[lisan]}</Alert.Description>
        </Alert.Root>
      );
    } else if (fuelAmount > oxiAmount) {
      return (
        <Alert.Root status="error" size="sm">
          <Alert.Indicator />
          <Alert.Description>{notEnoughOxidizerText[lisan]}</Alert.Description>
        </Alert.Root>
      );
    }
  };

  const getFuelsNotEqualAlert = () => {
    if (fuelAmount !== oxiAmount)
      return (
        <Alert.Root status="warning" size="sm">
          <Alert.Indicator />
          <Alert.Description>{fuelsNotEqualText[lisan]}</Alert.Description>
        </Alert.Root>
      );
  };

  const getUnnecessaryOxidizerAlert = () => {
    if (engine?.uses_internal_fuel && oxiAmount > 0) {
      return (
        <Alert.Root status="warning" size="sm">
          <Alert.Indicator />
          <Alert.Description>{oxiOnSteamText[lisan]}</Alert.Description>
        </Alert.Root>
      );
    }
  };

  return (
    <>
      <Box w={"85%"}>
        <Flex justify={"space-between"}>
          <Text>{dryMassText[lisan]}</Text>
          <Text>{dryMass} kg</Text>
        </Flex>
        <Flex justify={"space-between"}>
          <Text>{propellantText[lisan]}</Text>
          <Text>{propellantMass} kg</Text>
        </Flex>
        <Flex justify={"space-between"}>
          <Text>{wetMassText[lisan]}</Text>
          <Text>{dryMass + propellantMass} kg</Text>
        </Flex>
        <Flex justify={"space-between"}>
          <Text>{rangeText[lisan]}</Text>
          <Text>{range > 0 ? range.toFixed(0) : "-"} km</Text>
        </Flex>
        {getEngineAlert()}
        {getFuelAlert()}
        {getFuelsNotEqualAlert()}
        {getUnnecessaryOxidizerAlert()}
      </Box>
    </>
  );
};

export default Stats;
