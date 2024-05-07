'use client';
import { CompanyInterface } from "@/app/types/company";
import { DocumentSetterInterace, DocumentInterface } from "@/app/types/document";
import { DocumentTypeInterface } from "../types/document_type";

import useDocuments from "@/api/v1/useDocuments";
import { Listbox } from '@headlessui/react'

interface DropDownDocumentsInterface {
    selectedCompany: CompanyInterface,
    selectedDocumentType: DocumentTypeInterface,
    selectedDocument: DocumentInterface | null,
    setSelectedDocument: DocumentSetterInterace,
}

export function DropDownDocuments({
  selectedDocumentType,
  selectedDocument,
  setSelectedDocument,
 } : DropDownDocumentsInterface) {
  const stackOrder = `z-10`
  const { documents, isLoading } = useDocuments(selectedDocumentType);

  if (isLoading) {
    return (
    <div className={`relative ${stackOrder} animate-pulse w-full h-full text-left text-sm  inline-block w-full bg-company-grey rounded-2xl text-foreground-white pl-3 pt-3 pb-2`}>
        <p className="opacity-0">
          {". . ."}
        </p>
    </div>
    )
  }

  const onListBoxChange = (value : DocumentInterface | null) => {
    setSelectedDocument(value);
  }

  var sortedDocuments = [...documents];
  sortedDocuments.sort(
    (lhs, rhs) => lhs.pretty_date.localeCompare(rhs.pretty_date)
  )

  return (
    <Listbox value={selectedDocument} onChange={onListBoxChange} >
      {({ open }) => (
        <>
        <Listbox.Button className={`relative ${stackOrder}  w-full h-full text-left text-sm  inline-block bg-company-grey ${open ? "rounded-t-2xl" : "rounded-2xl"} text-foreground-white pl-5 pt-3 pb-2`}>
            { selectedDocument ? selectedDocument.pretty_date : "Click to select a date" }
        </Listbox.Button>
        <Listbox.Options className={`absolute ${stackOrder} border-solid border w-1/4  max-h-60 border-opacity-25 border-foreground-white overflow-auto rounded-b-2xl bg-company-grey text-sm text-foreground-white`}>
        {sortedDocuments.map((document: DocumentInterface) => (
            <Listbox.Option
            className={`relative ${stackOrder} overflow-hidden truncate pt-3 pb-2 pl-5 cursor-default select-none hover:opacity-75`}
            key={document.hash_id}
            value={document}
            >
            {document.pretty_date}
            </Listbox.Option>
        ))}
        </Listbox.Options>
        </>
      )}
    </Listbox>
    );
}