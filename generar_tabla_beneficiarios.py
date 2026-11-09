from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from decimal import Decimal, InvalidOperation
from difflib import SequenceMatcher
from pathlib import Path
import re
import unicodedata

import openpyxl
import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.table import Table, TableStyleInfo


BASE = Path(r"C:\Users\Julio C Barrales\Downloads")
EMPLOYEES_FILE = BASE / "Catalogo_Empleados.xlsx"
ACCOUNTS_FILE = BASE / "catalogo_cuentas_2026-07-22.xls"
BALANCE_FILE = BASE / "balanza_comprobacion_enero.xlsx"
OUTPUT_DIR = Path(r"C:\dixsys\manual_pjev\sitio_web\outputs\beneficiarios_enero")
OUTPUT_FILE = OUTPUT_DIR / "tabla_beneficiarios_balanza_enero.xlsx"


PROVIDERS = [
    ("00001", "COMISION MUNICIPAL DE AGUA POTABLE Y SANEAMIENTO", ["COMISION MPAL DE AGUA POTABLE Y SANEAM"]),
    ("00002", "COMISION FEDERAL DE ELECTRICIDAD", []),
    ("00003", "RENTAS", []),
    ("00004", "SERVICIO POSTAL MEXICANO", []),
    ("00005", "SISTEMAS CONTINO S.A. DE C.V.", []),
    ("00006", "TELMEX", []),
    ("00007", "PROVEEDORES DE BIENES Y SERVICIOS VARIOS", []),
    ("00008", "EDENRED MEXICO S.A. DE C.V.", []),
    ("00009", "COMISION DEL AGUA DEL ESTADO DE VERACRUZ", []),
    ("00010", "TOTAL PLAY TELECOMUNICACIONES", []),
    ("00011", "HIDROSISTEMA DE CORDOBA", []),
    ("00012", "GRUPO METROPOLITANO DE AGUA Y SANEAMIENTO", ["GRUPO METROP. DE AGUA Y SANEAMIENTO"]),
    ("00013", "COMISION MUNICIPAL DE AGUA POTABLE Y SANEAMIENTO DE HUATUSCO", ["COMIS MPAL AGUA POTAB Y SANEA HUATUSCO"]),
    ("00014", "COMISION MUNICIPAL DE AGUA POTABLE Y SANEAMIENTO", ["COMISION MUNICIPAL DE AGUA Y SANEAMIENTO"]),
    ("00015", "COMISION MUNICIPAL DE AGUA POTABLE Y SANEAMIENTO DE LA ANTIGUA", ["COMISION MPAL. AGUA POTAB Y SANEA ANTIG"]),
    ("00016", "AZIEL MUÑOZ CORDOBA", []),
    ("00017", "MEGACABLE COMUNICACIONES DE MEXICO", []),
    ("00018", "COMISION MUNICIPAL DE AGUA POTABLE Y SANEAMIENTO DE SAN ANDRES", ["COMISION MPAL AGUA POTAB Y SANEA SAN AND"]),
    ("00019", "BLEGAM CORP", []),
    ("00020", "MIRCA ABASTECEDORA", []),
    ("00021", "MUNICIPIO DE MINATITLAN, VER.", ["MUNICIPIO DE MINATITLAN,VER,."]),
    ("00022", "OFFICARSA S.A. DE C.V.", []),
    ("00023", "LEMAR DE XALAPA", []),
    ("00024", "IVREA CONSTRUCCIONES S. DE R.L. DE C.V.", ["IVREA CONSTRUCCIONES S DE RL DE CV"]),
]


def repair_text(value) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    try:
        repaired = text.encode("latin1").decode("utf-8")
        if repaired.count("�") <= text.count("�"):
            text = repaired
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass
    return text


def normalize(value) -> str:
    text = repair_text(value).upper()
    text = "".join(
        char for char in unicodedata.normalize("NFD", text)
        if unicodedata.category(char) != "Mn"
    )
    text = text.replace("Ñ", "N")
    return re.sub(r"[^A-Z0-9]+", " ", text).strip()


def account_key(value) -> str:
    return re.sub(r"\D", "", repair_text(value))


def parse_amount(value) -> float | None:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = repair_text(value).replace(",", "").replace("$", "").strip()
    if text.startswith("(") and text.endswith(")"):
        text = "-" + text[1:-1]
    try:
        return float(Decimal(text))
    except (InvalidOperation, ValueError):
        return None


def strip_role_prefix(value) -> str:
    text = normalize(value)
    prefixes = (
        "DEUDOR ", "DEUDORA ", "EMPLEADO ", "EMPLEADA ",
        "PROVEEDOR ", "PROVEEDORA ",
    )
    changed = True
    while changed:
        changed = False
        for prefix in prefixes:
            if text.startswith(prefix):
                text = text[len(prefix):].strip()
                changed = True
    return text


