import useSWR from "swr"
import { ADRESS, fetcher } from '@/api/constants';
import { CompanyInterface } from "@/app/types/company";

export default function useCompanyDocumentTypes(company: CompanyInterface) {
    const url = `${ADRESS}/v1/get_document_types_by_company_hash_id/${company.hash_id}`
    const { data, error, isLoading } = useSWR(url, fetcher);

    if (
        isLoading || error
    ) return {
        documentTypes: [],
        isLoading,
        isError: error
    }

    return {
        documentTypes: data,
        isLoading,
        isError: error
    }
}
