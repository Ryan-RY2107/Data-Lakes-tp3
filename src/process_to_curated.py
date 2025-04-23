import pymysql
import pymongo
from transformers import AutoTokenizer
from datetime import datetime
from tqdm import tqdm


mysql_conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="staging",
    cursorclass=pymysql.cursors.DictCursor
)
cursor = mysql_conn.cursor()


cursor.execute("SELECT * FROM texts")
rows = cursor.fetchall()
cursor.close()
mysql_conn.close()

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["curated"]
mongo_collection = mongo_db["wikitext"]

mongo_collection.delete_many({})

for row in tqdm(rows, desc="Processing"):
    tokens = tokenizer(row["text"], truncation=True, padding=True, max_length=128)["input_ids"]
    document = {
        "split": row["split"],
        "text": row["text"],
        "tokens": tokens,
        "metadata": {
            "source": "mysql",
            "processed_at": datetime.utcnow().isoformat()
        }
    }
    mongo_collection.insert_one(document)

print(f"✅ Inserted {len(rows)} documents into MongoDB collection 'wikitext'")
