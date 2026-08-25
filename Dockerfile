FROM python:3.9-slim-bookworm
WORKDIR /app

# 1. Install system utilities
RUN apt update -y && apt install awscli -y

# 2. Copy and install Python dependencies (cached layer)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy the rest of the application code
COPY . /app

# 4. Command to run your app
CMD ["python3", "app.py"]
