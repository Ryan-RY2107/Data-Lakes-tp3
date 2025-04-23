import argparse
import boto3
import pandas as pd
from datasets import load_dataset

def save_combined_wikitext(dataset, output_path):
    combined = []
    for split in ['train', 'test', 'validation']:
        texts = dataset[split]['text']
        df = pd.DataFrame({'split': split, 'text': texts})
        combined.append(df)
    full_df = pd.concat(combined, ignore_index=True)
    full_df = full_df[full_df['text'].str.strip() != '']  # 去除空行
    full_df.to_csv(output_path, index=False)
    print(f"Saved combined data to {output_path}")

def upload_to_s3(local_file, bucket_name, s3_key):
    s3 = boto3.client('s3', endpoint_url="http://localhost:4566")
    s3.upload_file(local_file, bucket_name, s3_key)
    print(f"Uploaded {local_file} to s3://{bucket_name}/{s3_key}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket_name", type=str, required=True)
    parser.add_argument("--output_file", type=str, default="combined_raw.csv")
    args = parser.parse_args()

    print("Downloading WikiText dataset...")
    dataset = load_dataset("wikitext", "wikitext-2-raw-v1")
    save_combined_wikitext(dataset, args.output_file)
    upload_to_s3(args.output_file, args.bucket_name, args.output_file)
