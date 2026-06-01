import type { languageType } from "@/assets/types";
import {
  Box,
  Flex,
  HStack,
  IconButton,
  NumberInput,
  Slider,
  Text,
} from "@chakra-ui/react";
import { LuMinus, LuPlus } from "react-icons/lu";

// ─── Types & Interfaces ────────────────────────────────────────────────────────
interface EngineFuelProps {
  internal_fuel: number;
  capacity: number;
  onUpdateEngineFuel: (value: number) => void;
  lisan: languageType;
}

// ─── Translatable Text ─────────────────────────────────────────────────────────
const InternalFuelText = {
  En: "Internal Fuel",
  Tr: "Motor İçi Yakıt",
};
const FuelAmountText = {
  En: "Current Amount: ",
  Tr: "Mevcut Yakıt: ",
};

const EngineFuel = ({
  internal_fuel,
  capacity,
  onUpdateEngineFuel,
  lisan,
}: EngineFuelProps) => {
  return (
    <Slider.Root
      width="100%"
      value={[internal_fuel]}
      min={0}
      max={capacity}
      onValueChange={(e) => onUpdateEngineFuel(Number(e.value[0]))}>
      <Slider.Label>{InternalFuelText[lisan]}</Slider.Label>
      <NumberInput.Root
        value={internal_fuel.toString()}
        onValueChange={(e) => onUpdateEngineFuel(Number(e.value))}
        min={0}
        max={capacity}>
        <HStack justify={"space-around"}>
          <Box>
            <NumberInput.DecrementTrigger asChild>
              <IconButton variant="outline" size="sm">
                <LuMinus />
              </IconButton>
            </NumberInput.DecrementTrigger>
          </Box>
          <Flex align="center">
            <Text>{FuelAmountText[lisan]}</Text>
            <NumberInput.Input width={"50px"} />
            <Text> / {capacity}</Text>
          </Flex>
          <Box>
            <NumberInput.IncrementTrigger asChild>
              <IconButton variant="outline" size="sm">
                <LuPlus />
              </IconButton>
            </NumberInput.IncrementTrigger>
          </Box>
        </HStack>
      </NumberInput.Root>
      <Slider.Control>
        <Slider.Track>
          <Slider.Range />
        </Slider.Track>
        <Slider.Thumb index={0} />
      </Slider.Control>
    </Slider.Root>
  );
};

export default EngineFuel;
