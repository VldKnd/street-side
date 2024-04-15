import { ADRESS } from "@/api/constants";

export function getSleep({ seconds }: { seconds: number }) {
    const API_QUERY = `${ADRESS}/v1/sleep/?` + new URLSearchParams({
        "seconds": `${seconds}`,
    })
    
    return fetch(API_QUERY,
        {
            method: "GET",
            cache: "no-cache",
        }
    );
}