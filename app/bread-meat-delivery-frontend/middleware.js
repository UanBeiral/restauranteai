// app/bread-meat-delivery-frontend/middleware.js
import { NextResponse } from 'next/server';

export function middleware(req) {
  const token = req.cookies.get('bm_token')?.value || null;
  const { pathname, search } = req.nextUrl;

  const isProtected = pathname.startsWith('/pedidos') || pathname.startsWith('/pedido');
  const isAuthRoute = pathname === '/login';

  if (isProtected && !token) {
    const url = req.nextUrl.clone();
    url.pathname = '/login';
    url.searchParams.set('next', pathname + search);
    return NextResponse.redirect(url);
  }

  if (isAuthRoute && token) {
    const next = req.nextUrl.searchParams.get('next') || '/pedidos';
    const url = req.nextUrl.clone();
    url.pathname = next; url.search = '';
    return NextResponse.redirect(url);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/pedidos/:path*', '/pedido/:path*', '/login'],
};
