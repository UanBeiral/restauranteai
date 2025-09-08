// middleware.js
import { NextResponse } from "next/server";

export function middleware(req) {
  const { pathname } = req.nextUrl;

  // Rotas públicas: login, assets e proxy de API
  const isPublic =
    pathname.startsWith("/login") ||
    pathname.startsWith("/_next") ||
    pathname.startsWith("/favicon") ||
    pathname.startsWith("/api");

  if (isPublic) return NextResponse.next();

  // Autorizado se tiver o cookie bm_token
  const token = req.cookies.get("bm_token")?.value;
  if (token) return NextResponse.next();

  // Sem token -> manda para /login e guarda a rota desejada
  const url = req.nextUrl.clone();
  url.pathname = "/login";
  url.searchParams.set("from", pathname);
  return NextResponse.redirect(url);
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
