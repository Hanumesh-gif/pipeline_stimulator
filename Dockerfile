FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for bioinformatics tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-jre-headless \
    samtools \
    wget \
    unzip \
    build-essential \
    libfontconfig1 \
    libharfbuzz0b \
    libxrender1 \
    libxtst6 \
    libxi6 \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Install FastQC
RUN wget -q https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.9.zip && \
    unzip -q fastqc_v0.11.9.zip && \
    chmod +x FastQC/fastqc && \
    ln -s /app/FastQC/fastqc /usr/local/bin/fastqc && \
    rm fastqc_v0.11.9.zip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

CMD ["gunicorn", "-b", "0.0.0.0:10000", "main:app"]