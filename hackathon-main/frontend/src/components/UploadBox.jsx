import { useState } from "react";
import { uploadDocuments } from "../services/api";
import "./UploadBox.css";

export default function UploadBox({ refreshDocuments }) {
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
            setMessage("");

            console.log(
                "Uploading files:",
                files.map((file) => file.name)
            );

            const response = await uploadDocuments(files);

            console.log("Upload response:", response);

            setMessage(
                response.message || "Documents uploaded successfully."
            );

            // Clear selected files from the file input
            setFiles([]);

            // Refresh the document list from backend/Supabase
            await refreshDocuments();

        } catch (error) {
            console.error("Upload error:", error);

            setMessage(
                error.message || "Failed to upload documents."
            );
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
                disabled={loading}
            />

            {files.length > 0 && (
                <div className="selected-files">
                    <h3>
                        Selected Files ({files.length})
                    </h3>

                    {files.map((file, index) => (
                        <div
                            key={`${file.name}-${index}`}
                            className="file-item"
                        >
                            📄 {file.name}
                        </div>
                    ))}
                </div>
            )}

            <button
                onClick={handleUpload}
                disabled={loading || files.length === 0}
            >
                {loading
                    ? "Uploading..."
                    : "Upload Documents"}
            </button>

            {message && (
                <p className="status">
                    {message}
                </p>
            )}
        </div>
    );
}