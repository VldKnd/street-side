'use client';
import { CompanyInterface } from "@/app/types/company";
import { DocumentSetterInterace } from "@/app/types/document";
import { DocumentTypeInterface, DocumentTypeSetterInterace } from "../types/document_type";

import useCompanyDocumentTypes from "@/api/v1/useCompanyDocumentTypes";
import { Listbox } from '@headlessui/react'

interface DropDownDocumentTypesInterface {
    selectedCompany: CompanyInterface,
    selectedDocumentType: DocumentTypeInterface | null,
    setSelectedDocumentType: DocumentTypeSetterInterace,
    setSelectedDocument: DocumentSetterInterace,
}

export function DropDownDocumentTypes({
  selectedCompany,
  selectedDocumentType,
  setSelectedDocumentType,
  setSelectedDocument,
 } : DropDownDocumentTypesInterface) {
  const stackOrder = 'z-10';

  const { documentTypes, isLoading } = useCompanyDocumentTypes(selectedCompany);

  if (isLoading) {
    return (
    <div className={`relative ${stackOrder} animate-pulse w-full h-full text-left text-sm  inline-block w-full bg-company-grey rounded-2xl pl-3 pt-3 pb-2`}>
        <p className="opacity-0">
          {". . ."}
        </p>
    </div>
    )
  }

  const onListBoxChange = (value : DocumentTypeInterface | null) => {
    if (value !== selectedDocumentType) {
      setSelectedDocumentType(value);
      setSelectedDocument(null);
    }
  }

  return (
    <Listbox value={selectedDocumentType} onChange={onListBoxChange} >
      {({ open }) => (
        <>
        <Listbox.Button className={`relative ${stackOrder} w-full h-full text-left text-sm  inline-block bg-company-grey ${open ? "rounded-t-2xl" : "rounded-2xl"} text-foreground-white pl-5 pt-3 pb-2`}>
            { selectedDocumentType ? selectedDocumentType.short_name : "Click to select" }
        </Listbox.Button>
        <Listbox.Options className={`absolute ${stackOrder} border-solid border w-1/3 border-opacity-25 border-foreground-white overflow-auto rounded-b-2xl bg-company-grey text-sm text-foreground-white`}>
        {documentTypes.map((document_type: DocumentTypeInterface) => (
            <Listbox.Option
            className={`relative ${stackOrder} overflow-hidden truncate pt-3 pb-2 pl-5 cursor-default select-none hover:opacity-75`}
            key={document_type.hash_id}
            value={document_type}
            >
            {document_type.short_name}
            </Listbox.Option>
        ))}
        </Listbox.Options>
        </>
      )}
    </Listbox>
    );
}