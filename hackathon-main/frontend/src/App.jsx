import { useEffect, useState } from "react";
import "./App.css";

import Home from "./pages/Home";
import Chat from "./pages/Chat";
import Login from "./pages/Login";

import { supabase } from "./services/supabase";
import { getDocuments } from "./services/api";

function App() {
    const [session, setSession] = useState(null);
    const [documents, setDocuments] = useState([]);
    const [selectedDocumentIds, setSelectedDocumentIds] = useState([]);
    const [loadingDocuments, setLoadingDocuments] = useState(false);

    // Check whether user is already logged in
    useEffect(() => {
        const getSession = async () => {
            const {
                data: { session },
            } = await supabase.auth.getSession();

            setSession(session);
        };

        getSession();

        const {
            data: { subscription },
        } = supabase.auth.onAuthStateChange(
            (_event, session) => {
                setSession(session);
            }
        );

        return () => {
            subscription.unsubscribe();
        };
    }, []);

    const fetchDocuments = async () => {
        try {
            setLoadingDocuments(true);

            const data = await getDocuments();
            const docs = data.documents || [];

            setDocuments(docs);

            // Keep only selections that still exist
            setSelectedDocumentIds((previous) => {
                const validIds = previous.filter((id) =>
                    docs.some((doc) => doc.id === id)
                );

                // If there is exactly one document,
                // automatically select it.
                if (docs.length === 1) {
                    return [docs[0].id];
                }

                return validIds;
            });

        } catch (error) {
            console.error(error);
        } finally {
            setLoadingDocuments(false);
        }
    };

    // Fetch documents after login
    useEffect(() => {
        if (session) {
            fetchDocuments();
        } else {
            setDocuments([]);
            setSelectedDocumentIds([]);
        }
    }, [session]);

    const handleLogout = async () => {
        const { error } = await supabase.auth.signOut();

        if (error) {
            console.error(error);
        }
    };

    // Not logged in
    if (!session) {
        return <Login onLogin={setSession} />;
    }

    return (
        <div className="app">

            <header className="app-header">

                <div>
                    <h1>Insurance RAG Assistant</h1>

                    <p>
                        {documents.length === 0
                            ? "Your private insurance knowledge assistant"
                            : `📚 ${documents.length} document${documents.length !== 1 ? "s" : ""} uploaded`}
                    </p>
                </div>

                <button
                    className="logout-btn"
                    onClick={handleLogout}
                >
                    Logout
                </button>

            </header>

            <main>

                <Home
                    documents={documents}
                    selectedDocumentIds={selectedDocumentIds}
                    setSelectedDocumentIds={setSelectedDocumentIds}
                    refreshDocuments={fetchDocuments}
                    loadingDocuments={loadingDocuments}
                />

                <Chat
                    selectedDocumentIds={selectedDocumentIds}
                />

            </main>

        </div>
    );
}

export default App;