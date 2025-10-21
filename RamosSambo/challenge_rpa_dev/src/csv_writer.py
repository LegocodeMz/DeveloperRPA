import csv
import os
from datetime import datetime

def write_to_csv(data, output_path="./output"):
    os.makedirs(output_path, exist_ok=True)
    filename = f"{output_path}/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["nome", "email", "contacto", "estado_civil", "salario"])
        writer.writeheader()
        writer.writerows(data)

    return filename
