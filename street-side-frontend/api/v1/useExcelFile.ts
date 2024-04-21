import useSWR from "swr"
import { ADRESS, fetcher } from '@/api/constants';
import { DocumentInterface } from "@/app/types/document";
import { ExcelFileInterface, ExcelSheetInterface } from "@/app/types/excel_file";

interface useExcelFileInterface {
    excelFile: ExcelFileInterface | null,
    isLoading: boolean,
    isError : boolean
}

function rowObjectToMap( rowObject: Object ): Map<string, string[]> {
    const rowMap = new Map<string, string[]>();
    for (const [rowIndex, rowValues] of Object.entries(rowObject) ) {
        rowMap.set(rowIndex, rowValues);
    }

    return rowMap;
}

function excelFileObjectToMap( sheets: Object ): Map<string, ExcelSheetInterface> {
    const sheetsAsMap = new Map<string, ExcelSheetInterface>();

    for (const [sheetName, sheetObject] of Object.entries(sheets) ) {
        const rowMap = rowObjectToMap(sheetObject.rows);
        sheetsAsMap.set(sheetName, {
            headers: sheetObject.headers,
            rows: rowMap,
        })
    }

    return sheetsAsMap;
}

export default function useExcelFile(document: DocumentInterface): useExcelFileInterface {
    const { data, error, isLoading } = useSWR(`${ADRESS}/v1/get_excel_file_by_document_hash_id/${document.hash_id}`, fetcher);

    if (
        isLoading || error
    ) return {
        excelFile: null,
        isLoading,
        isError: error
    }

    const dataAsMap = excelFileObjectToMap(data.sheets);
    return {
        excelFile: dataAsMap,
        isLoading,
        isError: error
    }
}
