export const HOST = process.env.API_HOST;
export const PORT = process.env.API_PORT;
export const ADRESS = `${HOST}:${PORT}`;
export type fetchWithBodyInterface = [input: RequestInfo | URL, init?: RequestInit ]
export const fetcher = (input: RequestInfo | URL, init?: RequestInit) => fetch(input, init).then(res => res.json())
