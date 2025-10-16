# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Expose port
EXPOSE 8080

# Run Flask with Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
