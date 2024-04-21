import useSWR from "swr"
import { ADRESS, fetcher } from '@/api/constants';
import { CompanyInterface } from "@/app/types/company";
import { DocumentTypeInterface } from "@/app/types/document_type"

interface useDocumentTypeInterface {
    documentTypes: DocumentTypeInterface[],
    isLoading: boolean,
    isError : boolean
}

export default function useCompanyDocumentTypes(company: CompanyInterface): useDocumentTypeInterface {
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
