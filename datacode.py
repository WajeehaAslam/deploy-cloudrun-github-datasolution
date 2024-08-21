import os
import functions_framework
import json
import csv
from google.cloud import storage
import mysql.connector

# Initialize clients
storage_client = storage.Client()

# Set environment variables for Cloud SQL connection
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'pass')
DB_NAME = os.getenv('DB_NAME', 'customer')
SQL_HOST = os.getenv('SQL_HOST', '34.46.80.109')

# Retrieve PORT environment variable
PORT = os.getenv('PORT', '8080')
print(f"PORT is set to: {PORT}")

def read_csv_from_gcs(bucket_name, file_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    content = blob.download_as_text()
    csv_reader = csv.DictReader(content.splitlines())
    return list(csv_reader)

def read_json_from_gcs(bucket_name, file_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    content = blob.download_as_text()
    return json.loads(content)

def read_from_cloud_sql():
    cnx = mysql.connector.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=SQL_HOST
    )
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM sample_table;")
    result = cursor.fetchall()
    cnx.close()
    return result

def upload_json_to_gcs(bucket_name, file_name, data):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(json.dumps(data), content_type='application/json')

@functions_framework.http
def hello_http(request):
    try:
        bucket_name = 'customers_products_prices'
        csv_data = read_csv_from_gcs(bucket_name, 'data.csv')
        json_data = read_json_from_gcs(bucket_name, 'json.JSON')
        sql_data = read_from_cloud_sql()

        combined_data = {
            "csv_data": csv_data,
            "json_data": json_data,
            "sql_data": sql_data
        }

        upload_json_to_gcs(bucket_name, 'output-file.json', combined_data)
        return "Data combined and uploaded successfully."

    except Exception as e:
        return f"Error: {str(e)}", 500


