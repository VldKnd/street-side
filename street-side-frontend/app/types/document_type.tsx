export interface DocumentTypeInterface {
    company_hash_id: string,
    full_name: string,
    short_name: string,
    is_quaterly: boolean,
    is_yearly: boolean,
    created_at: string,
    hash_id: string,
}

export type DocumentTypeSetterInterace = React.Dispatch<React.SetStateAction<null | DocumentTypeInterface>>

export function isDocumentTypeInterface( value: DocumentTypeInterface | null | undefined) {
    return (value === null || value === undefined);
}

export interface DocumentTypePropsInterace {
    selectedDocumentType: null | DocumentTypeInterface,
    setSelectedDocumentType: DocumentTypeSetterInterace,
}
