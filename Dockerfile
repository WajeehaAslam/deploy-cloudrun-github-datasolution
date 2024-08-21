# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt || true

# Define environment variables for file paths
ENV INPUT_FILE=input.json
ENV OUTPUT_FILE=output.json

# Run etl.py when the container launches
CMD ["python", "etl.py"]
