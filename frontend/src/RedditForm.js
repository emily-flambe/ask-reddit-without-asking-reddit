import {
    Box,
    Button,
    Input,
    FormControl,
    FormLabel,
    Heading,
    VStack,
    Text,
} from "@chakra-ui/react";

function RedditForm() {
    return (
        <VStack spacing={4} align="stretch" w="100%" maxW="md" mx="auto" mt={10}>
            <Heading textAlign="center">Reddit Summarizer</Heading>
            <form>
                <FormControl>
                    <FormLabel>Enter your query</FormLabel>
                    <Input placeholder="Type your query here" />
                </FormControl>
                <Button colorScheme="teal" mt={4}>
                    Submit
                </Button>
            </form>
        </VStack>
    );
}
