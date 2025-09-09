// app/bread-meat-delivery-frontend/next.config.js
/** @type {import('next').NextConfig} */
const isDev = process.env.NODE_ENV !== 'production';
const API_BASE_URL = isDev
  ? 'http://127.0.0.1:8000'                 // dev local
  : (process.env.API_BASE_URL || 'http://backend:8000'); // Docker/Portainer

module.exports = {
  output: 'standalone',
  async rewrites() {
    return [
      // Evita 307 do FastAPI quando a chamada vier sem barra final
      { source: '/api/pedidos', destination: `${API_BASE_URL}/pedidos/` },
      // Regra genérica para o restante
      { source: '/api/:path*', destination: `${API_BASE_URL}/:path*` },
    ];
  },
};
