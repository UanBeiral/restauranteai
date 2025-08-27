// app/pedidos/page.jsx
"use client";
import React, { useEffect, useState } from "react";
import Link from "next/link";
import api from "@/lib/api";

const STATUS_OPTIONS = [
  "solicitado",
  "em_preparo",
  "saiu_para_entrega",
  "entregue",
  "finalizado",
  "cancelado",
];

export default function OrdersPage() {
  const [pedidos, setPedidos] = useState([]);
  const [statusFiltro, setStatusFiltro] = useState("solicitado");
  const [dataFiltro, setDataFiltro] = useState(new Date().toISOString().slice(0, 10));
  const [salvandoId, setSalvandoId] = useState(null);
  const [erroId, setErroId] = useState(null);

  const carregar = async () => {
    try {
      const { data } = await api.get("/pedidos/", {
        params: { status: statusFiltro, data: dataFiltro },
      });
      setPedidos(Array.isArray(data) ? data : []);
    } catch {
      setPedidos([]);
    }
  };

  useEffect(() => {
    carregar();
  }, [statusFiltro, dataFiltro]);

  const alterarStatus = async (id, novoStatus) => {
    setErroId(null);
    // otimismo: atualiza local antes
    setPedidos((prev) => prev.map((p) => (p.id === id ? { ...p, status: novoStatus } : p)));
    setSalvandoId(id);
    try {
      await api.patch(`/pedidos/${id}/status`, { status: novoStatus });
    } catch (e) {
      setErroId(id);
      // rollback em caso de erro
      await carregar();
    } finally {
      setSalvandoId(null);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-4">
      <h2 className="text-xl font-bold mb-4">Pedidos</h2>

      <div className="flex gap-4 mb-4">
        <label className="flex items-center gap-2">
          <span>Data:</span>
          <input
            type="date"
            value={dataFiltro}
            onChange={(e) => setDataFiltro(e.target.value)}
            className="border px-2 py-1 rounded"
          />
        </label>

        <label className="flex items-center gap-2">
          <span>Status:</span>
          <select
            value={statusFiltro}
            onChange={(e) => setStatusFiltro(e.target.value)}
            className="border px-2 py-1 rounded"
          >
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

      <ul className="space-y-2">
        {pedidos.length === 0 ? (
          <li className="text-gray-400">Nenhum pedido encontrado.</li>
        ) : (
          pedidos.map((p) => (
            <li key={p.id} className="p-4 border rounded shadow">
              <div className="flex items-center justify-between">
                <div>
                  <div className="font-semibold">
                    #{p.id} — <span className="capitalize">{p.status}</span>
                  </div>
                  <div className="text-sm text-gray-600">
                    {(p.cliente ?? "Cliente")} • {(p.created_at_br ?? p.created_at ?? "")}
                  </div>
                  {p.total_br && <div className="text-sm mt-1">Total: {p.total_br}</div>}
                </div>

                <div className="flex items-center gap-2">
                  <select
                    value={p.status}
                    onChange={(e) => alterarStatus(p.id, e.target.value)}
                    className="border px-2 py-1 rounded"
                    disabled={salvandoId === p.id}
                  >
                    {STATUS_OPTIONS.map((s) => (
                      <option key={s} value={s}>
                        {s.replaceAll("_", " ")}
                      </option>
                    ))}
                  </select>

                  <Link
                    href={`/pedido/${p.id}`}
                    className="text-blue-600 underline whitespace-nowrap"
                  >
                    Ver detalhes
                  </Link>
                </div>
              </div>

              {erroId === p.id && (
                <div className="text-red-600 text-sm mt-2">
                  Não foi possível salvar o novo status.
                </div>
              )}
            </li>
          ))
        )}
      </ul>
    </div>
  );
}
