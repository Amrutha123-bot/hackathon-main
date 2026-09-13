import { useState } from "react";
import { supabase } from "../services/supabase";
import "./Login.css";

export default function Login({ onLogin }) {
    const [isSignUp, setIsSignUp] = useState(false);

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!email || !password) {
            setMessage("Please enter email and password.");
            return;
        }

        try {
            setLoading(true);
            setMessage("");

            if (isSignUp) {
                const { data, error } =
                    await supabase.auth.signUp({
                        email,
                        password,
                    });

                if (error) {
                    throw error;
                }

                if (data.session) {
                    onLogin(data.session);
                } else {
                    setMessage(
                        "Account created! Please check your email to confirm your account."
                    );
                }
            } else {
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
            }
        } catch (error) {
            console.error(error);
            setMessage(error.message);
        } finally {
            setLoading(false);
        }
    };

    const toggleMode = () => {
        setIsSignUp((previous) => !previous);
        setMessage("");
        setEmail("");
        setPassword("");
    };

    return (
        <div className="login-page">
            <div className="login-card">

                <div className="login-brand">
                    <h1>Insurance RAG Assistant</h1>
                    <p>
                        Your private policy document assistant
                    </p>
                </div>

                <div className="login-heading">
                    <h2>
                        {isSignUp
                            ? "Create Account"
                            : "Welcome back"}
                    </h2>

                    <p>
                        {isSignUp
                            ? "Create an account to manage your policy documents."
                            : "Sign in to access your policy documents."}
                    </p>
                </div>

                <form onSubmit={handleSubmit}>

                    <div className="input-group">
                        <label htmlFor="email">
                            Email
                        </label>

                        <input
                            id="email"
                            type="email"
                            placeholder="Enter your email"
                            value={email}
                            onChange={(e) =>
                                setEmail(e.target.value)
                            }
                        />
                    </div>

                    <div className="input-group">
                        <label htmlFor="password">
                            Password
                        </label>

                        <input
                            id="password"
                            type="password"
                            placeholder="Enter your password"
                            value={password}
                            onChange={(e) =>
                                setPassword(e.target.value)
                            }
                        />
                    </div>

                    <button
                        className="submit-btn"
                        type="submit"
                        disabled={loading}
                    >
                        {loading
                            ? isSignUp
                                ? "Creating Account..."
                                : "Logging in..."
                            : isSignUp
                                ? "Create Account"
                                : "Login"}
                    </button>

                </form>

                {message && (
                    <p className="login-message">
                        {message}
                    </p>
                )}

                <div className="auth-switch">
                    <span>
                        {isSignUp
                            ? "Already have an account?"
                            : "Don't have an account?"}
                    </span>

                    <button
                        type="button"
                        className="switch-btn"
                        onClick={toggleMode}
                    >
                        {isSignUp
                            ? "Login"
                            : "Sign Up"}
                    </button>
                </div>

            </div>
        </div>
    );
}