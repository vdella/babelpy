import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    discord_token: str
    guild_id: int | None
    channel_id: int | None
    data_source: str
    sheets_id: str | None
    sheets_worksheet: str
    service_account_file: str | None
    excel_file_path: str | None
    excel_sheet_name: str



def _to_optional_int(value: str | None) -> int | None:
    if not value:
        return None
    return int(value)



def load_settings() -> Settings:
    data_source = os.getenv("DATA_SOURCE", "google_sheets").strip().lower()
    return Settings(
        discord_token=os.environ["DISCORD_TOKEN"],
        guild_id=_to_optional_int(os.getenv("DISCORD_GUILD_ID")),
        channel_id=_to_optional_int(os.getenv("DISCORD_CHANNEL_ID")),
        data_source=data_source,
        sheets_id=os.getenv("GOOGLE_SHEETS_ID"),
        sheets_worksheet=os.getenv("GOOGLE_SHEETS_WORKSHEET", "Estoque"),
        service_account_file=os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE"),
        excel_file_path=os.getenv("EXCEL_FILE_PATH"),
        excel_sheet_name=os.getenv("EXCEL_SHEET_NAME", "Estoque"),
    )
