import { ADRESS } from "@/api/constants";

export async function getHealth() {
    return await fetch(`${ADRESS}/health`, {
        method: "GET"
    });
}