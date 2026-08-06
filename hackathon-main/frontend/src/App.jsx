import { useEffect, useState } from "react";
import "./App.css";

import Home from "./pages/Home";
import Chat from "./pages/Chat";

import { getDocuments } from "./services/api";

function App() {
    const [documents, setDocuments] = useState([]);
    const [selectedCollection, setSelectedCollection] = useState(null);
    const [loadingDocuments, setLoadingDocuments] = useState(true);

    const fetchDocuments = async () => {
        try {
            setLoadingDocuments(true);

            const data = await getDocuments();

            const docs = data.documents || [];

            setDocuments(docs);

            // Automatically select the first collection
            if (
                docs.length > 0 &&
                (!selectedCollection ||
                    !docs.some(
                        (d) => d.collection_name === selectedCollection
                    ))
            ) {
                setSelectedCollection(docs[0].collection_name);
            }

            // If nothing exists
            if (docs.length === 0) {
                setSelectedCollection(null);
            }
        } catch (error) {
            console.error(error);
        } finally {
            setLoadingDocuments(false);
        }
    };

    useEffect(() => {
        fetchDocuments();
    }, []);

    return (
        <div className="app">
            <header className="app-header">
                <h1>Insurance RAG Assistant</h1>

                <p>
                    {documents.length === 0
                        ? "📄 No documents uploaded yet. Upload a PDF, DOCX or TXT file to begin."
                        : `📚 ${documents.length} document(s) available`}
                </p>
            </header>

            <main>
                <Home
                    documents={documents}
                    selectedCollection={selectedCollection}
                    setSelectedCollection={setSelectedCollection}
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