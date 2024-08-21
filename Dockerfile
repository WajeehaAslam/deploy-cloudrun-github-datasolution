# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Google Cloud Functions Framework
RUN pip install functions-framework google-cloud-storage mysql-connector-python

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Set environment variables
ENV PORT=8080

# Run the function when the container launches
CMD ["functions-framework", "--target", "hello_http"]
