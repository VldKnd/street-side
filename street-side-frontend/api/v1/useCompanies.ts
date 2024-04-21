import useSWR from "swr"
import { ADRESS, fetcher } from '@/api/constants';
import { CompanyInterface } from "@/app/types/company";

interface useCompaniesInterface {
    companies: CompanyInterface[],
    isLoading: boolean,
    isError : boolean
}

export default function useCompanies() : useCompaniesInterface {
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
