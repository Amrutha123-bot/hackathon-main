import { useState } from "react";
import ChatWindow from "../components/ChatWindow";
import { askQuestion } from "../services/api";

export default function Chat() {

    const [messages, setMessages] = useState([]);

    const [question, setQuestion] = useState("");

    const [loading, setLoading] = useState(false);

    const handleSend = async () => {

        if (!question.trim()) return;

        const userMessage = {
            role: "user",
            content: question
        };

        setMessages(prev => [...prev, userMessage]);

        const currentQuestion = question;

        setQuestion("");

        setLoading(true);

        try {

            const response = await askQuestion(currentQuestion);

            const botMessage = {
                role: "assistant",
                content: response.answer
            };

            setMessages(prev => [...prev, botMessage]);

        }
        catch (error) {

            console.error(error);

            const botMessage = {
                role: "assistant",
                content:
                    "Sorry! Unable to generate an answer at the moment."
            };

            setMessages(prev => [...prev, botMessage]);

        }
        finally {

            setLoading(false);

        }

    };

    return (

        <ChatWindow
            messages={messages}
            loading={loading}
            question={question}
            setQuestion={setQuestion}
            onSend={handleSend}
        />

    );

}