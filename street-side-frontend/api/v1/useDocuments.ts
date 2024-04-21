import useSWR from "swr"
import { ADRESS, fetcher } from '@/api/constants';
import { DocumentTypeInterface } from "@/app/types/document_type";
import { DocumentInterface } from "@/app/types/document";

interface useDocumentInterface {
    documents: DocumentInterface[],
    isLoading: boolean,
    isError : boolean
}

export default function useDocuments(document_type: DocumentTypeInterface): useDocumentInterface {
    const url = `${ADRESS}/v1/get_documents_by_document_type_hash_id/${document_type.hash_id}`
    const { data, error, isLoading } = useSWR(url, fetcher);

    if (
        isLoading || error
    ) return {
        documents: [],
        isLoading,
        isError: error
    }

    return {
        documents: data,
        isLoading,
        isError: error
    }
}
