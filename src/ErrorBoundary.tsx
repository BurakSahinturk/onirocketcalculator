import React from "react";
import { Alert, Button, Container, Heading, Text } from "@chakra-ui/react";

interface ErrorBoundaryProps {
  children: React.ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  errorMessage: string | null;
}

class ErrorBoundary extends React.Component<
  ErrorBoundaryProps,
  ErrorBoundaryState
> {
  constructor(props: ErrorBoundaryProps) {
    super(props);

    this.state = {
      hasError: false,
      errorMessage: null,
    };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return {
      hasError: true,
      errorMessage: error.message,
    };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error("Application crashed:", error);
    console.error(errorInfo);
  }

  handleReload = () => {
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <Container centerContent py={20}>
          <Heading mb={4}>Something went wrong 🚨</Heading>

          <Alert.Root status="error" maxW="600px">
            <Alert.Indicator />
            <Alert.Content>
              <Alert.Title>Application Error</Alert.Title>
              <Alert.Description>
                {this.state.errorMessage ?? "Unknown application error"}
              </Alert.Description>
            </Alert.Content>
          </Alert.Root>

          <Text mt={6}>Try refreshing the page.</Text>

          <Button mt={4} onClick={this.handleReload}>
            Reload Application
          </Button>
        </Container>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
