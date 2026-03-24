# Cyber Security & Compliance Data Analytics Project

## 🛡️ Project Overview
This project is an advanced data analytics solution designed for Managed Service Providers (MSPs) like **PC Consultants**. It simulates a real-world scenario where security data is analyzed to provide business-critical insights into corporate safety and compliance.

The project analyzes over **60,000 security events** for **1,000 employees** and visualizes key metrics such as MFA adoption, device health (patching), and the effectiveness of security awareness training.

## 🚀 Features
- **Data Generation:** Custom Python script to generate realistic corporate security logs.
- **SQL Database:** SQLite database with indexed tables for high-performance querying.
- **Business Intelligence:** Pre-written SQL queries to calculate core Security KPIs.
- **Scalability:** Handles large volumes of data while maintaining performance.

## 📊 Key Insights (KPIs)
- **MFA Adoption Rate:** Identifies security gaps in critical services (Email, VPN, Cloud).
- **Patch Compliance:** Tracks outdated devices by department to prioritize updates.
- **Risk Segmentation:** Highlights departments with high phishing risk (Sales, Marketing).
- **Training Effectiveness:** Correlates security training completion with the reduction of security incidents.

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Libraries:** Pandas, SQLite3
- **SQL:** SQLite
- **Visualization:** Power BI (Recommended for connecting to the generated `.db` file)

## 📁 Project Structure
- `generate_security_data.py`: Script to generate 60k records of CSV data.
- `setup_sqlite.py`: Script to create the SQLite database and import CSV files.
- `analytical_queries.sql`: A collection of SQL queries for business reporting.
- `CyberSecurity.db`: The resulting database (generated locally).

## 📝 How to Use
1. Clone this repository.
2. Install requirements: `pip install pandas`.
3. Run the generator: `python generate_security_data.py`.
4. Build the database: `python setup_sqlite.py`.
5. Run analytical queries in your preferred SQL client.

---
*Created as part of a Data Analytics Portfolio for companies like PC Consultants & Carnival UK.*
