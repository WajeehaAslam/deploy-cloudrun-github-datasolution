# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Cloud Run will use
EXPOSE 8080

# Set environment variables for database connection
ENV DB_USER=root
ENV DB_PASSWORD=pass
ENV DB_NAME=customer
ENV SQL_HOST=34.46.80.109

# Use the PORT environment variable provided by Cloud Run
ENV PORT=8080

# Run the application
CMD ["functions-framework", "--target=hello_http", "--port=${PORT}"]

