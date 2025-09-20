# Base image
FROM ubuntu:22.04

# Avoid interactive prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Set locale to avoid warnings
RUN apt-get update && apt-get install -y locales && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# Install tools and dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    ca-certificates \
    lsb-release \
    software-properties-common \
    wget \
    git \
    sudo \
    python3 \
    python3-pip \
    python3-venv

# --- Install Git LFS ---
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash && \
    apt-get update && apt-get install -y git-lfs && \
    git lfs install

# Create models directory (but don't download yet)
RUN mkdir -p /models

# Create download script that will run at container startup
RUN cat > /usr/local/bin/download-model.sh << 'EOF'
#!/bin/bash
set -e

MODEL_DIR="/models/Qwen3-Embedding-0.6B"

if [ ! -d "$MODEL_DIR/.git" ]; then
    echo "Downloading Qwen3-Embedding-0.6B model..."
    
    if [ -z "$HF_USERNAME" ] || [ -z "$HF_TOKEN" ]; then
        echo "Error: HF_USERNAME and HF_TOKEN environment variables must be set"
        exit 1
    fi
    
    # Clone the model
    git clone "https://${HF_USERNAME}:${HF_TOKEN}@huggingface.co/Qwen/Qwen3-Embedding-0.6B" "$MODEL_DIR"
    echo "Model download completed successfully"
else
    echo "Model already exists at $MODEL_DIR, skipping download"
fi
EOF

RUN chmod +x /usr/local/bin/download-model.sh

# Ensure scripts are executable by all users
RUN chmod 755 /usr/local/bin/download-model.sh 
# /usr/local/bin/setup-postgres.sh

# Add PostgreSQL APT repository
RUN echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
    curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
    apt-get update && apt-get install -y \
    postgresql-14 \
    postgresql-contrib \
    postgresql-14-pgvector

# Disable postgres password
RUN sed -i -E 's/\b(peer|md5|scram-sha-256)\b/trust/g' /etc/postgresql/14/main/pg_hba.conf

# Set environment variables for PostgreSQL
ENV PGDATA=/var/lib/postgresql/14/main

# Clean up
RUN rm -rf /var/lib/apt/lists/*

# Install Ollama (system-level daemon)
RUN curl -fsSL https://ollama.com/install.sh -o install-ollama.sh && \
    bash install-ollama.sh && \
    rm install-ollama.sh

# Create non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

# Give the vscode user ownership of the models directory
RUN chown -R $USERNAME:$USERNAME /models

# Switch to non-root user
USER $USERNAME
WORKDIR /home/$USERNAME

# Install Python packages
RUN pip3 install --upgrade pip && \
    pip3 install ollama sentence-transformers nltk sqlalchemy pgvector psycopg2-binary wikipedia

# Expose PostgreSQL default port
EXPOSE 5432