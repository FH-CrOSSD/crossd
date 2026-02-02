import { dev } from '$app/environment';
import { env } from '$env/dynamic/private';
import type { Handle } from '@sveltejs/kit';

if (dev) {
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";
}
import { Database, aql } from "arangojs";

export const db = new Database({
    url: env.ARANGO_URL,
    databaseName: "crossd",
    auth: { username: env.FRONTEND_USER ?? "", password: env.FRONTEND_PASSWORD },
    agentOptions: {
        // disable https hostname verification in development environment
        rejectUnauthorized: dev ? false : true
    },
    rejectUnauthorized: dev ? false : true
});

export const handle: Handle = async ({ resolve, event }) => {
    console.log(event.url.pathname);
    // Apply CORS header for API routes
    if (event.url.pathname.startsWith('/api')) {
        // Required for CORS to work
        if (event.request.method === 'OPTIONS') {
            return new Response(null, {
                headers: {
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': '*',
                }
            });
        }

    }

    const response = await resolve(event);
    if (event.url.pathname.startsWith('/api')) {
        response.headers.append('Access-Control-Allow-Origin', '*');
        response.headers.append('Vary', '*');
    }
    return response;
};
