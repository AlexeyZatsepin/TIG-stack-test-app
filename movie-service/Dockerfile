# Use a slim Python base image
FROM python:3.9-slim-buster

# Set environment variables (best practice)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy only requirements.txt first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code (after dependencies)
COPY . .

# Install gunicorn (if not already in requirements.txt)
RUN pip install gunicorn

# Expose the Flask app port
EXPOSE 9000

# Run the Flask app using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:9000", "app:app"]