import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function OrdersPage() {
  const [pedidos, setPedidos] = useState([]);
  const [statusFiltro, setStatusFiltro] = useState("solicitado");
  const [dataFiltro, setDataFiltro] = useState(new Date().toISOString().slice(0,10));
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchPedidos() {
      const token = localStorage.getItem("sbtoken");
      if (!token) { navigate("/login"); return; }
      const resp = await axios.get("http://localhost:8000/pedidos", {
        headers: { Authorization: `Bearer ${token}` },
        params: { status: statusFiltro, data: dataFiltro }
      });
      setPedidos(resp.data);
    }
    fetchPedidos();
  }, [statusFiltro, dataFiltro, navigate]);

  return (
    <div>
      <h2>Pedidos</h2>
      <label>Data: <input type="date" value={dataFiltro} onChange={e=>setDataFiltro(e.target.value)}/></label>
      <label>
        Status:
        <select value={statusFiltro} onChange={e=>setStatusFiltro(e.target.value)}>
          <option value="solicitado">Solicitado</option>
          <option value="em_preparo">Em preparo</option>
          <option value="saiu_para_entrega">Saiu para entrega</option>
          <option value="entregue">Entregue</option>
          <option value="finalizado">Finalizado</option>
          <option value="cancelado">Cancelado</option>
          <option value="">Todos</option>
        </select>
      </label>
      <ul>
        {pedidos.length === 0 ? (
          <li>Nenhum pedido encontrado.</li>
        ) : pedidos.map(pedido => (
          <li key={pedido.id} onClick={() => navigate(`/pedido/${pedido.id}`)} style={{cursor:'pointer',margin:8,padding:8,border:'1px solid #ddd',borderRadius:6}}>
            <b># {pedido.id}</b> - {pedido.cliente} - {pedido.status}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default OrdersPage;
