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
        throw new Error("Failed to upload documents.");
    }

    return await response.json();
}

/**
 * Ask a question
 */
export async function askQuestion(question) {

    const response = await fetch(`${BASE_URL}/ask`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json",
        },

        body: JSON.stringify({
            question: question,
        }),
    });

    if (!response.ok) {
        throw new Error("Failed to get response.");
    }

    return await response.json();
}