import { useState } from "react";
import { askQuestion } from "../services/api";
import ChatWindow from "../components/ChatWindow";

export default function Chat({ selectedCollection }) {
    const [messages, setMessages] = useState([]);
    const [question, setQuestion] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSend = async () => {
        if (!question.trim()) return;

        if (!selectedCollection) {
            alert("Please upload and select a knowledge base first.");
            return;
        }

        const userMessage = {
            role: "user",
            content: question,
        };

        setMessages((prev) => [...prev, userMessage]);

        const currentQuestion = question;

        setQuestion("");
        setLoading(true);

        try {
            const response = await askQuestion(
                currentQuestion,
                selectedCollection
            );

            const assistantMessage = {
                role: "assistant",
                content: response.answer,
            };

            setMessages((prev) => [...prev, assistantMessage]);
        } catch (error) {
            console.error(error);

            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    content: `❌ ${error.message}`,
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