FROM python:3.10

# Install system dependencies
RUN apt-get update && apt-get install -y libgl1

# Optional: Set YOLO config dir to avoid Ultralytics warning
ENV YOLO_CONFIG_DIR=/tmp

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
