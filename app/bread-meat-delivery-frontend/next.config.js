// ✅ Opção A — next.config.js (CommonJS)
 /** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://127.0.0.1:8000/:path*', // mantém o path
      },
    ];
  },
};

module.exports = nextConfig;