def sorted_tokens(value) -> tuple[str, ...]:
    return tuple(sorted(strip_role_prefix(value).split()))


def load_employees():
    wb = load_workbook(EMPLOYEES_FILE, read_only=True, data_only=True)
    ws = wb[wb.sheetnames[0]]
    rows = ws.iter_rows(values_only=True)
    headers = [normalize(v) for v in next(rows)]
    number_idx = headers.index("NUMERO EMPLEADO")
    name_idx = headers.index("NOMBRE")
    employees = []
    exact = defaultdict(list)
    for row in rows:
        number = repair_text(row[number_idx])
        name = repair_text(row[name_idx])
        if not number or not name:
            continue
        number = number.zfill(10)
        record = {"number": number, "name": name, "tokens": sorted_tokens(name)}
        employees.append(record)
        exact[record["tokens"]].append(record)
    return employees, exact


def load_accounts():
    table = pd.read_html(ACCOUNTS_FILE)[0]
    table.columns = [repair_text(c) for c in table.columns]
    level_col = next(c for c in table.columns if normalize(c) == "NIVEL")
    account_col = next(c for c in table.columns if normalize(c) == "CUENTA CONTABLE")
    affect_col = next(c for c in table.columns if "AFECTACION" in normalize(c))
    table["_level"] = pd.to_numeric(table[level_col], errors="coerce")
    table = table[table["_level"] == 6].copy()
    exact = {}
    prefix_affects = defaultdict(set)
    for _, row in table.iterrows():
        key = account_key(row[account_col])
        affect = repair_text(row[affect_col])
        if not key or not affect:
            continue
        exact[key] = affect
        prefix_affects[key[:8]].add(affect)
    return exact, prefix_affects


def load_provider_indexes():
    exact = {}
    records = []
    for number, name, aliases in PROVIDERS:
        record = {"number": number, "name": name}
        records.append(record)
        for label in [name, *aliases]:
            exact[normalize(label)] = record
    return records, exact


def fuzzy_best(query, records, field="name"):
    query_norm = normalize(query)
    if not query_norm:
        return None, 0.0, 0.0
    scored = []
    for record in records:
        candidate = normalize(record[field])
        score = SequenceMatcher(None, query_norm, candidate).ratio()
        scored.append((score, record))
    scored.sort(key=lambda item: item[0], reverse=True)
    best_score, best_record = scored[0]
    second_score = scored[1][0] if len(scored) > 1 else 0.0
    return best_record, best_score, best_score - second_score


def match_employee(description, employees, exact_index):
    tokens = sorted_tokens(description)
    exact_matches = exact_index.get(tokens, [])
    if len(exact_matches) == 1:
        return exact_matches[0], "exacta"
    if len(exact_matches) > 1:
        return None, "ambigua"

    query = " ".join(tokens)
    scored = []
    for employee in employees:
        candidate = " ".join(employee["tokens"])
        score = SequenceMatcher(None, query, candidate).ratio()
        scored.append((score, employee))
    scored.sort(key=lambda item: item[0], reverse=True)
    best_score, best = scored[0]
    second_score = scored[1][0] if len(scored) > 1 else 0.0
    if best_score >= 0.92 and best_score - second_score >= 0.035:
        return best, f"probable:{best_score:.3f}"
    return None, f"sin_coincidencia:{best_score:.3f}"


def match_provider(description, providers, exact_index):
    key = normalize(description)
    if key in exact_index:
        return exact_index[key], "exacta"
    best, score, lead = fuzzy_best(description, providers)
    if score >= 0.86 and lead >= 0.04:
        return best, f"probable:{score:.3f}"
    return None, f"sin_coincidencia:{score:.3f}"


def classify_account(key, exact_accounts, prefix_affects):
    # In beneficiary-controlled accounts, the catalog uses sentinel subaccounts
    # (for example 9001) to declare the affectation. The balance replaces those
    # last four digits with the beneficiary subaccount, so the prefix rule must
    # take precedence over coincidental exact rows for administrative units.
    affects = prefix_affects.get(key[:8], set())
    target_affects = {
        normalize(a): a for a in affects
        if normalize(a) in {"PROVEEDOR", "EMPLEADO"}
    }
    if len(target_affects) == 1:
        return next(iter(target_affects.values())), "prefijo_afectacion"
    if key in exact_accounts:
        return exact_accounts[key], "exacta"
    normalized = {normalize(a): a for a in affects if normalize(a)}
    if len(normalized) == 1:
        return next(iter(normalized.values())), "prefijo"
    return "", "sin_correspondencia"


