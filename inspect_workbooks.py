from pathlib import Path
import openpyxl
import importlib.util

print("OPTIONAL_MODULES", {name: bool(importlib.util.find_spec(name)) for name in ("win32com", "pandas", "xlrd", "olefile")})

BASE = Path(r"C:\Users\Julio C Barrales\Downloads")
FILES = [
    BASE / "Catalogo_Empleados.xlsx",
    BASE / "catalogo_cuentas_2026-07-22.xls",
    BASE / "balanza_comprobacion_enero.xlsx",
]

for path in FILES:
    print(f"\nFILE: {path.name} ({path.stat().st_size} bytes)")
    if path.suffix.lower() == ".xlsx":
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        print("SHEETS:", wb.sheetnames)
        for ws in wb.worksheets:
            print(f"  SHEET {ws.title}: rows={ws.max_row}, cols={ws.max_column}")
            for row in ws.iter_rows(min_row=1, max_row=min(ws.max_row, 12), values_only=True):
                print("   ", row[:15])
    else:
        raw = path.read_bytes()
        if raw.lstrip(b"\xef\xbb\xbf").lower().startswith(b"<html"):
            import pandas as pd
            tables = pd.read_html(path)
            print(f"HTML_TABLES: {len(tables)}")
            for i, table in enumerate(tables):
                print(f"  TABLE {i}: rows={len(table)}, cols={len(table.columns)}")
                print(table.head(12).to_string(index=False))
            continue
        try:
            import xlrd
        except ImportError as exc:
            print("XLRD_MISSING", exc)
            continue
        wb = xlrd.open_workbook(path)
        print("SHEETS:", wb.sheet_names())
        for ws in wb.sheets():
            print(f"  SHEET {ws.name}: rows={ws.nrows}, cols={ws.ncols}")
            for i in range(min(ws.nrows, 12)):
                print("   ", tuple(ws.row_values(i)[:15]))
