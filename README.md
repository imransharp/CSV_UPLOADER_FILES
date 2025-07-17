# CSV_UPLOADER_FILES
It uplods csv files 
# 📊 CSV Uploader for BI Data (Python)

## 📌 Purpose
Handles large CSV file uploads by splitting them into manageable chunks and inserting them into the database without timeout or performance issues.

This tool is used in a telecom BI (Business Intelligence) environment to efficiently upload and process millions of rows from CSV files.

---

## 🚀 Features

✅ Uploads large CSV files to MySQL database  
✅ Automatically splits files to prevent DB timeout  
✅ Batch inserts for optimized performance  
✅ Supports header mapping and validation  
✅ Command Line Interface (CLI) for scheduled runs

---

## 🔧 Tech Stack

- Python 3.x  
- Pandas  
- MySQL Connector  
- File Handling  
- CLI Environment

---

## 🏁 How It Works

1. Reads target CSV file from a given folder  
2. Splits the file into multiple parts (e.g., 50,000 rows each)  
3. Maps headers (e.g., `M_202312` → `Month_19`)  
4. Batch inserts each chunk into the database  
5. Moves the file to a `/processed` folder after successful import

---

## 💡 Real-World Impact

- Used for uploading 2.5M+ record files  
- Reduced DB timeout issues to zero  
- Enabled full BI ingestion without human intervention  
- Saved multiple hours per file upload session  
- Improved system reliability

---

## 📷 Screenshot (Optional)

*(Upload image showing folder layout or terminal success log)*

---

## 🚀 Future Improvements

- Add email alerts after completion  
- Convert to web-based dashboard for tracking progress  
- Add error tracking & retry mechanism

---

## 👤 Author

**Imran Bhatti** – Backend & Automation Engineer | [LinkedIn](https://www.linkedin.com/in/imransharp)  

