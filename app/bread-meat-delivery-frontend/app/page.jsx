// app/bread-meat-delivery-frontend/app/page.jsx
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';

export default async function Home() {
  // Next 14/15: cookies() é assíncrono
  const cookieStore = await cookies();
  const hasToken = !!cookieStore.get('bm_token');

  // Envia para /pedidos se logado; caso contrário, /login
  redirect(hasToken ? '/pedidos' : '/login');
}
