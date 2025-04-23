# Data-Lakes-TP3 🚀

A full-stack data pipeline integrating SQL and NoSQL for building a modern data lake architecture using **LocalStack**, **MySQL**, and **MongoDB**.

## 📁 Project Structure


## 🧠 Features

- ✅ Download and preprocess [WikiText V2](https://huggingface.co/datasets/wikitext)
- ✅ Local data lake emulated with **LocalStack (S3)**
- ✅ Structured staging data with **MySQL**
- ✅ Curated tokenized data with **MongoDB**
- ✅ Tokenization via 🤗 Transformers (`distilbert-base-uncased`)

## 🛠️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/Ryan-RY2107/Data-Lakes-tp3.git
cd Data-Lakes-tp3

### 2. Start services

'''bash
docker-compose up -d
docker run --name mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=staging -p 3306:3306 -d mysql:latest
