FROM python:3.10
COPY . /opt/ticket_support_bot/
WORKDIR /opt/ticket_support_bot/

RUN pip3 install -r /opt/ticket_support_bot/requirements.txt
CMD ["python", "start.py"]
