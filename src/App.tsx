import type { EngineRecipe, RocketRecipe, TankRecipe } from "./assets/types";
import { Alert, Box, Grid, GridItem } from "@chakra-ui/react";
import Navbar from "./components/Navbar";
import RocketImage from "./components/RocketImage";
import RocketForm from "./components/RocketForm";
import Stats from "./components/Stats";
import Target from "./components/Target";
import useEngine from "./hooks/useEngine";
import useRecipe from "./hooks/useRecipe";
import useCalculateRange from "./hooks/useCalculateRange";
import useRocketModules from "./hooks/useRocketModules";
import LoadingScreen from "./components/LoadingScreen";
import Footer from "./components/Footer";
import useCalculateMass from "./hooks/useCalculateMass";
import useLanguage from "./hooks/useLanguage";

// ─── Translatable Text ─────────────────────────────────────────────────────────
const LoadingMessage = {
  En: "Loading rocket parts...",
  Tr: "Roket parçaları yükleniyor...",
};

const App: React.FC = () => {
  const { recipe, setRecipe } = useRecipe();

  const {
    loadingParts,
    commandsList,
    enginesList,
    fuelTanksList,
    oxidizerTanksList,
    extraModulesList,
    thrustersList,
    gameConstants,
    loadingError,
  } = useRocketModules();
  const { calculatedRange, rangeError } = useCalculateRange(recipe);
  const { lisan, setLisan } = useLanguage();
  const updateRecipe = (
    key: keyof RocketRecipe,
    value: EngineRecipe | Record<string, TankRecipe> | Record<string, number>,
  ) => {
    setRecipe((prev) => ({ ...prev, [key]: value }));
  };
  const error = loadingError ?? rangeError;
  const { engine } = useEngine(enginesList, recipe.engine_system.engine);
  const { dryMass, propellantMass } = useCalculateMass(
    recipe,
    loadingParts,
    engine,
    commandsList,
    extraModulesList,
    fuelTanksList,
    oxidizerTanksList,
    thrustersList,
  );

  if (loadingParts) {
    return <LoadingScreen message={LoadingMessage[lisan]} />;
  }

  return (
    <Grid
      gap={4}
      p={2}
      templateAreas={{
        base: `"navbar" "stats" "form" "footer"`,
        md: `"navbar navbar navbar" "stats image form" "footer image form"`,
      }}
      gridTemplateRows={{
        base: "1fr 5fr 20fr 1fr",
        md: "auto 1fr auto",
      }}
      gridTemplateColumns={{
        base: "1fr",
        md: "1fr auto 3fr",
      }}
      maxW={"dvw"}
      maxH={{ base: "none", md: "dvh" }}>
      <GridItem area="navbar">
        <Navbar lisan={lisan} setLisan={setLisan} />
      </GridItem>
      <GridItem area="stats" m={2}>
        <Box>
          <Stats
            dryMass={dryMass}
            propellantMass={propellantMass}
            range={calculatedRange ?? 0}
            engine={engine}
            fuels={recipe.fuel_system}
            lisan={lisan}
          />
          <Box mt={6}>
            <Target
              updateRecipe={setRecipe}
              recipe={recipe}
              engine={engine}
              lisan={lisan}
            />
          </Box>
          {error && (
            <Box mt={4}>
              <Alert.Root status="error">
                <Alert.Indicator />
                <Alert.Content>
                  <Alert.Title>Error</Alert.Title>
                  <Alert.Description>{error}</Alert.Description>
                </Alert.Content>
              </Alert.Root>
            </Box>
          )}
        </Box>
      </GridItem>
      <GridItem area="image" hideBelow="md" overflowY={"auto"}>
        <RocketImage recipe={recipe} />
      </GridItem>
      <GridItem area="footer" overflow={"auto"}>
        <Footer lisan={lisan} />
      </GridItem>
      <GridItem area="form" overflowY={"auto"}>
        <RocketForm
          engine={engine}
          recipe={recipe}
          enginesList={enginesList}
          fuelTanksList={fuelTanksList}
          oxidizerTanksList={oxidizerTanksList}
          extraModulesList={extraModulesList}
          thrustersList={thrustersList}
          onUpdateRecipe={updateRecipe}
          gameConstants={gameConstants}
          lisan={lisan}
        />
      </GridItem>
    </Grid>
  );
};

export default App;
