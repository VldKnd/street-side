'use client';
import { FilePDF } from "@/app/raw/FilePDF";
import { FileExcel } from "@/app/raw/FileExcel";
import { DocumentInterface } from "@/app/types/document";

export function File({ selectedDocument } : { selectedDocument : DocumentInterface }) {
  const stackOrder = `z-8`

  if (selectedDocument.extension == ".pdf") {
    return <FilePDF stackOrder={stackOrder} selectedDocument={selectedDocument}/>
  } else if (selectedDocument.extension == ".xlsx") {
    return <FileExcel stackOrder={stackOrder} selectedDocument={selectedDocument}/>
  }
}