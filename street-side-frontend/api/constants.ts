export const HOST = "http://localhost";
export const PORT = "8080";
export const ADRESS = `${HOST}:${PORT}`;
export type fetchWithBodyInterface = [input: RequestInfo | URL, init?: RequestInit ]
export const fetcher = (input: RequestInfo | URL, init?: RequestInit) => fetch(input, init).then(res => res.json())
