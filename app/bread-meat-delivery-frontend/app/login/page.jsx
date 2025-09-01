"use client";
import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { supabase } from "@/lib/supabase";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");
  const [loading, setLoading] = useState(false);

  const onSubmit = async (e) => {
    e.preventDefault();
    setErro("");
    setLoading(true);
    try {
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password: senha,
      });
      if (error) throw error;
      localStorage.setItem("sbtoken", data.session.access_token);
      router.push("/pedidos");
    } catch (err) {
      setErro("Login inválido");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <form onSubmit={onSubmit} className="w-full max-w-sm border rounded p-6 shadow">
        <h1 className="text-xl font-bold mb-4">Login do Restaurante</h1>
        <label className="block mb-2">
          <span>Email</span>
          <input
            type="email"
            className="mt-1 w-full border px-3 py-2 rounded"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </label>
        <label className="block mb-4">
          <span>Senha</span>
          <input
            type="password"
            className="mt-1 w-full border px-3 py-2 rounded"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            required
          />
        </label>
        {erro && <div className="text-red-600 mb-3">{erro}</div>}
        <button
          type="submit"
          className="w-full bg-black text-white px-4 py-2 rounded disabled:opacity-50"
          disabled={loading}
        >
          {loading ? "Entrando..." : "Entrar"}
        </button>
      </form>
    </div>
  );
}
