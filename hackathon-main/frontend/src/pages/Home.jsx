import UploadBox from "../components/UploadBox";
import DocumentList from "../components/DocumentList";

export default function Home({
    documents,
    selectedDocumentIds,
    setSelectedDocumentIds,
    refreshDocuments,
}) {
    return (
        <>
            <UploadBox
                refreshDocuments={refreshDocuments}
                setSelectedDocumentIds={setSelectedDocumentIds}
            />

            <DocumentList
                documents={documents}
                selectedDocumentIds={selectedDocumentIds}
                setSelectedDocumentIds={setSelectedDocumentIds}
                refreshDocuments={refreshDocuments}
            />
        </>
    );
}