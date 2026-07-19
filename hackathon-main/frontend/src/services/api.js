// const BASE_URL = import.meta.env.VITE_API_URL;
const BASE_URL = "http://127.0.0.1:8000"

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
        throw new Error("Failed to upload documents.");
    }

    const data = await response.json();

    // Save the collection name returned by the backend
    localStorage.setItem("collection_name", data.collection_name);

    return data;
}

/**
 * Ask a question
 */
export async function askQuestion(question) {

    // Read the saved collection name
    const collectionName = localStorage.getItem("collection_name");

    const response = await fetch(`${BASE_URL}/ask`, {
        method: "POST",

        headers: {
            "Content-Type": "application/json",
        },

        body: JSON.stringify({
            question: question,
            collection_name: collectionName,
        }),
    });

    if (!response.ok) {
        throw new Error("Failed to get response.");
    }

    return await response.json();
}