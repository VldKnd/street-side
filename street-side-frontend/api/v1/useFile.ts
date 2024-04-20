import useSWR from "swr"
import { ADRESS, fetcher } from '@/api/constants';
import { DocumentInterface } from "@/app/types/document";

export default function useFileBase64(document: DocumentInterface) {
    const { data, error, isLoading } = useSWR(`${ADRESS}/v1/get_file_as_base64_by_document_hash_id/${document.hash_id}`, fetcher);

    if (
        isLoading || error
    ) return {
        fileBase64: null,
        isLoading,
        isError: error
    }

    return {
        fileBase64: data,
        isLoading,
        isError: error
    }
}
