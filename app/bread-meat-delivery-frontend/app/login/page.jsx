// app/login/page.jsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const [code, setCode] = useState("");
  const [err, setErr] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function handleSubmit(e) {
    e.preventDefault();
    setErr("");
    setLoading(true);
    try {
      const res = await fetch(`/api/auth/verify`, {
        method: "POST",
        credentials: "include",      // mantém, agora é same-origin
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });

      if (!res.ok) {
        setErr("Código inválido.");
        return;
      }

      router.push("/"); // troque para "/pedidos" se quiser cair direto na lista
    } catch (e) {
      setErr("Falha ao conectar. Tente novamente.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ minHeight: "100svh", display: "grid", placeItems: "center", background: "#f6f7f9" }}>
      <form onSubmit={handleSubmit} style={{ width: 360, background: "#fff", padding: 24, borderRadius: 12, boxShadow: "0 6px 30px rgba(0,0,0,.08)" }}>
        <h1 style={{ fontSize: 20, fontWeight: 700, marginBottom: 16 }}>Entrar</h1>
        <label style={{ fontSize: 12, color: "#555" }}>Código de acesso</label>
        <input
          placeholder="Digite o código"
          autoFocus
          value={code}
          onChange={(e) => setCode(e.target.value)}
          style={{ width: "100%", border: "1px solid #ddd", borderRadius: 8, padding: "10px 12px", marginTop: 6, marginBottom: 12 }}
        />
        {err && <p style={{ color: "#c00", fontSize: 12, marginBottom: 8 }}>{err}</p>}
        <button
          type="submit"
          disabled={loading}
          style={{ width: "100%", border: 0, background: "#111", color: "#fff", borderRadius: 8, padding: "10px 12px", cursor: "pointer", opacity: loading ? 0.7 : 1 }}
        >
          {loading ? "Verificando..." : "Acessar"}
        </button>
      </form>
    </div>
  );
}
