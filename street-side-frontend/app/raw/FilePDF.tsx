'use client';
import { useState } from "react";
import 'react-pdf/dist/Page/TextLayer.css';
import { DocumentInterface } from "../types/document";
import { pdfjs, Document, Page } from 'react-pdf';
import useFileBase64 from "@/api/v1/useFile";

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.js',
  import.meta.url,
).toString();

function LoadingFile() {
    return (
        <div className={`relative flex animate-pulse justify-center text-foreground-white inline-block w-full`}>
            Loading ...
        </div>
    )
}

function LoadingError() {
    return (
        <div className={`relative flex flex-col items-center justify-center text-foreground-white inline-block w-full`}>
            <p>
               Unexpected error occurred while loading the file!
            </p>
            <p>
                Try refreshing the page or come back later.
            </p>
        </div>
    )
}

export function FilePDF({
    selectedDocument, stackOrder
 } : { selectedDocument : DocumentInterface, stackOrder: string }) {
    const { fileBase64, isLoading, isError } = useFileBase64(selectedDocument);
    const [numPages, setNumPages] = useState<number>();
    function onDocumentLoadSuccess({ numPages }: { numPages: number }): void {
        setNumPages(numPages);
    }

    if (isLoading) return <LoadingFile />
    if (isError) return <LoadingError />
    
    return (
        <div className={`relative flex justify-center ${stackOrder} text-sm inline-block w-full`}>
            <Document
                loading={<div />}
                file={`data:application/pdf;base64,${fileBase64}`}
                onLoadSuccess={onDocumentLoadSuccess}
            >
                <div className="bg-company-grey rounded-lg overflow-y-auto overflow-x-hidden max-h-screen">
                {numPages &&
                    Array.from({ length: numPages }, (_, index) => index + 1).map(
                    (pageNumber) => {
                    return <Page
                        key={pageNumber}
                        renderAnnotationLayer={false}
                        renderTextLayer={true}
                        pageNumber={pageNumber}
                    />
                    })}
                </div>
            </Document>
        </div>
    )
}