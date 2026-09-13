import { deleteDocument } from "../services/api";
import "./DocumentList.css";

export default function DocumentList({
    documents,
    selectedDocumentIds,
    setSelectedDocumentIds,
    refreshDocuments,
}) {
    const handleDelete = async (documentId) => {
        const confirmDelete = window.confirm(
            "Are you sure you want to delete this document?"
        );

        if (!confirmDelete) return;

        try {
            await deleteDocument(documentId);

            // Remove deleted document from selection
            setSelectedDocumentIds((previous) =>
                previous.filter((id) => id !== documentId)
            );

            await refreshDocuments();
        } catch (error) {
            console.error(error);
            alert(error.message);
        }
    };

    const handleSelect = (documentId) => {
        setSelectedDocumentIds((previous) => {
            if (previous.includes(documentId)) {
                return previous.filter((id) => id !== documentId);
            }

            return [...previous, documentId];
        });
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
                        Select one or more documents to use for
                        questions.
                    </p>
                </div>

                <div>
                    <strong>
                        {selectedDocumentIds.length}
                    </strong>{" "}
                    selected
                </div>
            </div>

            <div className="documents-grid">
                {documents.map((doc) => {
                    const isSelected =
                        selectedDocumentIds.includes(doc.id);

                    return (
                        <div
                            key={doc.id}
                            className={
                                isSelected
                                    ? "document-card active"
                                    : "document-card"
                            }
                        >
                            <div
                                className="document-info"
                                onClick={() =>
                                    handleSelect(doc.id)
                                }
                            >
                                <input
                                    type="checkbox"
                                    checked={isSelected}
                                    onChange={() =>
                                        handleSelect(doc.id)
                                    }
                                    onClick={(event) =>
                                        event.stopPropagation()
                                    }
                                />

                                <div className="file-icon">
                                    📄
                                </div>

                                <div className="file-details">
                                    <h3>{doc.filename}</h3>

                                    <p>
                                        {isSelected
                                            ? "Selected for questions"
                                            : "Click to select"}
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
                    );
                })}
            </div>
        </section>
    );
}