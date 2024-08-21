# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for the Flask app to be accessible
EXPOSE 8080

# Set the environment variables for database connection
ENV DB_USER=root
ENV DB_PASSWORD=pass
ENV DB_NAME=customer
ENV SQL_HOST=34.46.80.109

# Run the application
CMD ["functions-framework", "--target=hello_http", "--port=8080"]

