import type {
  languageType,
  TankDesc,
  TankKey,
  TankRecipe,
} from "@/assets/types";
import TanksForm from "./TanksForm";

// ─── Types & Interfaces ────────────────────────────────────────────────────────
interface FuelFormProps {
  fuelTanksList: TankDesc[];
  oxidizerTanksList: TankDesc[];
  fuelRecipe: Record<TankKey, TankRecipe>;
  onUpdateFuelSystem: (
    tank: TankKey,
    property: keyof TankRecipe,
    value: number,
  ) => void;
  maxFuelTanks: number;
  maxOxiTanks: number;
  lisan: languageType;
}

const FuelForm = ({
  fuelTanksList,
  oxidizerTanksList,
  fuelRecipe,
  onUpdateFuelSystem,
  maxFuelTanks,
  maxOxiTanks,
  lisan,
}: FuelFormProps) => {
  return (
    <>
      <TanksForm
        tanks={fuelTanksList}
        fuelRecipe={fuelRecipe}
        onUpdateFuelSystem={onUpdateFuelSystem}
        maxTanks={maxFuelTanks}
        lisan={lisan}
      />
      <TanksForm
        tanks={oxidizerTanksList}
        fuelRecipe={fuelRecipe}
        onUpdateFuelSystem={onUpdateFuelSystem}
        maxTanks={maxOxiTanks}
        lisan={lisan}
      />
    </>
  );
};

export default FuelForm;
