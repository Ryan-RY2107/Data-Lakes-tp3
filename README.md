# 🚀 Data-Lakes-TP3

A full-stack data pipeline integrating SQL and NoSQL for modern data lake architecture, leveraging **LocalStack**, **MySQL**, and **MongoDB**.

---

## 🧠 Features

- ✅ Download and preprocess [WikiText V2](https://huggingface.co/datasets/wikitext)
- ✅ Local data lake emulated with **LocalStack (S3)**
- ✅ Structured staging zone using **MySQL**
- ✅ Curated zone using **MongoDB** with tokenized data
- ✅ Tokenization powered by 🤗 Transformers (`distilbert-base-uncased`)

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Ryan-RY2107/Data-Lakes-tp3.git
cd Data-Lakes-tp3
```

### 2. Start required services

```bash
docker-compose up -d

# Start MySQL container if not already running
docker run --name mysql \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=staging \
  -p 3306:3306 -d mysql:latest
```

### 3. Create S3 buckets in LocalStack

```bash
aws --endpoint-url=http://localhost:4566 s3 mb s3://raw
aws --endpoint-url=http://localhost:4566 s3 mb s3://staging
aws --endpoint-url=http://localhost:4566 s3 mb s3://curated
```

---

## 🔁 Pipeline Execution

### Step 1️⃣: Download and upload WikiText data to raw

```bash
python src/unpack_data.py --bucket_name raw --output_file combined_raw.csv
```

### Step 2️⃣: Clean data and insert into MySQL staging database

```bash
python src/preprocess_to_staging.py --bucket_raw raw --input_file combined_raw.csv
```

### Step 3️⃣: Tokenize and insert into MongoDB curated collection

```bash
python src/process_to_curated.py
```

---

## 📦 Requirements

- Python 3.9+
- Docker & Docker Compose
- AWS CLI (configured for LocalStack)
- Install dependencies:

```bash
pip install pandas boto3 localstack-client pymongo transformers pymysql mysql-connector-python datasets
```

---

## 💾 Sample Document (MongoDB)

```json
{
  "split": "train",
  "text": "This is a sample sentence.",
  "tokens": [2023, 2003, 1037, 7099, 6251, 1012],
  "metadata": {
    "source": "mysql",
    "processed_at": "2025-04-23T12:34:56.789Z"
  }
}
```

---

## 👤 Author

Developed by [@Ryan-RY2107](https://github.com/Ryan-RY2107)

---

## 🏁 Next Steps

- [ ] Package the project as a DVC pipeline
- [ ] Add `requirements.txt` for reproducibility
- [ ] Build a Streamlit dashboard to visualize curated data
- [ ] Expose MongoDB results via API using FastAPI/Flask

---

⭐ If you find this project helpful, feel free to fork, star, or contribute!
