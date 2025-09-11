// app/bread-meat-delivery-frontend/app/pedido/[id]/page.jsx
import { headers } from 'next/headers';

const moneyBR = (v) =>
  new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' })
    .format(Number(v ?? 0));

async function getPedido(id) {
  // Next 14/15: headers() é assíncrono
  const h = await headers();
  const host = h.get('host');
  const proto = h.get('x-forwarded-proto') || 'http';
  const base = `${proto}://${host}`;
  const cookie = h.get('cookie') ?? '';

  // SSR: URL absoluta + encaminhar o cookie para passar pelo rewrite (/api)
  const res = await fetch(`${base}/api/pedidos/${id}`, {
    headers: { cookie },
    cache: 'no-store',
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Falha ao carregar pedido #${id}: ${res.status} ${text}`);
  }
  return res.json();
}

export default async function PedidoPage({ params }) {
  const id = params?.id;
  const pedido = await getPedido(id);

  const titulo = `Pedido #${pedido?.id ?? id}`;
  const status = pedido?.status ?? '';
  const dataBR = pedido?.created_at_br ?? '';
  const totalStr = pedido?.total_br ?? (pedido?.total != null ? moneyBR(pedido.total) : '');

  // order_items já possui item_name e item_total (calculado no BD)
  const itens = Array.isArray(pedido?.order_items) ? pedido.order_items : [];

  return (
    <main className="max-w-2xl mx-auto p-6 space-y-4">
      <h1 className="text-2xl font-semibold">{titulo}</h1>

      <div className="grid grid-cols-2 gap-2">
        <div>
          <span className="text-gray-500">Status:</span>{' '}
          <span className="font-medium">{status}</span>
        </div>
        <div>
          <span className="text-gray-500">Data:</span>{' '}
          <span className="font-medium">{dataBR}</span>
        </div>
        <div className="col-span-2">
          <span className="text-gray-500">Total:</span>{' '}
          <span className="font-medium">{totalStr}</span>
        </div>
      </div>

      <section className="mt-4">
        <h2 className="text-lg font-medium mb-2">Itens</h2>
        {itens.length === 0 ? (
          <p className="text-gray-500">Nenhum item neste pedido.</p>
        ) : (
          <ul className="space-y-2">
            {itens.map((it, idx) => {
              const name = it?.item_name ?? it?.name ?? `Item ${idx + 1}`;
              const qty = it?.quantity ?? 1;
              // item_total vem do BD; se o backend já formatar, usar item_total_br
              const totalItemStr =
                it?.item_total_br ??
                (it?.item_total != null ? moneyBR(it.item_total) : moneyBR(0));

              return (
                <li
                  key={it?.id ?? idx}
                  className="flex items-center justify-between border rounded-lg p-3"
                >
                  <div className="truncate">
                    <span className="font-medium">{name}</span>
                    <span className="text-gray-500"> × {qty}</span>
                  </div>
                  <div className="font-semibold">{totalItemStr}</div>
                </li>
              );
            })}
          </ul>
        )}
      </section>
    </main>
  );
}
