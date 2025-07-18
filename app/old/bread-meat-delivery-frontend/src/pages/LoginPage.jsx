import React, { useState } from "react";
import { supabase } from "../services/supabase";
import { useNavigate } from "react-router-dom";

function LoginPage() {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");
  const navigate = useNavigate();

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
      navigate("/pedidos");
    }
  };

  return (
    <div style={{ maxWidth: 320, margin: "50px auto" }}>
      <h2>Login</h2>
      <form onSubmit={login}>
        <input
          type="email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          placeholder="E-mail"
          required
          style={{ width: "100%", marginBottom: 8 }}
        />
        <input
          type="password"
          value={senha}
          onChange={e => setSenha(e.target.value)}
          placeholder="Senha"
          required
          style={{ width: "100%", marginBottom: 8 }}
        />
        <button type="submit" style={{ width: "100%" }}>Entrar</button>
      </form>
      {erro && <div style={{color:"red"}}>{erro}</div>}
    </div>
  );
}

export default LoginPage;
