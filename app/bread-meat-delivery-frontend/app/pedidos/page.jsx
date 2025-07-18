"use client";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";

export default function OrdersPage() {
  const [pedidos, setPedidos] = useState([]);
  const [statusFiltro, setStatusFiltro] = useState("solicitado");
  const [dataFiltro, setDataFiltro] = useState(new Date().toISOString().slice(0,10));
  const router = useRouter();

  useEffect(() => {
    async function fetchPedidos() {
      const token = localStorage.getItem("sbtoken");
      if (!token) { router.push("/login"); return; }
      try {
        const resp = await axios.get("http://localhost:8000/pedidos", {
          headers: { Authorization: `Bearer ${token}` },
          params: { status: statusFiltro, data: dataFiltro }
        });
        setPedidos(resp.data);
      } catch (e) {
        setPedidos([]);
      }
    }
    fetchPedidos();
  }, [statusFiltro, dataFiltro, router]);

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h2 className="text-xl font-bold mb-4">Pedidos</h2>
      <div className="flex gap-4 mb-4">
        <label>
          Data: <input type="date" value={dataFiltro} onChange={e=>setDataFiltro(e.target.value)} className="border px-2 py-1 rounded"/>
        </label>
        <label>
          Status:
          <select value={statusFiltro} onChange={e=>setStatusFiltro(e.target.value)} className="border px-2 py-1 rounded">
            <option value="solicitado">Solicitado</option>
            <option value="em_preparo">Em preparo</option>
            <option value="saiu_para_entrega">Saiu para entrega</option>
            <option value="entregue">Entregue</option>
            <option value="finalizado">Finalizado</option>
            <option value="cancelado">Cancelado</option>
            <option value="">Todos</option>
          </select>
        </label>
      </div>
      <ul>
        {pedidos.length === 0 ? (
          <li className="text-gray-400">Nenhum pedido encontrado.</li>
        ) : pedidos.map(pedido => (
          <li key={pedido.id} onClick={() => router.push(`/pedido/${pedido.id}`)}
              className="cursor-pointer mb-2 p-4 border rounded shadow hover:bg-gray-100">
            <b># {pedido.id}</b> - {pedido.cliente} - <span className="capitalize">{pedido.status}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
