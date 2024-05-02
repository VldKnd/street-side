from typing import Dict, Hashable, List

import pandas
import pydantic


class ExcelSheet(pydantic.BaseModel):
    headers: List[Hashable]
    rows: Dict[int, List[str]]


class ExcelFile(pydantic.BaseModel):
    sheets: Dict[str, ExcelSheet]
    
    @classmethod
    def get_excel_file_from_local_disk(cls, path_to_file: str):
        try:
            excel_file = pandas.ExcelFile(path_to_file)
        except Exception as e:
            raise RuntimeError(f"Excel file parsing failed. {e}")
        
        sheet_names = excel_file.sheet_names
        sheets = {}

        for sheet_name in sheet_names:
            excel_sheet_as_dataframe = excel_file.parse(sheet_name)
            if excel_sheet_as_dataframe.empty: continue
            excel_sheet_as_dict = excel_sheet_as_dataframe.fillna('').astype(str).to_dict()
            headers = list(excel_sheet_as_dict.keys())
            indexes = excel_sheet_as_dict[headers[-1]].keys()
            rows = {
                index:[excel_sheet_as_dict[header][index] for header in headers]
                for index in indexes
            }

            sheets[sheet_name] = ExcelSheet(
                headers=headers,
                rows=rows,
            )

        return cls(sheets=sheets)