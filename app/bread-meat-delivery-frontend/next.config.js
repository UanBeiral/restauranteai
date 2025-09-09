// app/bread-meat-delivery-frontend/next.config.js
/** @type {import('next').NextConfig} */
const isDev = process.env.NODE_ENV !== 'production';
const API_BASE_URL = isDev
  ? 'http://127.0.0.1:8000'                  // dev local
  : (process.env.API_BASE_URL || 'http://backend:8000'); // Docker/Portainer

const nextConfig = {
  output: 'standalone',
  async rewrites() {
    return [{ source: '/api/:path*', destination: `${API_BASE_URL}/:path*` }];
  },
};

module.exports = nextConfig;
