# Use the official Python image as the base image
FROM python:3.10

# Set the working directory within the container
WORKDIR /app

# Copy the application code to the container
COPY . /app

# Install any required Python packages using pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your application will run on (if needed)
EXPOSE 5000

# Run your Python application
CMD ["python", "main.py"]
