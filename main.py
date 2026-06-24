import pdfplumber
import re
import csv
import json

def clean_extracted_line(text):
    if not text:
        return ""
    # Strip JSON/CSV escape character fragments injected during extraction
    return text.replace('"', '').replace("'", "").replace('\r', '').strip()

def parse_geotech_page(text, page_num):
    raw_lines = text.split('\n')
    lines = [clean_extracted_line(line) for line in raw_lines if line.strip()]
    full_text_flattened = " ".join(lines)
    
    # 1. Identify Unique Sample Target Row
    sample_match = re.search(r'Sample\s+Number:\s*([A-Z0-9\-]+)', full_text_flattened, re.IGNORECASE)
    if not sample_match:
        return None
    s_id = sample_match.group(1).strip()
    
    data = {
        "Sample Number": s_id, "Location": "", "Sample Depth (m)": "", 
        "Material": "", "Soil Description": "",
        "LL": "", "PL": "", "PI": "", "LS": "",
        "Fine S / Fines (%)": "", "Sand (%)": "", "Gravel (%)": "",
        "Geological unit": "See Engineering Logs", "Page Number": str(page_num)
    }

    # 2. Extract Location Bounded to Exclude Document Headers
    loc_match = re.search(r'Sample\s+Location:\s*([^,\(]+)', full_text_flattened, re.IGNORECASE)
    if loc_match:
        data["Location"] = loc_match.group(1).strip()

    # 3. Dynamic Parenthetical vs Direct Depth Resolution Fix
    depth_direct = re.search(r'\bDepth:\s*([\d\.\s-]+)\s*m', full_text_flattened, re.IGNORECASE)
    depth_paren = re.search(r'BH\s*\d+\s*\(\s*([\d\.\s-]+)\s*m?\s*\)', full_text_flattened, re.IGNORECASE)
    
    if depth_direct:
        data["Sample Depth (m)"] = depth_direct.group(1).strip()
    elif depth_paren:
        data["Sample Depth (m)"] = depth_paren.group(1).strip()

    # 4. Content-Bounded Multi-Line Extraction for Material and Soil Description
    for line in lines:
        if line.lower().startswith("material:"):
            mat_val = re.sub(r'(?i)^material:\s*', '', line).strip()
            mat_val = re.split(r'(?i)\b(particle|sieve|depth|report)\b', mat_val)[0]
            data["Material"] = mat_val.strip(", ")
            
        if "soil description" in line.lower():
            soil_val = re.sub(r'(?i).*?soil\s+description\s*', '', line).strip()
            soil_val = re.split(r'(?i)\b(nature|moisture|temperature|report)\b', soil_val)[0]
            data["Soil Description"] = soil_val.strip(", :")

    # 5. Extract Atterberg Limits (Strictly bound LS to its unit to bypass standard noise)
    limits_map = {
        "LL": r'Liquid\s+Limit.*?(\d+|Not\s+Obtainable)',
        "PL": r'Plastic\s+Limit.*?(\d+|Not\s+Obtainable)',
        "PI": r'Plasticity\s+Index.*?(\d+|Non\s+Plastic)',
        "LS": r'Linear\s+Shrinkage\s*\(%\)\s*([\d\.]+)'  # Captures only after the explicit (%) column label
    }
    for key, pattern in limits_map.items():
        m = re.search(pattern, full_text_flattened, re.IGNORECASE)
        if m:
            data[key] = m.group(1).strip()

    # 6. Particle Sieve Distribution Calculation Logic
    p236 = re.search(r'2\.36\s*mm\s+(\d+)', full_text_flattened, re.IGNORECASE)
    p075 = re.search(r'0\.075\s*mm\s+(\d+)', full_text_flattened, re.IGNORECASE)
    
    if p075:
        data["Fine S / Fines (%)"] = p075.group(1).strip()
    if p236 and p075:
        try:
            fines = int(p075.group(1))
            total_236 = int(p236.group(1))
            data["Gravel (%)"] = str(100 - total_236)
            data["Sand (%)"] = str(total_236 - fines)
        except ValueError:
            pass

    return data

def execute_pipeline(pdf_path, csv_output_path):
    aggregated_records = {}

    with pdfplumber.open(pdf_path) as pdf:
        for idx, page in enumerate(pdf.pages):
            page_num = idx + 1
            text = page.extract_text()
            if not text:
                continue

            parsed_row = parse_geotech_page(text, page_num)
            if parsed_row:
                s_id = parsed_row["Sample Number"]
                
                if s_id not in aggregated_records:
                    aggregated_records[s_id] = parsed_row
                else:
                    if str(page_num) not in aggregated_records[s_id]["Page Number"]:
                        aggregated_records[s_id]["Page Number"] += f", {page_num}"
                    
                    for col, value in parsed_row.items():
                        if not aggregated_records[s_id][col] and value:
                            aggregated_records[s_id][col] = value

    columns = [
        "Sample Number", "Location", "Sample Depth (m)", "Material", "Soil Description",
        "LL", "PL", "PI", "LS", "Fine S / Fines (%)", "Sand (%)", "Gravel (%)",
        "Geological unit", "Page Number"
    ]
    with open(csv_output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(aggregated_records.values())

if __name__ == "__main__":
    execute_pipeline("Lab Results-Geotechnical-Factual-Report.pdf", "geotech_report_summary.csv")