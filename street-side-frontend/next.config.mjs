/** @type {import('next').NextConfig} */
const nextConfig = {
    webpack: (config) => {
        config.resolve.alias.canvas = false;
        return config;
    },
    env: {
      userName: process.env.userName,
    },
};

export default nextConfig;
