import { supabase } from "./supabase";

const BASE_URL = "https://hackathon-main-6.onrender.com";

/**
 * Get the current user's access token
 */
async function getAccessToken() {
    const {
        data: { session },
    } = await supabase.auth.getSession();

    if (!session) {
        throw new Error("You are not logged in.");
    }

    return session.access_token;
}

/**
 * Upload multiple documents
 */
export async function uploadDocuments(files) {
    const token = await getAccessToken();

    const formData = new FormData();

    for (const file of files) {
        formData.append("files", file);
    }

    const response = await fetch(`${BASE_URL}/upload`, {
        method: "POST",
        headers: {
            Authorization: `Bearer ${token}`,
        },
        body: formData,
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(
            error.detail || "Failed to upload documents."
        );
    }

    return await response.json();
}

/**
 * Get all uploaded documents
 */
export async function getDocuments() {
    const token = await getAccessToken();

    const response = await fetch(`${BASE_URL}/documents`, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(
            error.detail || "Failed to fetch documents."
        );
    }

    return await response.json();
}

/**
 * Delete an individual document
 */
export async function deleteDocument(documentId) {
    const token = await getAccessToken();

    const response = await fetch(
        `${BASE_URL}/documents/file/${documentId}`,
        {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
    );

    if (!response.ok) {
        const error = await response.json();
        throw new Error(
            error.detail || "Failed to delete document."
        );
    }

    return await response.json();
}

/**
 * Ask a question
 */
export async function askQuestion(question, collectionName) {
    const token = await getAccessToken();

    const response = await fetch(`${BASE_URL}/ask`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
            question,
            collection_name: collectionName,
        }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(
            error.detail || "Failed to get response."
        );
    }

    return await response.json();
}