FROM python:3.10-slim

# Install Poetry
RUN pip install poetry

# Set working directory
WORKDIR /pilottai-tools

# Copy and install dependencies
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root

# Copy source code
COPY . .

# Install the framework itself
RUN poetry install

# Default command shows the version
CMD ["python", "-c", "import pilottai_tools; print(pilottai_tools.__version__)"]
