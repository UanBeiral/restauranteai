// app/bread-meat-delivery-frontend/app/page.jsx
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';

export default function Home() {
  const hasToken = !!cookies().get('bm_token');
  redirect(hasToken ? '/pedidos' : '/login');
}
