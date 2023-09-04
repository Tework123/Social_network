FROM python:3.11

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1



RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN chmod +x /app/docker-entrypoint.sh

#CMD ["gunicorn", "-b", ":8000", "Social_network.wsgi:application"]

#CMD ["/app/docker-entrypoint.sh"]
#ENTRYPOINT ["/app/docker-entrypoint.sh"]
