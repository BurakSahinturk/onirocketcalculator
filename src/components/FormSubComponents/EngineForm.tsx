import type {
  EngineDesc,
  EngineRecipe,
  languageType,
  RocketPart,
} from "@/assets/types";
import {
  Field,
  Fieldset,
  HStack,
  NativeSelect,
  NumberInput,
} from "@chakra-ui/react";
import EngineFuel from "./EngineFuel";

// ─── Types & Interfaces ────────────────────────────────────────────────────────
interface EngineFormProps {
  engine: EngineDesc | null;
  enginesList: EngineDesc[];
  thrustersList: RocketPart[];
  engineRecipe: EngineRecipe;
  onUpdateEngineSystem: (
    key: keyof EngineRecipe,
    value: number | string | null,
  ) => void;
  maxThrusters: number;
  lisan: languageType;
}

// ─── Translatable Text ─────────────────────────────────────────────────────────
const HeadingText = {
  En: "Engines",
  Tr: "Roket Motoru",
};
const TypeSelectorText = {
  En: "Engine Type",
  Tr: "Motor Türü",
};
const DropDownText = {
  En: "Select Engine",
  Tr: "Motor Seç",
};

const EngineForm = ({
  engine,
  enginesList,
  thrustersList,
  engineRecipe,
  onUpdateEngineSystem,
  maxThrusters,
  lisan,
}: EngineFormProps) => {
  const onUpdateEngineFuel = (value: number) =>
    onUpdateEngineSystem("internal_fuel", value);

  return (
    <Fieldset.Root>
      <Fieldset.Legend>{HeadingText[lisan]}</Fieldset.Legend>
      <HStack>
        <Field.Root>
          <Field.Label>{TypeSelectorText[lisan]}</Field.Label>
          <NativeSelect.Root>
            <NativeSelect.Field
              value={engineRecipe.engine ?? ""}
              onChange={(e) =>
                onUpdateEngineSystem(
                  "engine",
                  e.target.value === "" ? null : e.target.value,
                )
              }>
              <option value="">{DropDownText[lisan]}</option>
              {enginesList.map((engine) => (
                <option key={engine.key} value={engine.key}>
                  {engine.display_name}
                </option>
              ))}
            </NativeSelect.Field>
            <NativeSelect.Indicator />
          </NativeSelect.Root>
        </Field.Root>
        {thrustersList.map((thruster) => (
          <Field.Root key={thruster.key}>
            <Field.Label>{thruster.display_name}</Field.Label>
            <NumberInput.Root
              value={engineRecipe.thrusters?.toString() ?? ""}
              min={0}
              max={maxThrusters}
              onValueChange={(e) =>
                onUpdateEngineSystem("thrusters", Number(e.value))
              }>
              <NumberInput.Control />
              <NumberInput.Input />
            </NumberInput.Root>
          </Field.Root>
        ))}
      </HStack>
      {engine !== null && engine.capacity !== null && (
        <EngineFuel
          internal_fuel={engineRecipe.internal_fuel}
          capacity={engine.capacity}
          onUpdateEngineFuel={onUpdateEngineFuel}
          lisan={lisan}
        />
      )}
    </Fieldset.Root>
  );
};

export default EngineForm;
