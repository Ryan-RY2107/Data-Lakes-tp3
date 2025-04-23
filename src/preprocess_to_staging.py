import argparse
import pandas as pd
import pymysql
import boto3
from io import StringIO

def download_from_s3(bucket_name, key):
    s3 = boto3.client("s3", endpoint_url="http://localhost:4566")
    response = s3.get_object(Bucket=bucket_name, Key=key)
    content = response["Body"].read().decode("utf-8")
    return pd.read_csv(StringIO(content))

def clean_data(df):
    df = df.drop_duplicates()
    df = df[df['text'].str.strip() != '']
    return df

def save_to_mysql(df, host, user, password, db):
    conn = pymysql.connect(host=host, user=user, password=password, database=db)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS texts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            split VARCHAR(10),
            text TEXT
        )
    """)
    for _, row in df.iterrows():
        cursor.execute("INSERT INTO texts (split, text) VALUES (%s, %s)", (row['split'], row['text']))
    conn.commit()
    conn.close()
    print(f"Inserted {len(df)} rows into MySQL.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket_raw", type=str, required=True)
    parser.add_argument("--db_host", type=str, default="localhost")
    parser.add_argument("--db_user", type=str, default="root")
    parser.add_argument("--db_password", type=str, default="root")
    parser.add_argument("--db_name", type=str, default="staging")
    parser.add_argument("--input_file", type=str, default="combined_raw.csv")
    args = parser.parse_args()

    df = download_from_s3(args.bucket_raw, args.input_file)
    df = clean_data(df)
    save_to_mysql(df, args.db_host, args.db_user, args.db_password, args.db_name)
