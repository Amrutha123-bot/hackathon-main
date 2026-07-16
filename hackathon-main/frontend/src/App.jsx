import "./App.css";
import Home from "./pages/Home";
import Chat from "./pages/Chat";

function App() {

    return (

        <div className="app">

            <header className="app-header">

                <h1>Insurance RAG Assistant</h1>

                <p>
                    📄 No documents uploaded yet.
                Upload a PDF, DOCX or TXT file to begin.
                </p>

            </header>

            <main>

                <Home />

                <Chat />

            </main>

        </div>

    );

}

export default App;