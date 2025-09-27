import boto3
import csv
import io
import os
import time

s3 = boto3.client("s3", region_name="ap-southeast-1")

def lambda_handler(event, context):
    try:
        if "Records" in event:
            bucket = event["Records"][0]["s3"]["bucket"]["name"]
            key = event["Records"][0]["s3"]["object"]["key"]
        else:
            bucket = os.environ.get("BUCKET_NAME", "team3-titanic-data")
            key = "processed/titanic_clean.csv"

        print(f"Processing file: s3://{bucket}/{key}")


        obj = s3.get_object(Bucket=bucket, Key=key)
        csv_content = obj["Body"].read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(csv_content))

        processed_rows = []
        for row in reader:

            row["Age"] = row.get("Age") or "30"     
            row["Fare"] = row.get("Fare") or "15"  

            if "Survived" not in row or row["Survived"] == "":
                row["Survived"] = "0"

            sex_value = row.get("Sex", "").strip().lower()
            row["Sex"] = "1" if sex_value == "female" else "0"

            processed_row = {
                "Pclass": row.get("Pclass", "3"),
                "Sex": row["Sex"],
                "Age": row["Age"],
                "Fare": row["Fare"],
                "SibSp": row.get("SibSp", "0"),
                "Parch": row.get("Parch", "0"),
                "Survived": row["Survived"]
            }
            processed_rows.append(processed_row)

        if not processed_rows:
            print("No valid rows to process")
            return {"statusCode": 400, "body": "No valid rows to process"}

        timestamp = int(time.time())
        processed_key = key.replace("raw/", f"processed/{timestamp}_")

        out_buffer = io.StringIO()
        writer = csv.DictWriter(out_buffer, fieldnames=processed_rows[0].keys())
        writer.writeheader()
        writer.writerows(processed_rows)

        s3.put_object(Bucket=bucket, Key=processed_key, Body=out_buffer.getvalue())

        print(f" Processed file saved to s3://{bucket}/{processed_key}")

        return {"statusCode": 200, "body": f"Processed {key} successfully"}

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"statusCode": 500, "body": str(e)}

    return {"statusCode": 200, "body": "Hello from Lambda!"}
    
