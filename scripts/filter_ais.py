import pandas as pd
import os

# ── Config ──────────────────────────────────────────────
INPUT_FILE = r"/Users/imadsharof/Library/Mobile Documents/com~apple~CloudDocs/Cours/MA1/Geospatial Web/MaaSDB-Eval-2026/data/raw/aisdk-2026-04-09.csv"
OUTPUT_DIR = r"/Users/imadsharof/Library/Mobile Documents/com~apple~CloudDocs/Cours/MA1/Geospatial Web/MaaSDB-Eval-2026/data/processed"

TIME_START = "10:00"
TIME_END   = "10:30"
SIZES      = [5, 10, 20]
# ────────────────────────────────────────────────────────

print("Reading CSV... (this may take a moment)")
df = pd.read_csv(INPUT_FILE, low_memory=False)
print(f"  Loaded {len(df):,} rows")

# Normalize column names (strip spaces, lowercase)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("/", "_")
print(f"  Columns: {df.columns.tolist()}")

# Find the timestamp column
ts_col = next((c for c in df.columns if "timestamp" in c or "time" in c), None)
if not ts_col:
    raise ValueError("Could not find a timestamp column. Check your column names above.")

# Parse timestamps
df[ts_col] = pd.to_datetime(df[ts_col], dayfirst=True, errors="coerce")
df = df.dropna(subset=[ts_col])

# Filter 10:00 to 10:30
mask = (df[ts_col].dt.time >= pd.Timestamp(TIME_START).time()) & \
       (df[ts_col].dt.time <= pd.Timestamp(TIME_END).time())
df_filtered = df[mask].copy()
print(f"  Rows in 10:00-10:30 window: {len(df_filtered):,}")

# Find MMSI column
mmsi_col = next((c for c in df.columns if "mmsi" in c), None)
if not mmsi_col:
    raise ValueError("Could not find MMSI column.")

# Get all unique ships in that window
all_ships = df_filtered[mmsi_col].dropna().unique()
print(f"  Unique ships in window: {len(all_ships)}")

# Output one file per size
for n in SIZES:
    if len(all_ships) < n:
        print(f"  WARNING: only {len(all_ships)} ships available, skipping size {n}")
        continue

    selected_ships = all_ships[:n]
    out = df_filtered[df_filtered[mmsi_col].isin(selected_ships)].copy()

    filename = os.path.join(OUTPUT_DIR, f"ais_10h_ships{n}.csv")
    out.to_csv(filename, index=False)
    print(f"  Saved {n} ships ({len(out):,} rows) → {filename}")

print("\nDone! You now have 3 filtered CSV files ready.")
