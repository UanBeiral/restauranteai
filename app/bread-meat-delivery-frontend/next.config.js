// app/bread-meat-delivery-frontend/next.config.js
/** @type {import('next').NextConfig} */
const isDev = process.env.NODE_ENV !== 'production';
const API_BASE_URL = isDev
  ? 'http://127.0.0.1:8000'
  : (process.env.API_BASE_URL || 'http://backend:8000');

module.exports = {
  output: 'standalone',
  async rewrites() {
    return [
      { source: '/api/pedidos', destination: `${API_BASE_URL}/pedidos/` }, // evita 307
      { source: '/api/:path*', destination: `${API_BASE_URL}/:path*` },
    ];
  },
};
