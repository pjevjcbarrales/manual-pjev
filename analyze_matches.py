from pathlib import Path
import pandas as pd
import openpyxl
import unicodedata
import re

BASE = Path(r"C:\Users\Julio C Barrales\Downloads")

def clean_text(value):
    if value is None:
        return ""
    text = str(value).strip()
    try:
        text = text.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass
    return text

def normalize(value):
    text = clean_text(value).upper()
    text = "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")
    return re.sub(r"[^A-Z0-9]+", " ", text).strip()

accounts = pd.read_html(BASE / "catalogo_cuentas_2026-07-22.xls")[0]
accounts.columns = [clean_text(c) for c in accounts.columns]
print("COLUMNS", list(accounts.columns))
for col in accounts.columns:
    if "afect" in normalize(col).lower():
        affect_col = col
        break
else:
    raise RuntimeError("No affect column")

accounts["Nivel_num"] = pd.to_numeric(accounts["Nivel"], errors="coerce")
level6 = accounts[accounts["Nivel_num"] == 6].copy()
print("LEVEL6", len(level6))
print("AFFECT_COUNTS")
print(level6[affect_col].map(clean_text).value_counts(dropna=False).to_string())
print("RELEVANT SAMPLES")
mask = level6[affect_col].map(normalize).isin(["PROVEEDOR", "EMPLEADO"])
print(level6.loc[mask, ["Cuenta contable", "Descripción", affect_col]].head(80).to_string(index=False))

wb = openpyxl.load_workbook(BASE / "balanza_comprobacion_enero.xlsx", read_only=True, data_only=True)
ws = wb.active
rows = list(ws.iter_rows(values_only=True))
headers = [clean_text(x) for x in rows[0]]
print("BAL_HEADERS", headers)
idx_account = next(i for i,h in enumerate(headers) if normalize(h)=="CUENTA CONTABLE")
bal_accounts = []
for row in rows[1:]:
    val = row[idx_account]
    if val is not None:
        s = re.sub(r"\D", "", str(val))
        bal_accounts.append(s)
print("BAL_ROWS", len(bal_accounts), "LAST4_NONZERO", sum(not s.endswith("0000") for s in bal_accounts))

catalog_keys = {re.sub(r"\D", "", clean_text(x)): i for i,x in enumerate(level6["Cuenta contable"]) if clean_text(x)}
print("BAL_LEVEL6_MATCH", sum(s in catalog_keys for s in bal_accounts))
print("BAL_NO_CATALOG", [s for s in bal_accounts if not s.endswith('0000') and s not in catalog_keys][:30])

affected_prefixes = {}
for _, rec in level6.loc[mask].iterrows():
    key = re.sub(r"\D", "", clean_text(rec["Cuenta contable"]))
    affected_prefixes.setdefault(key[:8], set()).add(normalize(rec[affect_col]))
print("AFFECTED_PREFIXES", affected_prefixes)

print("BAL_ROWS_AFFECTED_PREFIX")
for row in rows[1:]:
    val = row[idx_account]
    if val is None:
        continue
    key = re.sub(r"\D", "", str(val))
    if key[:8] in affected_prefixes:
        print(key, affected_prefixes[key[:8]], "ORIG=", clean_text(row[1]), "LOOKUP=", clean_text(row[7]), "SALDO=", clean_text(row[2]))
