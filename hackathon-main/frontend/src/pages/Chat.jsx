import { useEffect, useState } from "react";
import { askQuestion } from "../services/api";
import ChatWindow from "../components/ChatWindow";

export default function Chat({ selectedDocumentIds }) {
    const [messages, setMessages] = useState([]);
    const [question, setQuestion] = useState("");
    const [loading, setLoading] = useState(false);

    // Clear chat when selected documents change
    useEffect(() => {
        setMessages([]);
    }, [selectedDocumentIds]);

    const handleSend = async () => {
        if (!question.trim()) return;

        // At least one document must be selected
        if (
            !selectedDocumentIds ||
            selectedDocumentIds.length === 0
        ) {
            alert("Please select at least one document first.");
            return;
        }

        const currentQuestion = question.trim();

        // Add user message
        const userMessage = {
            role: "user",
            content: currentQuestion,
        };

        setMessages((prev) => [
            ...prev,
            userMessage,
        ]);

        setQuestion("");
        setLoading(true);

        try {
            console.log(
                "Selected document IDs:",
                selectedDocumentIds
            );

            console.log(
                "Question:",
                currentQuestion
            );

            const response = await askQuestion(
                currentQuestion,
                selectedDocumentIds
            );

            console.log(
                "RAG response:",
                response
            );

            console.log(
                "Citations:",
                response.citations
            );

            // IMPORTANT:
            // Keep BOTH answer and citations
            const assistantMessage = {
                role: "assistant",
                content: response.answer,
                citations: response.citations || [],
            };

            setMessages((prev) => [
                ...prev,
                assistantMessage,
            ]);

        } catch (error) {
            console.error(error);

            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    content: `❌ ${error.message}`,
                    citations: [],
                },
            ]);

        } finally {
            setLoading(false);
        }
    };

    return (
        <ChatWindow
            messages={messages}
            loading={loading}
            onSend={handleSend}
            question={question}
            setQuestion={setQuestion}
        />
    );
}