
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 9093 available to the world outside the container
EXPOSE 9093

# Define the environment variable
ENV KAFKA_SERVER=kafka:9093

# Run consumer.py when the container launches
CMD ["python", "consumer.py"]
