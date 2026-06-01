import {
  OXIDIZER_TYPES,
  type EngineDesc,
  type languageType,
  type RocketRecipe,
} from "@/assets/types";
import apiClient from "@/services/api-client";
import {
  Button,
  Fieldset,
  HStack,
  NativeSelect,
  RadioGroup,
  Spinner,
} from "@chakra-ui/react";
import { isAxiosError } from "axios";
import { useState } from "react";

// ─── Translatable Text ─────────────────────────────────────────────────────────
const MissingRangeText = {
  En: "Please select a range",
  Tr: "Lütfen bir menzil seçin",
};
const DropDownText = {
  En: "Select Range",
  Tr: "Menzil Seç",
};
const MissingOxidizerText = {
  En: "Please select an oxidizer",
  Tr: "Lütfen bir oksitleyici seçin",
};
const LegendText = {
  En: "Calculate for Target",
  Tr: "Menzil için yakıt hesabı",
};
const ButtonText = {
  En: "Configure Rocket",
  Tr: "Hesapla",
};
const ERROR_MESSAGES = {
  416: {
    En: "Range is not achievable with these modules",
    Tr: "Bu roket bu menzile ulaşamaz",
  },

  400: {
    En: "Bad Request",
    Tr: "İstemde sorun var sanki?",
  },
};

// ─── Types & Interfaces ────────────────────────────────────────────────────────
interface TargetProps {
  recipe: RocketRecipe;
  engine: EngineDesc | null;
  updateRecipe: (recipe: RocketRecipe) => void;
  lisan: languageType;
}

const Target = ({ recipe, engine, updateRecipe, lisan }: TargetProps) => {
  const [targetRange, setTargetRange] = useState<number>(0);
  const [isConfiguring, setIsConfiguring] = useState<boolean>(false);
  const [oxidizer, setOxidizer] = useState<keyof typeof OXIDIZER_TYPES | null>(
    null,
  );
  const [error, setError] = useState<string | null>(null);

  const onSubmit = () => {
    if (targetRange == 0) {
      setError(MissingRangeText[lisan]);
      return;
    }
    if (recipe.engine_system.engine == null) {
      if (oxidizer == null) {
        setError(MissingOxidizerText[lisan]);
        return;
      }
    }
    const rangeRequest = {
      rocket_recipe: recipe,
      desired_range: targetRange,
      oxidizer: oxidizer,
    };
    setIsConfiguring(true);
    apiClient
      .post("/configure", rangeRequest)
      .then((res) => {
        updateRecipe(res.data);
        setError(null);
      })
      .catch((err: unknown) => {
        if (!isAxiosError(err)) {
          setError("Unexpected error");
          return;
        }

        const detail = err.response?.data?.detail;

        if (!detail) {
          setError("Unknown error");
          return;
        }

        const code = detail.code as keyof typeof ERROR_MESSAGES;

        setError(ERROR_MESSAGES[code]?.[lisan] ?? detail.message);
      })
      .finally(() => setIsConfiguring(false));
  };

  return (
    <Fieldset.Root marginTop={10} disabled={isConfiguring}>
      {isConfiguring && <Spinner size={"sm"} />}
      <Fieldset.Legend>{LegendText[lisan]}</Fieldset.Legend>
      {error && <Fieldset.HelperText>{error}</Fieldset.HelperText>}
      <Fieldset.Content>
        <NativeSelect.Root marginTop={"-10px"}>
          <NativeSelect.Field
            name="targetRange"
            value={targetRange}
            onChange={(e) => setTargetRange(Number(e.currentTarget.value))}>
            <option value={0}>{DropDownText[lisan]}</option>
            {Array.from({ length: 18 }).map((_, i) => (
              <option key={i} value={(i + 1) * 10000}>
                {(i + 1) * 10000}km
              </option>
            ))}
          </NativeSelect.Field>
          <NativeSelect.Indicator />
        </NativeSelect.Root>
        <RadioGroup.Root
          value={oxidizer ?? ""}
          disabled={engine?.uses_internal_fuel}
          onValueChange={(e) =>
            setOxidizer(e.value as keyof typeof OXIDIZER_TYPES)
          }>
          <HStack gap="6">
            {Object.entries(OXIDIZER_TYPES).map(([key, value]) => (
              <RadioGroup.Item value={key} key={key}>
                <RadioGroup.ItemHiddenInput />
                <RadioGroup.ItemIndicator />
                <RadioGroup.ItemText>{value[lisan]}</RadioGroup.ItemText>
              </RadioGroup.Item>
            ))}
          </HStack>
        </RadioGroup.Root>
      </Fieldset.Content>
      <Button
        type="submit"
        alignSelf="flex-start"
        onClick={onSubmit}
        disabled={isConfiguring}>
        {ButtonText[lisan]}
      </Button>
    </Fieldset.Root>
  );
};

export default Target;
