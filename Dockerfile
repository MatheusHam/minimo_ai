# Base image, you can change it as you want
FROM python:3.10-slim-buster

# Install necessary system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libblas3 \
        liblapack3 \
        libopenblas-dev \
        liblapack-dev \
        libatlas-base-dev \
        gfortran \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
WORKDIR /app
ARG PIP_EXTRA_INDEX_URL="https://download.pytorch.org/whl/cpu"
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

# Set the working directory inside the container
WORKDIR /app

# Copy the example.py file into the container
COPY /app/example.py .
COPY .env .


# Run the example.py file when the container starts
CMD ["python", "example.py"]
