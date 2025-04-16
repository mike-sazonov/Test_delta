FROM python:3.12-slim as base

WORKDIR ./

COPY uv.lock pyproject.toml .

RUN pip install uv
RUN uv sync

COPY . .

# CMD ["uv", "run", "main.py"]
