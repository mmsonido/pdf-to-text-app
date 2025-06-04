import { useState } from "react";
import axios from "axios";

// Asegúrate de que coincida con tu .env: VITE_API_URL=http://localhost:8000
const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
  const [file, setFile] = useState(null);
  const [text, setText] = useState("");
  const [msg, setMsg] = useState("");

  const onChange = (e) => {
    setFile(e.target.files[0]);
    setText("");
    setMsg("");
  };

  const onUpload = async () => {
    if (!file) return setMsg("Selecciona un PDF primero.");
    setMsg("Subiendo…");
    const form = new FormData();
    form.append("file", file);

    try {
      const res = await axios.post(`${API}/api/v1/upload`, form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setText(res.data.text);
      setMsg("¡Listo!");
    } catch {
      setMsg("Error al subir el archivo.");
    }
  };

  return (
    <div
      style={{
        maxWidth: 800,
        margin: "3rem auto",
        fontFamily: "sans-serif",
        fontSize: "1.5rem",
        lineHeight: 1.5,
        padding: "1rem",
      }}
    >
      <h1 style={{ fontSize: "2rem" }}>PDF → Texto</h1>
      <input
        type="file"
        accept="application/pdf"
        onChange={onChange}
        style={{ fontSize: "1.3rem", padding: "0.5rem" }}
      />
      <button
        onClick={onUpload}
        style={{ marginLeft: 8, fontSize: "1.3rem", padding: "0.5rem 1rem" }}
      >
        Subir y extraer
      </button>
      <p>{msg}</p>
      {text && (
        <textarea
          readOnly
          value={text}
          rows={20}
          style={{
            width: "100%",
            marginTop: 16,
            fontSize: "1.3rem",
            padding: "0.5rem",
          }}
        />
      )}
    </div>
  );
}

export default App;