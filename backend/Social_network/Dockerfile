FROM python:3.11

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1



RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

#COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

#COPY ./entrypoint.sh .


COPY . .

RUN chmod +x /app/entrypoint.sh
RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo

USER docker

#RUN ["chmod", "+x", "/app/entrypoint.sh"]


#CMD ["gunicorn", "-b", ":8000", "Social_network.wsgi:application"]

CMD ["/app/entrypoint.sh"]
ENTRYPOINT ["/app/entrypoint.sh"]
