'use client';
import { DropDownCompanies } from "@/app/raw/DropDownCompanies";
import { DropDownDocumentTypes } from "@/app/raw/DropDownDocumentTypes";
import { DropDownDocuments } from "@/app/raw/DropDownDocuments";
import { DownloadFileButton } from "@/app/raw/DownloadFileButton";
import { File } from "@/app/raw/File";
import { useState } from 'react'
import { CompanyInterface, isCompanyInterface } from "../types/company";
import { DocumentTypeInterface, isDocumentTypeInterface } from "../types/document_type";
import { DocumentInterface, isDocumentInterface } from "../types/document";

export default function RawDocumentsPage() {
  const [selectedCompany, setSelectedCompany] = useState<CompanyInterface | null>(null);
  const [selectedDocumentType, setSelectedDocumentType] = useState<DocumentTypeInterface | null>(null);
  const [selectedDocument, setSelectedDocument] = useState<DocumentInterface | null>(null);

  return (
    <div className='w-10/12'>
      <div className='relative h-full w-full'>
        <div className='mb-3 ml-3 text-foreground-white text-base'>
          {"Select a clearing company"}
        </div>
        <DropDownCompanies
          selectedCompany={selectedCompany}
          setSelectedCompany={setSelectedCompany}
          setSelectedDocumentType={setSelectedDocumentType}
          setSelectedDocument={setSelectedDocument}
        />
        <div className="flex z-9 flex-row mt-3 h-full z-9">
          <div className="w-1/3 z-10">
            {
              !isCompanyInterface(selectedCompany) &&
              <DropDownDocumentTypes
                selectedCompany={selectedCompany}
                selectedDocumentType={selectedDocumentType}
                setSelectedDocumentType={setSelectedDocumentType}
                setSelectedDocument={setSelectedDocument}
              />
            }
          </div>
          <div className="ml-2 w-1/4 z-10">
            {
              !isCompanyInterface(selectedCompany) &&
              !isDocumentTypeInterface(selectedDocumentType) &&
              <DropDownDocuments
                selectedCompany={selectedCompany}
                selectedDocumentType={selectedDocumentType}
                selectedDocument={selectedDocument}
                setSelectedDocument={setSelectedDocument}
              />
            }
          </div>
          <div className="ml-2 z-10">
            {
              !isCompanyInterface(selectedCompany) &&
              !isDocumentTypeInterface(selectedDocumentType) &&
              !isDocumentInterface(selectedDocument) &&
              <DownloadFileButton selectedDocument={selectedDocument} />
            }
          </div>
        </div>
        <div className="mt-5 flex h-full w-full">
          {
            !isCompanyInterface(selectedCompany) &&
            !isDocumentTypeInterface(selectedDocumentType) &&
            !isDocumentInterface(selectedDocument) &&
            <File selectedDocument={selectedDocument} />
          }
        </div>
      </div>
    </div>
  );
}
