import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'standalone',
  images: {
    domains: ['localhost', 'res.cloudinary.com'],
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001',
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  async rewrites() {
    const apiBaseUrl = process.env.INTERNAL_API_URL || 'http://api:8001';
    console.log(`[Next.js] Configuring rewrites targeting API at: ${apiBaseUrl}`);
    return [
      {
        source: '/api/:path*',
        destination: `${apiBaseUrl}/api/:path*/`,
      },
    ];
  },
};

export default nextConfig;
