export interface ExcelSheetInterface {
    headers: string[],
    rows: Map<string, string[] >
}

export type ExcelFileInterface = Map<string, ExcelSheetInterface>

export type ExcelFileSetter = React.Dispatch<React.SetStateAction<null | ExcelFileInterface>>

export function isExcelFileInterface( value: ExcelFileInterface | null | undefined) {
    return (value === null || value === undefined);
}

export function isExcelSheetInterface( value: ExcelSheetInterface | null | undefined) {
    return (value === null || value === undefined);
}