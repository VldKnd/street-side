import useSWR from "swr"
import { ADRESS, fetcher } from '@/api/constants';

export default function useCompanies() {
    const { data, error, isLoading } = useSWR(`${ADRESS}/v1/get_all_companies`, fetcher);

    if (
        isLoading || error
    ) return {
        companies: [],
        isLoading,
        isError: error
    }

    return {
        companies: data,
        isLoading,
        isError: error
    }
}
