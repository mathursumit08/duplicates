import json
from collections import defaultdict
from pathlib import Path
from datetime import datetime

# Load config
with open("config.json", "r") as f:
    config = json.load(f)

json_files = config.get("json_files", [])
dup_keys = config.get("duplicate_keys", [])
root_path = config.get("json_root_path", [])

if not json_files or not dup_keys:
    raise ValueError("Missing 'json_files' or 'duplicate_keys' in config")

# Create output directory
output_dir = Path("duplicates")
output_dir.mkdir(exist_ok=True)

# Extract nested list from root path (e.g., ["RecordSet", "Items"])
def extract_root(data, path):
    for key in path:
        if isinstance(data, dict):
            data = data.get(key)
        else:
            return None
    return data if isinstance(data, list) else None

# Normalize keys (case-insensitive, trimmed)
def build_composite_key(item, keys):
    try:
        return tuple(str(item.get(k)).strip().lower() for k in keys)
    except Exception:
        return tuple("MISSING" for _ in keys)

# Combine all data
combined_data = []
file_counts = {}

for filepath in json_files:
    path = Path(filepath)
    if not path.exists():
        print(f"[WARN] File not found: {filepath}")
        continue

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        try:
            data = json.load(f)
            records = extract_root(data, root_path) if root_path else data
            if isinstance(records, list):
                for record in records:
                    record["_source_file"] = str(filepath)
                    combined_data.append(record)
                file_counts[filepath] = len(records)
                print(f"[INFO] Loaded {len(records)} records from {filepath}")
            else:
                print(f"[WARN] No list found at path {root_path} in {filepath}")
        except json.JSONDecodeError as e:
            print(f"[ERROR] Failed to decode {filepath}: {e}")

total_records = len(combined_data)

# Detect duplicates
seen = defaultdict(list)
for item in combined_data:
    key = build_composite_key(item, dup_keys)
    if "MISSING" in key or None in key:
        continue
    seen[key].append(item)

duplicates = {k: v for k, v in seen.items() if len(v) > 1}
duplicate_count = sum(len(v) for v in duplicates.values())

# Output paths
timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
json_output = output_dir / f"duplicates_{timestamp}.json"
txt_output = output_dir / f"duplicates_{timestamp}.txt"

# Write JSON (convert key tuples to strings)
json_compatible_duplicates = {
    str(k): v for k, v in duplicates.items()
}
with open(json_output, "w", encoding="utf-8") as f_json:
    json.dump(json_compatible_duplicates, f_json, indent=2)

# Write TXT
with open(txt_output, "w", encoding="utf-8") as f_txt:
    f_txt.write(f"=== Duplicate Summary ===\n")
    f_txt.write(f"Files checked: {len(file_counts)}\n")
    f_txt.write(f"Total records combined: {total_records}\n")
    f_txt.write(f"Duplicate keys found: {len(duplicates)}\n")
    f_txt.write(f"Total duplicate rows: {duplicate_count}\n\n")

    f_txt.write("=== Records per File ===\n")
    for fname, count in file_counts.items():
        f_txt.write(f"{fname}: {count} record(s)\n")

    if duplicates:
        f_txt.write("\n=== Duplicates ===\n")
        for key, items in duplicates.items():
            f_txt.write(f"\nDuplicate Key: {key}\n")
            for i, item in enumerate(items, 1):
                source = item.get("_source_file", "unknown")
                f_txt.write(f"  #{i} (from {source}): {json.dumps(item, indent=2)}\n")
            f_txt.write("\n" + "-" * 40 + "\n")
    else:
        f_txt.write("\nNo duplicates found.\n")

# Console summary
print("\nSummary")
print(f"Files checked: {len(file_counts)}")
print(f"Total records: {total_records}")
print(f"Duplicate keys found: {len(duplicates)}")
print(f"Duplicate rows: {duplicate_count}")
print(f"JSON output: {json_output}")
print(f"TXT output:  {txt_output}")
