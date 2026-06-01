import type {
  languageType,
  TankDesc,
  TankKey,
  TankRecipe,
} from "@/assets/types";
import {
  Box,
  Fieldset,
  Flex,
  HStack,
  IconButton,
  NumberInput,
  Slider,
  Text,
} from "@chakra-ui/react";
import { LuMinus, LuPlus } from "react-icons/lu";

// ─── Types & Interfaces ────────────────────────────────────────────────────────
interface TanksFormProps {
  tanks: TankDesc[];
  fuelRecipe: Record<TankKey, TankRecipe>;
  onUpdateFuelSystem: (
    tank: TankKey,
    property: keyof TankRecipe,
    value: number,
  ) => void;
  maxTanks: number;
  lisan: languageType;
}

// ─── Translatable Text ─────────────────────────────────────────────────────────
const TankCountText = {
  En: "Tank Count: ",
  Tr: "Tank Sayısı: ",
};
const FuelAmountText = {
  En: "Current Amount: ",
  Tr: "Mevcut Yakıt: ",
};

const TanksForm = ({
  tanks,
  fuelRecipe,
  onUpdateFuelSystem,
  maxTanks,
  lisan,
}: TanksFormProps) => {
  return (
    <Fieldset.Root
      maxW="800px"
      my={2}
      shadow="md"
      borderWidth="1px"
      borderRadius="md">
      {tanks.map((tank) => {
        const tankData = fuelRecipe[tank.key];
        const maxCapacity = tankData.tank_count
          ? tankData.tank_count * tank.capacity
          : 0;
        return (
          <Fieldset.Root key={tank.key} p={3}>
            <Fieldset.Legend>{tank.display_name}</Fieldset.Legend>
            <HStack gap={8}>
              <Box flex={"auto"}>
                <Text fontSize="sm" mb={1}>
                  {TankCountText[lisan]}
                </Text>
                <NumberInput.Root
                  w="100px"
                  min={0}
                  max={maxTanks}
                  value={tankData.tank_count.toString()}
                  onValueChange={(e) =>
                    onUpdateFuelSystem(tank.key, "tank_count", e.valueAsNumber)
                  }>
                  <HStack>
                    <NumberInput.DecrementTrigger asChild>
                      <IconButton variant="outline" size="sm">
                        <LuMinus />
                      </IconButton>
                    </NumberInput.DecrementTrigger>
                    <NumberInput.ValueText
                      textAlign="center"
                      fontSize={"xl"}
                      m={1}
                    />
                    <NumberInput.IncrementTrigger asChild>
                      <IconButton variant="outline" size="sm">
                        <LuPlus />
                      </IconButton>
                    </NumberInput.IncrementTrigger>
                  </HStack>
                </NumberInput.Root>
              </Box>

              <Box flex={"auto"}>
                <NumberInput.Root
                  value={
                    tankData.fuel_amount ? tankData.fuel_amount.toString() : "0"
                  }
                  min={0}
                  max={maxCapacity}
                  onValueChange={(e) =>
                    onUpdateFuelSystem(tank.key, "fuel_amount", Number(e.value))
                  }>
                  <HStack justify="space-around">
                    <Box>
                      <NumberInput.DecrementTrigger asChild width={"30px"}>
                        <IconButton variant="outline" size="xs">
                          <LuMinus />
                        </IconButton>
                      </NumberInput.DecrementTrigger>
                    </Box>
                    <Flex align={"center"}>
                      <Text fontSize="sm" mb={1}>
                        {FuelAmountText[lisan]}
                      </Text>
                      <NumberInput.Input width={"60px"} />
                      <Text fontSize="sm" mb={1}>
                        / {maxCapacity}
                      </Text>
                    </Flex>
                    <Box>
                      <NumberInput.IncrementTrigger asChild>
                        <IconButton variant="outline" size="xs">
                          <LuPlus />
                        </IconButton>
                      </NumberInput.IncrementTrigger>
                    </Box>
                  </HStack>
                </NumberInput.Root>
                <Slider.Root
                  width="100%"
                  value={[tankData.fuel_amount]}
                  min={0}
                  max={maxCapacity}
                  onValueChange={(e) =>
                    onUpdateFuelSystem(
                      tank.key,
                      "fuel_amount",
                      Number(e.value[0]),
                    )
                  }
                  disabled={tankData.tank_count === 0}>
                  <Slider.Control>
                    <Slider.Track>
                      <Slider.Range />
                    </Slider.Track>
                    <Slider.Thumb index={0} />
                  </Slider.Control>
                </Slider.Root>
              </Box>
            </HStack>
          </Fieldset.Root>
        );
      })}
    </Fieldset.Root>
  );
};

export default TanksForm;
