import { ADRESS, fetcher } from "@/api/constants";
import useSWR from 'swr'

export function listDocuments(company_name : string) {
    const API_QUERY =  `${ADRESS}/v1/list_company_documents_names/${company_name}`
    const { data, error, isLoading } = useSWR(API_QUERY, fetcher)

    return {
        document_names: data,
        isLoading,
        error: error
    }
}