import { useState } from "react";
import { uploadDocuments } from "../services/api";
import "./UploadBox.css";

export default function UploadBox({ refreshDocuments, setSelectedCollection }) {
    const [files, setFiles] = useState([]);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");

    const handleFileChange = (e) => {
        setFiles(Array.from(e.target.files));
        setMessage(""); 
    };

    const handleUpload = async () => {
        if (files.length === 0) {
            setMessage("Please select at least one document.");
            return;
        }

        try {
            setLoading(true);

            const response = await uploadDocuments(files);

            setMessage(response.message);

            setFiles([]);

            // Refresh document list
            await refreshDocuments();
            setSelectedCollection(response.collection_name);
        } catch (error) {
            console.error(error);
            setMessage(error.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="upload-card">
            <h2>Upload Documents</h2>

            <p className="subtitle">
                Supported formats: PDF, DOCX and TXT
            </p>

            <input
                type="file"
                multiple
                accept=".pdf,.docx,.txt"
                onChange={handleFileChange}
            />

            {files.length > 0 && (
                <div className="selected-files">
                    <h3>Selected Files</h3>

                    {files.map((file, index) => (
                        <div key={index} className="file-item">
                            📄 {file.name}
                        </div>
                    ))}
                </div>
            )}

            <button
                onClick={handleUpload}
                disabled={loading}
            >
                {loading ? "Uploading..." : "Upload Documents"}
            </button>

            {message && (
                <p className="status">
                    {message}
                </p>
            )}
        </div>
    );
}