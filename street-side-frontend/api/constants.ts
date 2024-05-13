export const ADRESS = process.env.NEXT_PUBLIC_API_ADRESS;
export type fetchWithBodyInterface = [input: RequestInfo | URL, init?: RequestInit ]
export const fetcher = (input: RequestInfo | URL, init?: RequestInit) => fetch(input, init).then(res => res.json())
