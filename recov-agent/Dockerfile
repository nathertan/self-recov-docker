FROM python:3.9-slim

WORKDIR /app
RUN pip install docker requests

COPY recov-agent.py .
CMD ["python", "recov-agent.py"]