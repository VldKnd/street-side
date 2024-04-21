'use client';
import { ExcelSheetInterface, isExcelFileInterface, isExcelSheetInterface } from "../types/excel_file";
import { useState } from "react";
import useExcelFile from "@/api/v1/useExcelFile";
import { DocumentInterface } from "../types/document";

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
                Try refreshing the page or come back later
            </p>
        </div>
    )
}

function createTableBodyFromExcelSheet( excelSheet : ExcelSheetInterface ) {
    return (
        <tbody>
        {
            Array.from(excelSheet.rows.values()).map(
                (value: string[], index: number) => {
                    return (
                        <tr key={index}>
                        {
                            value.map(
                                ( _value: string, _index: number ) => {
                                    return (
                                        <td
                                        className="text-sm text-center text-balance bg-background-black border border-company-grey p-3 text-foreground-white"
                                        key={`${index},${_index}`}
                                        >
                                            {_value}
                                        </td>
                                    )
                                }
                            )
                        }
                        </tr>
                    )
                }
            )
        }
        </tbody>
    )
}

function createTableHeadFromExcelSheet( excelSheet : ExcelSheetInterface ) {
    return (
        <thead>
            <tr>
            {
                excelSheet.headers.map(
                    (value: string, index: number) => {
                        return (
                            <th
                            className="border bg-company-grey border-company-grey p-3 text-foreground-white"
                            key={index}
                            >
                                {value}
                            </th>
                        )
                    }
                )
            }
            </tr>
        </thead>
    )
}

function createTableFromExcelSheet( excelSheet : ExcelSheetInterface | undefined) {
    if ( typeof excelSheet === undefined ) return;

    return (
    <div className="overflow-scroll flex bg-company-grey max-h-screen w-full border border-collapse border-company-grey">
        <table className="w-full">
            {
                createTableHeadFromExcelSheet(excelSheet)
            }
            {
                createTableBodyFromExcelSheet(excelSheet)
            }
        </table>
    </div>
    )
}
export function FileExcel({
    selectedDocument, stackOrder
 } : { selectedDocument : DocumentInterface, stackOrder: string }) {
    const { excelFile, isLoading, isError } = useExcelFile(selectedDocument);
    const [selectedExcelSheet, setSelectedExcelSheet] = useState<string>('');
    const activatedExcelSheetStyle = "text-foreground-white bg-company-grey relative text-sm inline-block rounded-t-2xl px-3 pb-2 pt-3 mx-2"
    const notActivatedExcelSheetStyle = "text-foreground-white border-2 border-company-grey hover:opacity-50 relative text-sm inline-block rounded-2xl px-3 pb-2 pt-3 mb-2 mx-2"
    if (isLoading) return <LoadingFile />
    if (isError) return <LoadingError />

    return (
        <div className={`relative ${stackOrder} w-full`}>
            <div className="overflow-x-auto flex rounded-t-2xl" >
            {
                !isExcelFileInterface(excelFile) &&
                Array.from(excelFile.keys()).map(
                    (value: string, index) => {
                        return (
                            <button
                                key={index}
                                className={`${value == selectedExcelSheet ? activatedExcelSheetStyle : notActivatedExcelSheetStyle }`}
                                onClick={() => {setSelectedExcelSheet(value)}}
                            >
                                {value}
                            </button>
                        )
                    }
                )
            }
            </div>
            {
                selectedExcelSheet != '' &&
                !isExcelFileInterface(excelFile) &&
                createTableFromExcelSheet(excelFile.get(selectedExcelSheet))
            }
        </div>
    )
   
}