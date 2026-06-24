# Geotechnical Laboratory Report Data Extraction Pipeline

## Overview

This project is a Python-based automated data extraction pipeline designed to process geotechnical laboratory reports in PDF format and convert them into a standardized tabular dataset.

The primary objective is to extract relevant geotechnical information from laboratory reports that may vary in layout and formatting while maintaining a fixed output structure. The extracted data is then exported to a CSV file for further analysis and processing.

The solution was developed as part of a technical assessment focused on handling heterogeneous PDF reports and transforming unstructured document content into structured data.

---

## Project Objective

The pipeline extracts key geotechnical parameters from PDF reports and maps them into a standardized table containing fields such as:

* Sample Number
* Location
* Sample Depth
* Material
* Soil Description
* Liquid Limit (LL)
* Plastic Limit (PL)
* Plasticity Index (PI)
* Linear Shrinkage (LS)
* Fine Soil / Fines Percentage
* Sand Percentage
* Gravel Percentage
* Geological Unit
* Page Number

The output schema remains consistent regardless of report formatting variations.

---

## Approach

Instead of relying on fixed page coordinates or absolute positions, the solution uses:

* Text extraction using `pdfplumber`
* Keyword-based identification
* Regular expression (RegEx) pattern matching
* Multi-page sample aggregation
* Missing-value handling

This approach improves robustness when processing reports with varying layouts and structures.

---

## Processing Flow

```text
User provides PDF
        │
        ▼
PDF opened using pdfplumber
        │
        ▼
Text extracted from each page
        │
        ▼
Text cleaning and normalization
        │
        ▼
Keyword and RegEx-based extraction
        │
        ▼
Data mapped to standard schema
        │
        ▼
Multi-page records merged
        │
        ▼
Structured dataset generated
        │
        ▼
CSV file exported
```

### Detailed Workflow

1. User places the PDF report in the project directory.
2. The script opens the PDF and processes it page by page.
3. Text content is extracted from each page.
4. Extracted text is cleaned and normalized.
5. Regular expressions identify and extract required fields.
6. Records belonging to the same sample are merged across multiple pages.
7. Missing values are preserved as empty fields without causing failures.
8. All extracted records are written into a structured CSV file.

---

## Project Structure

```text
project/
│
├── main.py
├── requirements.txt
├── README.md
├── Lab Results-Geotechnical-Factual-Report.pdf
└── geotech_clean_summary6.csv
```

---

## Requirements

* Python 3.10 or newer (latest stable version recommended)
* pip package manager

### Python Dependencies

```text
pdfplumber
```

---

## Setup Guide

### 1. Clone the Project

```bash
git clone https://github.com/ujjwalnp/automated_data_extraction
cd automated_data_extraction
```


---

### 2. Place PDF File

Copy the input PDF file into the same directory as `main.py`.

Example:

```text
project/
│
├── main.py
├── Lab Results-Geotechnical-Factual-Report.pdf
```

---

### 3. Create a Virtual Environment

Linux / macOS:

```bash
python3 -m venv venv
```

Windows:

```bash
python -m venv venv
```

---

### 4. Activate the Virtual Environment

Linux / macOS:

```bash
source venv/bin/activate
```

Windows (Command Prompt):

```cmd
venv\Scripts\activate
```

Windows (PowerShell):

```powershell
.\venv\Scripts\Activate.ps1
```

---

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```


---

### 6. Run the Script

```bash
python main.py
```

---

## Output

After successful execution, the script generates:

```text
geotech_report_summary.csv
```

---

## Error Handling

The pipeline is designed to be fault tolerant.

If a field cannot be found:

* The extraction process continues.
* The field remains empty.
* The script does not terminate unexpectedly.


---

## Limitations

Although the solution is designed to be robust, several limitations exist:

### 1. Text-Based PDFs Only

The current implementation assumes that text can be extracted directly from the PDF.

Scanned PDFs or image-only reports are not supported and would require OCR integration (e.g., Tesseract OCR).

### 2. Dependency on Keywords

Extraction relies on keywords such as:

* Sample Number
* Sample Location
* Material
* Soil Description
* Liquid Limit

Significant terminology changes may require updates to extraction patterns.

### 3. Formatting Variations

Extreme formatting differences may impact extraction accuracy if field labels differ substantially from expected patterns.

### 4. Limited Table Understanding

The current implementation primarily uses text and pattern matching.

Complex embedded tables may require specialized table extraction libraries such as:

* Camelot
* Tabula
* pdfplumber table extraction

### 5. Geological Unit

The Geological Unit field currently defaults to:

```text
See Engineering Logs
```

because the required information is not consistently available within the laboratory report pages.

### 6. Graphs and Charts

The pipeline cannot analyze graphs, plots, or charts.

It is designed for text extraction only, so any information contained visually inside figures, trend charts, or graphical summaries will not be captured unless additional OCR or image analysis is added.

---

## Future Improvements

Potential enhancements include:

* OCR support for scanned PDFs
* Configurable extraction rules using JSON/YAML
* Advanced table extraction
* Confidence scoring for extracted values
* Validation and quality checks
* Support for JSON output format
* Automated unit and integration testing
* Graph and chart interpretation using image analysis or OCR-based workflows

---

## Technologies Used

* Python
* pdfplumber
* Regular Expressions (RegEx)
* CSV Processing

---

## Author

Developed as part of a technical assessment focused on automated extraction of structured geotechnical laboratory data from heterogeneous PDF reports.
