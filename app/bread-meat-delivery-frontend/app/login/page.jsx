"use client";
import React, { useState } from "react";
import { supabase } from "@/lib/supabase";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");
  const router = useRouter();

  const login = async (e) => {
    e.preventDefault();
    setErro("");
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
      setErro("E-mail inválido");
      return;
    }
    const { data, error } = await supabase.auth.signInWithPassword({ email, password: senha });
    if (error) {
      setErro("Login inválido");
    } else {
      localStorage.setItem("sbtoken", data.session.access_token);
      router.push("/pedidos");
    }
  };

  return (
    <div className="max-w-xs mx-auto mt-20">
      <h2 className="text-2xl font-bold mb-4">Login</h2>
      <form onSubmit={login} className="space-y-2">
        <input
          type="email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          placeholder="E-mail"
          required
          className="w-full border px-2 py-1 rounded"
        />
        <input
          type="password"
          value={senha}
          onChange={e => setSenha(e.target.value)}
          placeholder="Senha"
          required
          className="w-full border px-2 py-1 rounded"
        />
        <button type="submit" className="w-full bg-black text-white py-2 rounded">Entrar</button>
      </form>
      {erro && <div className="text-red-500">{erro}</div>}
    </div>
  );
}
