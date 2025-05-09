import json
from collections import defaultdict
from pathlib import Path
from datetime import datetime

# Load config
with open("config.json", "r") as f:
    config = json.load(f)

json_files = config.get("json_files", [])
dup_keys = config.get("duplicate_keys", [])

if not json_files or not dup_keys:
    raise ValueError("Missing 'json_files' or 'duplicate_keys' in config")

# --- Load and Combine JSON ---
combined_data = []
file_counts = {}  # file -> number of records

for filepath in json_files:
    path = Path(filepath)
    if not path.exists():
        print(f"⚠️ File not found: {filepath}")
        continue
    with open(path, "r") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                combined_data.extend(data)
                file_counts[filepath] = len(data)
            else:
                print(f"⚠️ File does not contain a list: {filepath}")
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error in {filepath}: {e}")

total_records = len(combined_data)

# --- Find Duplicates ---
seen = defaultdict(list)

def build_composite_key(item, keys):
    return tuple(item.get(k) for k in keys)

for item in combined_data:
    key = build_composite_key(item, dup_keys)
    if None not in key:
        seen[key].append(item)

duplicates = {k: v for k, v in seen.items() if len(v) > 1}
duplicate_count = sum(len(v) for v in duplicates.values())

# --- File outputs ---
timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
json_output = f"duplicates_{timestamp}.json"
txt_output = f"duplicates_{timestamp}.txt"

# JSON
with open(json_output, "w") as f_json:
    json.dump(duplicates, f_json, indent=2)

# TXT
with open(txt_output, "w") as f_txt:
    f_txt.write(f"=== Duplicate Summary ===\n")
    f_txt.write(f"Checked files: {len(file_counts)}\n")
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
                f_txt.write(f"  #{i}: {json.dumps(item, indent=2)}\n")
            f_txt.write("\n" + "-" * 40 + "\n")
    else:
        f_txt.write("\n✅ No duplicates found.\n")

# Console
print(f"\n📊 Summary")
print(f"Total files checked: {len(file_counts)}")
for fname, count in file_counts.items():
