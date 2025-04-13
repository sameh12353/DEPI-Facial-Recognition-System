FROM python:3.12.9-slim

# Set working directory
WORKDIR /project

# Copy project files into the container
COPY . /project

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
