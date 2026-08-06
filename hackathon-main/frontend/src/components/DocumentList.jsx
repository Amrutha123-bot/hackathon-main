import { deleteDocument } from "../services/api";
import "./DocumentList.css";

export default function DocumentList({
    documents,
    selectedCollection,
    setSelectedCollection,
    refreshDocuments,
}) {

    const handleDelete = async (collectionName) => {

        const confirmDelete = window.confirm(
            "Are you sure you want to delete this knowledge base?"
        );

        if (!confirmDelete) return;

        try {

            await deleteDocument(collectionName);

            await refreshDocuments();

        } catch (error) {

            console.error(error);

            alert(error.message);

        }

    };

    if (documents.length === 0) {

        return (
            <div className="document-list empty">
                <h2>Knowledge Bases</h2>
                <p>No uploaded documents.</p>
            </div>
        );

    }

    return (

        <div className="document-list">

            <h2>Knowledge Bases</h2>

            {

                documents.map((doc) => (

                    <div
                        key={doc.collection_name}
                        className={
                            selectedCollection === doc.collection_name
                                ? "document-card active"
                                : "document-card"
                        }
                    >

                        <div
                            className="document-info"
                            onClick={() =>
                                setSelectedCollection(doc.collection_name)
                            }
                        >

                            <h3>{doc.document_name}</h3>

                            <p>
                                Collection:
                                <br />
                                <small>{doc.collection_name}</small>
                            </p>

                        </div>

                        <button
                            className="delete-btn"
                            onClick={() =>
                                handleDelete(doc.collection_name)
                            }
                        >
                            Delete
                        </button>

                    </div>

                ))

            }

        </div>

    );

}