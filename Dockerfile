# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variables
ENV DATACODE_FILE=datacode.py
ENV PORT=8080

# Run datacode.py when the container launches
CMD ["python", "datacode.py"]


