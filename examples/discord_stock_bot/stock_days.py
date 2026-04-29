from __future__ import annotations

from dataclasses import dataclass
from math import ceil

import pandas as pd


@dataclass(frozen=True)
class StockRow:
    sku: str
    media_diaria: float
    estoque: float
    dias_restantes: int



def _to_float(value: object) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0



def build_stock_rows(df: pd.DataFrame) -> list[StockRow]:
    rows: list[StockRow] = []
    for _, row in df.iterrows():
        sku = str(row.get("sku", "")).strip()
        if not sku:
            continue

        media = _to_float(row.get("media_diaria", 0))
        estoque = _to_float(row.get("estoque", 0))

        dias = 0 if media <= 0 else max(0, ceil(estoque / media))
        rows.append(StockRow(sku=sku, media_diaria=media, estoque=estoque, dias_restantes=dias))

    return rows



def format_top_shortage(rows: list[StockRow], top_n: int = 15) -> str:
    if not rows:
        return "Nenhum dado de estoque encontrado."

    ordered = sorted(rows, key=lambda item: item.dias_restantes)
    lines = ["📦 **Dias restantes de estoque (menor cobertura primeiro)**"]
    for row in ordered[:top_n]:
        lines.append(
            f"- `{row.sku}` | média: {row.media_diaria:.2f} | estoque: {row.estoque:.0f} | **{row.dias_restantes} dias**"
        )

    return "\n".join(lines)
