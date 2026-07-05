FROM python:3.12-slim

RUN pip install --no-cache-dir uv==0.8.13

WORKDIR /code

# Copy the frontend dependencies and lockfile
COPY ./submission_frontend/pyproject.toml ./submission_frontend/uv.lock* ./submission_frontend/

# Copy the app directory (required by main.py) and the frontend source code
COPY ./app ./app
COPY ./submission_frontend/main.py ./submission_frontend/

# Install dependencies using uv
RUN cd submission_frontend && uv sync --frozen

EXPOSE 8080

CMD ["uv", "run", "--project", "submission_frontend", "uvicorn", "submission_frontend.main:app", "--host", "0.0.0.0", "--port", "8080"]
