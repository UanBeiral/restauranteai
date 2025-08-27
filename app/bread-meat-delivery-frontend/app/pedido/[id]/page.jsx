// app/pedido/[id]/page.jsx
"use client";
import React, { useEffect, useState } from "react";
import api from "@/lib/api";
import { useParams, useRouter } from "next/navigation";

export default function OrderDetailPage() {
  const router = useRouter();
  const params = useParams();
  const id = params?.id;
  const [pedido, setPedido] = useState(null);
  const [erro, setErro] = useState("");

  useEffect(() => {
    const run = async () => {
      try {
        const { data } = await api.get(`/pedidos/${id}`);
        setPedido(data || null);
      } catch {
        setErro("Falha ao carregar o pedido.");
        setPedido(null);
      }
    };
    if (id) run();
  }, [id]);

  if (!pedido) {
    return (
      <div className="max-w-xl mx-auto p-4">
        <button className="mb-4 text-blue-600" onClick={() => router.back()}>
          Voltar
        </button>
        {erro ? <div className="text-red-600">{erro}</div> : "Carregando..."}
      </div>
    );
  }

  return (
    <div className="max-w-xl mx-auto p-4">
      <button className="mb-4 text-blue-600" onClick={() => router.back()}>
        Voltar
      </button>
      <h2 className="text-2xl font-bold mb-2">Pedido #{pedido.id}</h2>
      <div className="mb-1">Status: <span className="capitalize">{pedido.status}</span></div>
      <div className="mb-1">Data: {pedido.created_at_br ?? pedido.created_at ?? "-"}</div>
      <div className="mb-1">Total: {pedido.total_br ?? (pedido.total ?? "-")}</div>

      <h3 className="font-bold mt-6 mb-2">Itens</h3>
      <ul className="list-disc pl-5">
        {(pedido.order_items ?? []).length
          ? pedido.order_items.map((it, i) => (
              <li key={i}>
                {(it.name ?? it.nome ?? "Item")} x{(it.quantity ?? it.qtd ?? 1)} — {(it.price_br ?? it.preco_br ?? it.price ?? it.preco ?? "")}
              </li>
            ))
          : <li>Nenhum item.</li>}
      </ul>
    </div>
  );
}
