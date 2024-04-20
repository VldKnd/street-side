export interface CompanyInterface {
    short_name: string,
    full_name: string,
    home_url: string,
    created_at: string,
    hash_id: string,
}

export type CompanySetter = React.Dispatch<React.SetStateAction<null | CompanyInterface>>

export function isCompanyInterface( value: CompanyInterface | null | undefined) {
    return (value === null || value === undefined);
}

export interface CompanyPropsInterace {
    selectedCompany: null | CompanyInterface,
    setSelectedCompany:  CompanySetter,
}
