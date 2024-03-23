import { ADRESS } from "@/api/constants";

export async function getName() {
    return await fetch(`${ADRESS}/v1/name`, {
        method: "GET"
    });
}