# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of your application's code into the container
COPY . .

RUN dir -s
# Run your Telegram bot script when the container launches
# ENTRYPOINT  ["ls"]
CMD ["python3", "-u", "main.py"]
