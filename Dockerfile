FROM python:3.10

COPY . /app/ticket_support_bot/
WORKDIR /app/ticket_support_bot/
RUN --mount=type=cache,target=/root/.cache/pip pip install -r /app/ticket_support_bot/requirements.txt

CMD ["python", "start.py"]
