import { useState } from "react";
import { supabase } from "../services/supabase";
import "./Login.css";

export default function Login({ onLogin }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");

    const handleLogin = async (e) => {
        e.preventDefault();

        if (!email || !password) {
            setMessage("Please enter email and password.");
            return;
        }

        try {
            setLoading(true);
            setMessage("");

            const { data, error } =
                await supabase.auth.signInWithPassword({
                    email,
                    password,
                });

            if (error) {
                throw error;
            }

            console.log("Logged in user:", data.user);

            onLogin(data.session);

        } catch (error) {
            console.error(error);
            setMessage(error.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-page">
            <div className="login-card">

                <h1>Insurance RAG Assistant</h1>

                <h2>Login</h2>

                <p>
                    Sign in to access your policy documents.
                </p>

                <form onSubmit={handleLogin}>

                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) =>
                            setEmail(e.target.value)
                        }
                    />

                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) =>
                            setPassword(e.target.value)
                        }
                    />

                    <button
                        type="submit"
                        disabled={loading}
                    >
                        {loading ? "Logging in..." : "Login"}
                    </button>

                </form>

                {message && (
                    <p className="login-message">
                        {message}
                    </p>
                )}

            </div>
        </div>
    );
}