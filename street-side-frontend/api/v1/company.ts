import { ADRESS, fetcher } from "@/api/constants";
import useSWR from 'swr'

export function listCompanies() {
    const API_QUERY = `${ADRESS}/v1/list_companies`
    const { data, error, isLoading } = useSWR(API_QUERY, fetcher)

    return {
        companies: data,
        isLoading,
        error: error
    }
}