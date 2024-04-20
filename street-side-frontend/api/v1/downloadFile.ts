import useSWR from "swr"
import { ADRESS, fetcher } from '@/api/constants';
import { DocumentInterface } from "@/app/types/document";


export default function downloadFile(document: DocumentInterface): { documents: DocumentInterface[], isLoading: boolean, isError: boolean } {
    const url = `${ADRESS}/v1/download_file/${document.hash_id}`
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
