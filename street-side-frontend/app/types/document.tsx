export interface DocumentInterface {
    document_type_id: string,
    date_published: string,
    quater: string | null,
    year: string | null,
    remote_url: string,
    extension: string,
    pretty_date: string,
    created_at: string,
    hash_id: string,
}

export type DocumentSetterInterace = React.Dispatch<React.SetStateAction<null | DocumentInterface>>

export function isDocumentInterface( value: DocumentInterface | null | undefined) {
    return (value === null || value === undefined);
}
export interface DocumentPropsInterace {
    selectedDocumentType: null | DocumentType,
    setSelectedDocumentType: DocumentSetterInterace,
}
