import { Container, Spinner, Text } from "@chakra-ui/react";

interface LoadingScreenProps {
  message: string;
}

const LoadingScreen = ({ message }: LoadingScreenProps) => {
  return (
    <Container centerContent mt={10}>
      <Spinner size="xl" />
      <Text mt={4}>{message}</Text>
    </Container>
  );
};

export default LoadingScreen;
