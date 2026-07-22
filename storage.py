import csv
import os

def save_to_csv(models: list, filepath: str, fieldnames: list):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for m in models:
            writer.writerow(m.to_dict())

    print(f"✅ 数据已写入: {filepath}")    
