import type { NextConfig } from "next";

const nextConfig: NextConfig = {
    /* config options here */
    reactStrictMode: true,
    rewrites: async () => {
        return [
            {
                source: "/api/py/:path*",
                destination:
                    process.env.NODE_ENV === "development"
                        ? "http://127.0.0.1:8000/api/py/:path*"
                        : "/api/",
            },
        ];
    },
};

export default nextConfig;
