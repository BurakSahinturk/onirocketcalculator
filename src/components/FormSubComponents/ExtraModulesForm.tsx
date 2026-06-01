import type { languageType, RocketPart } from "@/assets/types";
import { Field, Fieldset, Grid, NumberInput } from "@chakra-ui/react";

// ─── Types & Interfaces ────────────────────────────────────────────────────────
interface ExtraModulesFormProps {
  extraModulesList: RocketPart[];
  moduleCounts: Record<string, number>;
  onUpdateModules: (key: string, value: number) => void;
  maxModules: number;
  lisan: languageType;
}

// ─── Translatable Text ─────────────────────────────────────────────────────────
const HeadingText = {
  En: "Extra Rocket Modules",
  Tr: "Diğer Roket Modülleri",
};

const ExtraModulesForm = ({
  extraModulesList,
  moduleCounts,
  onUpdateModules,
  maxModules,
  lisan,
}: ExtraModulesFormProps) => {
  return (
    <Fieldset.Root>
      <Fieldset.Legend>{HeadingText[lisan]}</Fieldset.Legend>
      <Grid templateColumns="repeat(2, 1fr)" gap={6}>
        {extraModulesList.map((module) => (
          <Field.Root key={module.key}>
            <Field.Label>{module.display_name}</Field.Label>

            <NumberInput.Root
              // value={recipe[module.name as keyof RocketRecipe].toString()}
              min={0}
              max={maxModules}
              value={(moduleCounts[module.key] ?? 0).toString()}
              onValueChange={(e) =>
                onUpdateModules(module.key, Number(e.value))
              }>
              <NumberInput.Control />
              <NumberInput.Input />
            </NumberInput.Root>
          </Field.Root>
        ))}
      </Grid>
    </Fieldset.Root>
  );
};

export default ExtraModulesForm;
