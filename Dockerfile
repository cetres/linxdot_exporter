FROM python:3.10-slim

RUN pip install --no-cache-dir linxdot_exporter

CMD ["python", "-m" , "linxdot_exporter"]