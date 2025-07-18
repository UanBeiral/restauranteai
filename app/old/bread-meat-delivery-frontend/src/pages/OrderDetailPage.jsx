import React, { useEffect, useState } from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";

function OrderDetailPage() {
  const { id } = useParams();
  const [pedido, setPedido] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchPedido() {
      const token = localStorage.getItem("sbtoken");
      if (!token) { navigate("/login"); return; }
      const resp = await axios.get(`http://localhost:8000/pedidos`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      const found = resp.data.find(p => String(p.id) === String(id));
      setPedido(found || null);
    }
    fetchPedido();
  }, [id, navigate]);
  if (!pedido) return <div>Carregando...</div>;
  return (
    <div>
      <button onClick={()=>navigate(-1)}>Voltar</button>
      <h2>Pedido #{pedido.id}</h2>
      <div>Cliente: {pedido.cliente}</div>
      <div>Status: {pedido.status}</div>
      <div>Endereço: {pedido.endereco}</div>
      <div>Total: R$ {pedido.total}</div>
      {/* Exemplo de itens */}
      <h3>Itens:</h3>
      <ul>
        {pedido.itens ? pedido.itens.map((item,i)=>
          <li key={i}>{item.nome} x{item.qtd} - R$ {item.preco}</li>
        ) : <li>Nenhum item.</li>}
      </ul>
    </div>
  );
}

export default OrderDetailPage;