def build_output():
    employees, employee_exact = load_employees()
    exact_accounts, prefix_affects = load_accounts()
    providers, provider_exact = load_provider_indexes()

    source = load_workbook(BALANCE_FILE, read_only=True, data_only=True)
    ws_source = source[source.sheetnames[0]]
    source_rows = list(ws_source.iter_rows(values_only=True))
    headers = [normalize(v) for v in source_rows[0]]
    account_idx = headers.index("CUENTA CONTABLE")
    description_idx = headers.index("DESCRIPCION")  # first occurrence by design
    balance_idx = headers.index("SALDO INICIAL")

    output_rows = []
    audit = []
    stats = defaultdict(int)

    for source_row_num, row in enumerate(source_rows[1:], start=2):
        key = account_key(row[account_idx])
        if not key or key.endswith("0000"):
            stats["excluidas_no_nivel_6"] += 1
            continue

        description = repair_text(row[description_idx])
        affect, account_match = classify_account(key, exact_accounts, prefix_affects)
        affect_norm = normalize(affect)
        beneficiary_number = ""
        beneficiary = ""
        beneficiary_match = "no_aplica"

        if affect_norm == "PROVEEDOR":
            record, beneficiary_match = match_provider(description, providers, provider_exact)
            if record:
                beneficiary_number = record["number"]
                beneficiary = record["name"]
                stats["proveedores_encontrados"] += 1
            else:
                beneficiary = "Falta proveedor"
                stats["proveedores_faltantes"] += 1
        elif affect_norm == "EMPLEADO":
            record, beneficiary_match = match_employee(description, employees, employee_exact)
            if record:
                beneficiary_number = record["number"]
                beneficiary = record["name"]
                stats["empleados_encontrados"] += 1
            else:
                beneficiary = "Falta empleado"
                stats["empleados_faltantes"] += 1
        elif not affect_norm:
            stats["cuentas_sin_correspondencia"] += 1
        else:
            stats["otras_afectaciones"] += 1

        output_rows.append([
            key,
            description,
            affect,
            beneficiary_number,
            beneficiary,
            parse_amount(row[balance_idx]),
        ])
        audit.append((source_row_num, key, account_match, affect, beneficiary_match, description, beneficiary))

    wb = Workbook()
    ws = wb.active
    ws.title = "Resultado"
    ws.sheet_view.showGridLines = False
    headers_out = [
        "Cuenta contable", "Descripción", "Nivel de afectación",
        "Número de beneficiario", "Beneficiario", "Saldo inicial",
    ]
    ws.append(headers_out)
    for output_row in output_rows:
        ws.append(output_row)

    navy = "1F4E78"
    light_blue = "D9EAF7"
    light_red = "FCE4D6"
    light_border = Side(style="thin", color="D9E2F3")
    header = ws[1]
    for cell in header:
        cell.fill = PatternFill("solid", fgColor=navy)
        cell.font = Font(color="FFFFFF", bold=True)
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = Border(bottom=Side(style="medium", color="17365D"))
    ws.row_dimensions[1].height = 28

    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        row[0].number_format = "@"
        row[3].number_format = "@"
        row[5].number_format = '#,##0.00;[Red](#,##0.00);-'
        row[5].alignment = Alignment(horizontal="right")
        for cell in row:
            cell.border = Border(bottom=light_border)
            cell.alignment = Alignment(vertical="top", wrap_text=False)
        if row[4].value in ("Falta proveedor", "Falta empleado"):
            for cell in row:
                cell.fill = PatternFill("solid", fgColor=light_red)

    widths = {"A": 18, "B": 48, "C": 23, "D": 24, "E": 48, "F": 18}
    for col, width in widths.items():
        ws.column_dimensions[col].width = width
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:F{ws.max_row}"
    table = Table(displayName="TablaBeneficiarios", ref=f"A1:F{ws.max_row}")
    table.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium2", showFirstColumn=False,
        showLastColumn=False, showRowStripes=True, showColumnStripes=False,
    )
    ws.add_table(table)
    ws.auto_filter.ref = f"A1:F{ws.max_row}"
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.print_title_rows = "1:1"
    ws.sheet_properties.tabColor = navy

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    wb.save(OUTPUT_FILE)

    # Verification: reopen the generated workbook and validate structure/types.
    check_wb = load_workbook(OUTPUT_FILE, read_only=False, data_only=False)
    check_ws = check_wb["Resultado"]
    assert check_ws.max_row == len(output_rows) + 1
    assert check_ws.max_column == 6
    assert [check_ws.cell(1, c).value for c in range(1, 7)] == headers_out
    assert all(not account_key(check_ws.cell(r, 1).value).endswith("0000") for r in range(2, check_ws.max_row + 1))
    assert all(isinstance(check_ws.cell(r, 6).value, (int, float)) or check_ws.cell(r, 6).value is None for r in range(2, check_ws.max_row + 1))

    print("OUTPUT", OUTPUT_FILE)
    print("ROWS", len(output_rows))
    for key in sorted(stats):
        print(key.upper(), stats[key])
    print("MISSING_DETAIL")
    for item in audit:
        if item[-1] in ("Falta proveedor", "Falta empleado"):
            print(item)


if __name__ == "__main__":
    build_output()
