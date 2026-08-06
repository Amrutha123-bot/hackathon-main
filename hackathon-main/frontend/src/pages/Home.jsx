import UploadBox from "../components/UploadBox";
import DocumentList from "../components/DocumentList";

export default function Home({
    documents,
    selectedCollection,
    setSelectedCollection,
    refreshDocuments,
}) {
    return (
        <>
            <UploadBox
                refreshDocuments={refreshDocuments}
            />

            <DocumentList
                documents={documents}
                selectedCollection={selectedCollection}
                setSelectedCollection={setSelectedCollection}
                refreshDocuments={refreshDocuments}
            />
        </>
    );
}