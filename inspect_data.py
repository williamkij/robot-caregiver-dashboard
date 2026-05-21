import os
import pandas as pd
import pyreadstat

RAW_DATA_PATH = os.path.join("data", "raw", "ATP W27.sav")
OUTPUT_PATH = os.path.join("data", "processed", "variable_audit.csv")

df, meta = pyreadstat.read_sav(RAW_DATA_PATH, apply_value_formats=False)

rows = []

for col in df.columns:
    variable_label = meta.column_names_to_labels.get(col, "")
    value_labels = meta.variable_value_labels.get(col, {})

    rows.append({
        "variable_name": col,
        "variable_label": variable_label,
        "value_labels": str(value_labels)
    })

audit_df = pd.DataFrame(rows)
audit_df.to_csv(OUTPUT_PATH, index=False)

print("Data loaded successfully.")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")
print(f"Variable audit saved to: {OUTPUT_PATH}")

print("\nCaregiver related variables:")
for col in df.columns:
    label = meta.column_names_to_labels.get(col, "")
    if "CAREGIV" in col.upper() or "caregiver" in label.lower() or "care" in label.lower():
        print(f"{col}: {label}")