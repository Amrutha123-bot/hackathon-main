import { useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import "./ChatWindow.css";

export default function ChatWindow({
    messages,
    loading,
    onSend,
    question,
    setQuestion
}) {

    const bottomRef = useRef(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({
            behavior: "smooth"
        });
    }, [messages, loading]);

    const handleSubmit = () => {

        if (!question.trim()) return;

        onSend();
    };

    const handleKeyDown = (e) => {

        if (e.key === "Enter") {
            handleSubmit();
        }

    };

    return (

        <div className="chat-container">

            <div className="chat-header">
                <h2>Insurance Assistant</h2>
                <p>Ask questions about your uploaded documents.</p>
            </div>

            <div className="chat-messages">

                {
                    messages.length === 0 && (

                        <div className="empty-chat">

                            Upload documents and ask your first question.

                        </div>

                    )
                }

                {

                    messages.map((msg, index) => (

                        <div
                            key={index}
                            className={`message ${msg.role}`}
                        >

                            <div className="message-content">

                                {

                                    msg.role === "assistant"

                                        ? (

                                            <div className="assistant-message">

                                                <ReactMarkdown>

                                                    {msg.content}

                                                </ReactMarkdown>

                                            </div>

                                        )

                                        : (

                                            msg.content

                                        )

                                }

                            </div>

                        </div>

                    ))

                }

                {

                    loading && (

                        <div className="message assistant">

                            <div className="message-content">

                                🤖 AI is analyzing your documents...

                            </div>

                        </div>

                    )

                }

                <div ref={bottomRef}></div>

            </div>

            <div className="chat-input">

                <input
                    type="text"
                    placeholder="Ask a question..."
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    onKeyDown={handleKeyDown}
                />

                <button
                    onClick={handleSubmit}
                    disabled={loading}
                >
                    Ask
                </button>

            </div>

        </div>

    );

}