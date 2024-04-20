'use client';
import 'react-pdf/dist/Page/TextLayer.css';
import { DocumentInterface } from "../types/document";

function LoadingFile() {
    return (
      <div className={`relative flex animate-pulse justify-center text-foreground-white inline-block w-full`}>
            Loading ...
      </div>
    )
  }

export function FileExcel({
    selectedDocument, stackOrder
 } : { selectedDocument : DocumentInterface, stackOrder: string }) {
    if (true) return <LoadingFile />;
}