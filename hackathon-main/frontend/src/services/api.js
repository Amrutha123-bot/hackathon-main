// const BASE_URL = import.meta.env.VITE_API_URL;
const BASE_URL = "http://127.0.0.1:8000";

/**
 * Upload multiple documents
 */
export async function uploadDocuments(files) {
    const formData = new FormData();

    for (const file of files) {
        formData.append("files", file);
    }

    const response = await fetch(`${BASE_URL}/upload`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Failed to upload documents.");
    }

    return await response.json();
}

/**
 * Get all uploaded knowledge bases
 */
export async function getDocuments() {
    const response = await fetch(`${BASE_URL}/documents`);

    if (!response.ok) {
        throw new Error("Failed to fetch documents.");
    }

    return await response.json();
}

/**
 * Delete a knowledge base
 */
export async function deleteDocument(collectionName) {
    const response = await fetch(
        `${BASE_URL}/documents/${collectionName}`,
        {
            method: "DELETE",
        }
    );

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Failed to delete document.");
    }

    return await response.json();
}

/**
 * Ask a question
 */
export async function askQuestion(question, collectionName) {
    const response = await fetch(`${BASE_URL}/ask`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            question,
            collection_name: collectionName,
        }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Failed to get response.");
    }

    return await response.json();
}