# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# # Make port 80 available to the world outside this container
# EXPOSE 80

# Define environment variable
ENV BOT_TOKEN=your_token_here

# Run app.py when the container launches
CMD ["python", "app/app.py"]