'use client';
import 'react-pdf/dist/Page/TextLayer.css';
import { pdfjs } from 'react-pdf';

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.js',
  import.meta.url,
).toString();

export function FileZIP({ stackOrder
 } : { stackOrder: string }) {
    return (
        <div className={`relative flex flex-col justify-center ${stackOrder} text-foreground-white items-center inline-block w-full`}>
            <p>
                Selected document is a .zip archive and can not be pre-viewed.
            </p>
            <p>
                You can still download it on your local disk by clicking the 'Download data' button!
            </p>
        </div>
    )
}