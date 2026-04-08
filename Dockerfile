# Dockerfile
# Builds a lightweight container for the Email Triage & Response Environment.
# Base image: official Python 3.10 slim (small footprint)

FROM python:3.10-slim

# -----------------------------------------------------------------------
# Set working directory inside the container
# -----------------------------------------------------------------------
WORKDIR /app

# -----------------------------------------------------------------------
# Copy dependency file and install dependencies first.
# Docker caches this layer, so re-builds are fast if requirements don't change.
# -----------------------------------------------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------------------------------------------------
# Copy all project source files into the container
# -----------------------------------------------------------------------
COPY env.py .
COPY tasks.py .
COPY grader.py .
COPY inference.py .
COPY openenv.yaml .

# -----------------------------------------------------------------------
# Default command: run the inference script
# Override with: docker run <image> python inference.py
# -----------------------------------------------------------------------
CMD ["python", "inference.py"]
