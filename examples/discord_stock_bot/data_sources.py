from __future__ import annotations

import pandas as pd

from config import Settings


REQUIRED_COLUMNS = {"sku", "media_diaria", "estoque"}



def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    renamed = {name: str(name).strip().lower() for name in df.columns}
    return df.rename(columns=renamed)



def read_from_excel(settings: Settings) -> pd.DataFrame:
    if not settings.excel_file_path:
        raise ValueError("EXCEL_FILE_PATH não configurado.")

    df = pd.read_excel(settings.excel_file_path, sheet_name=settings.excel_sheet_name)
    df = _normalize_columns(df)
    _validate_columns(df)
    return df



def read_from_google_sheets(settings: Settings) -> pd.DataFrame:
    if not settings.sheets_id or not settings.service_account_file:
        raise ValueError("GOOGLE_SHEETS_ID e GOOGLE_SERVICE_ACCOUNT_FILE são obrigatórios.")

    import gspread

    client = gspread.service_account(filename=settings.service_account_file)
    worksheet = client.open_by_key(settings.sheets_id).worksheet(settings.sheets_worksheet)
    records = worksheet.get_all_records()
    df = pd.DataFrame(records)
    df = _normalize_columns(df)
    _validate_columns(df)
    return df



def read_stock_dataframe(settings: Settings) -> pd.DataFrame:
    if settings.data_source == "excel":
        return read_from_excel(settings)
    if settings.data_source == "google_sheets":
        return read_from_google_sheets(settings)

    raise ValueError("DATA_SOURCE inválido. Use 'excel' ou 'google_sheets'.")



def _validate_columns(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            "Colunas obrigatórias ausentes na planilha: " + ", ".join(sorted(missing))
        )
