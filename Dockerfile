# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set environment variables
ENV BOT_TOKEN=5907195764:AAHjtXorzjiG6VZs8sj4c5ShUt1c3T3tBUU
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

RUN pip install --upgrade pip

# Install any dependencies required by your bot
RUN pip install -r requirements.txt

# Expose the port your bot listens on (if applicable)
EXPOSE 3000

# Run your bot when the container launches
CMD ["python3", "main.py"]
