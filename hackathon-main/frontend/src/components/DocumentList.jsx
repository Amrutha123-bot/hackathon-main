import { deleteDocument } from "../services/api";
import "./DocumentList.css";

export default function DocumentList({
    documents,
    selectedCollection,
    setSelectedCollection,
    refreshDocuments,
}) {
    const handleDelete = async (documentId) => {
        const confirmDelete = window.confirm(
            "Are you sure you want to delete this document?"
        );

        if (!confirmDelete) return;

        try {
            await deleteDocument(documentId);
            await refreshDocuments();
        } catch (error) {
            console.error(error);
            alert(error.message);
        }
    };

    if (documents.length === 0) {
        return (
            <section className="document-section empty">
                <div className="section-heading">
                    <div>
                        <h2>Your Documents</h2>
                        <p>No documents uploaded yet.</p>
                    </div>
                </div>
            </section>
        );
    }

    return (
        <section className="document-section">
            <div className="section-heading">
                <div>
                    <h2>Your Documents</h2>
                    <p>
                        {documents.length} document
                        {documents.length !== 1 ? "s" : ""} in your
                        knowledge base
                    </p>
                </div>
            </div>

            <div className="documents-grid">
                {documents.map((doc) => (
                    <div
                        key={doc.id}
                        className={
                            selectedCollection === doc.collection_name
                                ? "document-card active"
                                : "document-card"
                        }
                    >
                        <div
                            className="document-info"
                            onClick={() =>
                                setSelectedCollection(
                                    doc.collection_name
                                )
                            }
                        >
                            <div className="file-icon">📄</div>

                            <div className="file-details">
                                <h3>{doc.filename}</h3>

                                <p>
                                    Click to use this document for
                                    questions
                                </p>
                            </div>
                        </div>

                        <button
                            className="delete-btn"
                            onClick={() =>
                                handleDelete(doc.id)
                            }
                        >
                            Delete
                        </button>
                    </div>
                ))}
            </div>
        </section>
    );
}