# 🔍 JSON Duplicate Finder

This Python script detects duplicate records across multiple JSON files based on one or more user-defined keys. It's designed to be configurable, timestamped, and provide both machine-readable and human-readable reports.

---

## 📁 Project Structure

```
project/
├── config.json
├── find_duplicates.py
├── README.md
├── data/
│   ├── file1.json
│   ├── file2.json
│   └── ...
```

---

## ⚙️ Configuration

Edit the `config.json` file to define which files to process and which fields to use for identifying duplicates.

### Example:
```json
{
  "json_files": [
    "data/file1.json",
    "data/file2.json",
    "data/file3.json"
  ],
  "duplicate_keys": ["itemCode", "storeNum"]
}
```

- `json_files`: List of JSON files to be scanned (must be array of records).
- `duplicate_keys`: One or more keys that together define a unique row.

---

## 🚀 How to Run

Make sure you're using Python 3.7+.

### Step 1: Install dependencies (none required for base version)

```bash
pip install -r requirements.txt  # Optional - no third-party libraries needed
```

### Step 2: Run the script

```bash
python find_duplicates.py
```

---

## 📦 Output

Each run generates:

- `duplicates_<timestamp>.json` — full duplicate data
- `duplicates_<timestamp>.txt` — readable summary including:
  - File-by-file record count
  - Total records
  - Duplicate key summary
  - Actual duplicates

---

## ✅ Sample Console Output

```
📊 Summary
Total files checked: 3
  - data/file1.json: 120 record(s)
  - data/file2.json: 95 record(s)
  - data/file3.json: 140 record(s)
Combined total records: 355
Found 4 duplicate key(s), 9 total duplicate rows.
📁 JSON saved to: duplicates_2025-05-09_1640.json
📝 TXT summary saved to: duplicates_2025-05-09_1640.txt
```

---

## 🧪 Sample Data Format

Each file should contain a **JSON array** like:

```json
[
  { "itemCode": "A100", "storeNum": "S001", "qty": 5 },
  { "itemCode": "A101", "storeNum": "S002", "qty": 3 }
]
```

---

## 📌 Notes

- Fields with `null` or `missing` values for any `duplicate_keys` are **ignored** in duplication checks.
- You can run this script multiple times — results are saved with timestamped filenames.
- Handles JSON errors gracefully and skips unreadable or malformed files.

---

## 🛠️ Future Enhancements (Optional)

- Group duplicates by source file
- Support for nested JSON paths
- Interactive CLI or web UI

---

## 👨‍💻 Author

Sumit Mathur  
📧 srmathur@hotmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/sumit-mathur-3aa98b9/)
