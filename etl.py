import json
import os

# Define file paths using environment variables
INPUT_FILE = os.getenv('INPUT_FILE', 'input.json')
OUTPUT_FILE = os.getenv('OUTPUT_FILE', 'output.json')

def extract():
    """Extract data from a JSON file."""
    with open(INPUT_FILE, 'r') as file:
        data = json.load(file)
    return data

def transform(data):
    """Transform data."""
    # Example transformation: Add a new field
    data['transformed'] = True
    return data

def load(data):
    """Load data to a new JSON file."""
    with open(OUTPUT_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    """Run the ETL process."""
    data = extract()
    data = transform(data)
    load(data)
    print(f"Data processed and saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()




