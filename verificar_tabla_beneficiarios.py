from pathlib import Path
import openpyxl
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BOOK = Path(r"C:\dixsys\manual_pjev\sitio_web\outputs\beneficiarios_enero\tabla_beneficiarios_balanza_enero.xlsx")
PREVIEW = BOOK.with_name("preview_resultado.png")

wb = openpyxl.load_workbook(BOOK, read_only=True, data_only=True)
ws = wb["Resultado"]
rows = list(ws.iter_rows(values_only=True))
missing = [row for row in rows[1:] if row[4] in ("Falta proveedor", "Falta empleado")]
sample = [rows[0], *rows[1:9], *missing]

fig, ax = plt.subplots(figsize=(18, max(5, len(sample) * 0.42)))
ax.axis("off")
display = []
for ridx, row in enumerate(sample):
    formatted = []
    for cidx, value in enumerate(row):
        if cidx == 5 and isinstance(value, (int, float)):
            formatted.append(f"{value:,.2f}")
        else:
            formatted.append("" if value is None else str(value))
    display.append(formatted)

table = ax.table(cellText=display, loc="center", cellLoc="left", colWidths=[.12, .31, .14, .14, .24, .12])
table.auto_set_font_size(False)
table.set_fontsize(7.5)
table.scale(1, 1.55)
for (row, col), cell in table.get_celld().items():
    cell.set_edgecolor("#D9E2F3")
    if row == 0:
        cell.set_facecolor("#1F4E78")
        cell.get_text().set_color("white")
        cell.get_text().set_weight("bold")
    elif display[row][4] in ("Falta proveedor", "Falta empleado"):
        cell.set_facecolor("#FCE4D6")
    elif row % 2 == 0:
        cell.set_facecolor("#EAF2F8")
plt.tight_layout()
fig.savefig(PREVIEW, dpi=160, bbox_inches="tight")
print("PREVIEW", PREVIEW)
print("ROWS", ws.max_row - 1)
print("MISSING", len(missing))
print("PROVIDER_MISSING", sum(row[4] == "Falta proveedor" for row in rows[1:]))
print("EMPLOYEE_MISSING", sum(row[4] == "Falta empleado" for row in rows[1:]))
print("ACCOUNT_ENDS_0000", sum(str(row[0]).endswith("0000") for row in rows[1:]))
print("TOTAL_INITIAL_BALANCE", sum((row[5] or 0) for row in rows[1:]))
