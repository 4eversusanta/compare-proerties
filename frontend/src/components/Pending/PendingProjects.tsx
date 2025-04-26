import { VStack, Skeleton, Box } from "@chakra-ui/react";

function PendingProjects() {
  return (
    <VStack gap={4} align="stretch" direction="column">
      {Array.from({ length: 5 }).map((_, index) => (
        <Box key={index} padding="4" borderWidth="1px" borderRadius="lg">
          <Skeleton height="20px" mb="4" />
          <Skeleton height="16px" mb="2" />
          <Skeleton height="16px" />
        </Box>
      ))}
    </VStack>
  );
}
export default PendingProjects
