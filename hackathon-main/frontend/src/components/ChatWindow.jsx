import { useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import "./ChatWindow.css";

export default function ChatWindow({
    messages,
    loading,
    onSend,
    question,
    setQuestion,
}) {
    const bottomRef = useRef(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({
            behavior: "smooth",
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

                <p>
                    Ask questions about the selected documents.
                </p>
            </div>

            <div className="chat-messages">

                {messages.length === 0 && (
                    <div className="empty-chat">
                        Select one or more documents and ask
                        your first question.
                    </div>
                )}

                {messages.map((msg, index) => (
                    <div
                        key={index}
                        className={`message ${msg.role}`}
                    >

                        <div className="message-content">

                            {msg.role === "assistant" ? (

                                <div className="assistant-message">

                                    {/* AI ANSWER */}
                                    <ReactMarkdown>
                                        {msg.content}
                                    </ReactMarkdown>

                                    {/* CITATIONS */}
                                    {msg.citations &&
                                        msg.citations.length > 0 && (
                                            <div className="citations">

                                                <h4>
                                                    📚 Sources
                                                </h4>

                                                <div className="citation-list">

                                                    {msg.citations.map(
                                                        (
                                                            citation,
                                                            citationIndex
                                                        ) => (
                                                            <div
                                                                className="citation"
                                                                key={
                                                                    citationIndex
                                                                }
                                                            >

                                                                <div className="citation-icon">
                                                                    📄
                                                                </div>

                                                                <div className="citation-details">

                                                                    <strong>
                                                                        {
                                                                            citation.filename
                                                                        }
                                                                    </strong>

                                                                    {citation.page && (
                                                                        <span>
                                                                            Page{" "}
                                                                            {
                                                                                citation.page
                                                                            }
                                                                        </span>
                                                                    )}

                                                                </div>

                                                            </div>
                                                        )
                                                    )}

                                                </div>

                                            </div>
                                        )}

                                </div>

                            ) : (

                                msg.content

                            )}

                        </div>

                    </div>
                ))}

                {loading && (
                    <div className="message assistant">

                        <div className="message-content">
                            🤖 AI is analyzing your documents...
                        </div>

                    </div>
                )}

                <div ref={bottomRef}></div>

            </div>

            <div className="chat-input">

                <input
                    type="text"
                    placeholder="Ask a question..."
                    value={question}
                    onChange={(e) =>
                        setQuestion(e.target.value)
                    }
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