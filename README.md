# Twitter-Airflow-DataEngineering-Project

Welcome to the **Twitter Airflow Data Engineering Project** repository! 🚀  
An end-to-end data engineering project that uses the X (Twitter) API to ingest public data, Apache Airflow for orchestration, and Python-based pipelines for data extraction, transformation, and storage. The system is deployed on an AWS EC2 instance, enabling hands-on experience with cloud infrastructure, workflow scheduling, and scalable data pipeline design.


---
## 🏗️ Architecture Overview

An AWS EC2 instance running Ubuntu is used as the primary compute environment. The instance is accessed securely via SSH from a local terminal and configured with all required system dependencies, Python packages, and a Python virtual environment.

Data ingestion is performed using the X (Twitter) API. A Python script (x_etl.py) connects to the API and retrieves public tweet data from the account Elon Musk. The extracted data is written directly to a CSV file, representing raw ingested data without transformation.

Apache Airflow is installed and configured on the EC2 instance to orchestrate the workflow. The EC2 instance is assigned appropriate IAM roles, allowing secure interaction with AWS services—specifically Amazon S3—without embedding credentials in code.

The ingestion script (x_etl.py) and the Airflow DAG definition (x_dag.py) are copied to the EC2 instance so they can be recognized and executed by Airflow. Once the DAG is triggered through the Airflow UI, it executes the ingestion process and uploads the resulting CSV file to an S3 bucket.

This architecture establishes a complete pipeline from external API ingestion to cloud-based object storage using industry-standard tools.

---
## 📖 Data Flow

This project involves:

1. A Python script (x_etl.py) authenticates with the X (Twitter) API.
2. Public tweet data from the account Elon Musk is retrieved via the API.
3. The retrieved data is written directly to a CSV file as raw output.
4. An AWS EC2 instance running Ubuntu serves as the execution environment.
5. Apache Airflow is installed and configured on the EC2 instance for orchestration.
6. IAM roles attached to the EC2 instance provide secure access to Amazon S3.
7. The Airflow DAG (x_dag.py) is recognized by Airflow and triggered via the UI.
8. During DAG execution, the CSV file generated from the API data is uploaded to an Amazon S3 bucket for persistent storage.

---

## 🚀 Tech Stack

1. Programming Language: Python
2. API: X (Twitter) API
3. Workflow Orchestration: Apache Airflow
4. Compute: AWS EC2 (Ubuntu)
5. Cloud Storage: Amazon S3
6. Security & Authentication: AWS IAM Roles
7. Data Format: CSV
8. Access Method: SSH
9. Environment Management: Python virtual environment (venv)

---

## 📂 Repository Structure
```
Twitter-Airflow-DataEngineering-Project/
├── scripts/                            # SQL scripts for ETL and transformations
│   ├── x_etl.py/                         # Python script to fetch tweet data from X API and write to CSV
│   ├── x_dag.py/                         # Apache Airflow DAG definition
├── README.md                           # Project overview and instructions
├── LICENSE                             # License information for the repository
```
---

## 🛡️ License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and share this project with proper attribution.

## 🌟 About Me

Hi there! I'm **Yashwanth Chenna Reddy Gotike**. I am currently pursuing an **MSc in Web and Data Science** at the University of Koblenz, with a strong passion for data engineering and a keen interest in developing scalable data solutions.
