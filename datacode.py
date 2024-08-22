import os
import functions_framework
import json
import csv
from google.cloud import storage
import mysql.connector

# Initialize clients
storage_client = storage.Client()

# Set environment variables for Cloud SQL connection
DB_USER = 'root'
db_password = 'pass'
DB_NAME = 'customer'
sql_host = '34.46.80.109'

def read_csv_from_gcs(bucket_name, file_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    content = blob.download_as_text()

    # Parse CSV content
    csv_reader = csv.DictReader(content.splitlines())
    return list(csv_reader)

def read_json_from_gcs(bucket_name, file_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    content = blob.download_as_text()

    # Parse JSON content
    return json.loads(content)

def read_from_cloud_sql():
    # Connect to the Cloud SQL instance
    cnx = mysql.connector.connect(
        user=DB_USER,
        password=db_password,
        database=DB_NAME,
        host=sql_host
    )

    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM sample_table;")
    result = cursor.fetchall()
    cnx.close()

    return result

def upload_json_to_gcs(bucket_name, file_name, data):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Convert data to JSON string and upload to GCS
    blob.upload_from_string(json.dumps(data), content_type='application/json')

@functions_framework.http
def hello_http(request):
    try:
        # Get the bucket name from environment variable or request
        bucket_name = 'customers_products_prices'
        
        # Fetch and read CSV and JSON files from GCS bucket
        csv_data = read_csv_from_gcs(bucket_name, 'data.csv')
        json_data = read_json_from_gcs(bucket_name, 'json.JSON')
        
        # Fetch data from Cloud SQL
        sql_data = read_from_cloud_sql()

        # Combine all data into a JSON structure
        combined_data = {
            "csv_data": csv_data,
            "json_data": json_data,
            "sql_data": sql_data
        }

        # Upload combined data as JSON to GCS
        upload_json_to_gcs(bucket_name, 'output-file.json', combined_data)

        return "Data combined and uploaded successfully."

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    # Ensure the application listens on the correct port
    port = int(os.environ.get("PORT", 8080))
    functions_framework.run("hello_http", port=port)





