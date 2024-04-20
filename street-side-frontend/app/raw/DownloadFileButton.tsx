'use client';
import { DocumentInterface } from "@/app/types/document";
import { ADRESS } from '@/api/constants';


export function DownloadFileButton({ selectedDocument } : { selectedDocument : DocumentInterface }) {
  return (
      <a className={`h-full text-left text-sm  inline-block bg-company-grey rounded-2xl text-foreground-white pl-5 pt-3 pb-2 pr-6`} href={`${ADRESS}/v1/download_file/${selectedDocument.hash_id}`}>
         {"Download"}
      </a>
    );
}