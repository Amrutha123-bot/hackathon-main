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
    const [selectedCollection, setSelectedCollection] = useState(null);
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

        // Listen for login/logout changes
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

            if (
                docs.length > 0 &&
                (!selectedCollection ||
                    !docs.some(
                        (d) =>
                            d.collection_name ===
                            selectedCollection
                    ))
            ) {
                setSelectedCollection(
                    docs[0].collection_name
                );
            }

            if (docs.length === 0) {
                setSelectedCollection(null);
            }

        } catch (error) {
            console.error(error);
        } finally {
            setLoadingDocuments(false);
        }
    };

    // Fetch documents only after login
    useEffect(() => {
        if (session) {
            fetchDocuments();
        } else {
            setDocuments([]);
            setSelectedCollection(null);
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

    // Logged in
    return (
        <div className="app">

            <header className="app-header">

                <div>
                    <h1>Insurance RAG Assistant</h1>

                    <p>
                        {documents.length === 0
                            ? "Your private insurance knowledge assistant"
                            : `📚 ${documents.length} document${documents.length !== 1 ? "s" : ""
                            } uploaded`}
                    </p>
                </div>

                <button className="logout-btn" onClick={handleLogout}>
                    Logout
                </button>

            </header>

            <main>

                <Home
                    documents={documents}
                    selectedCollection={selectedCollection}
                    setSelectedCollection={
                        setSelectedCollection
                    }
                    refreshDocuments={fetchDocuments}
                    loadingDocuments={loadingDocuments}
                />

                <Chat
                    selectedCollection={selectedCollection}
                />

            </main>

        </div>
    );
}

export default App;