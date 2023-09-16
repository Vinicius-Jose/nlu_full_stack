FROM python:3.10

ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

RUN apt-get update \
    && apt-get install -y netcat-traditional

ENV APP=/app

# Change the workdir.
WORKDIR $APP


# Copy the rest of the files
COPY . $APP

RUN pip3 install poetry && poetry install --no-root


EXPOSE 8000

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/bin/bash","/app/entrypoint.sh"]

CMD ["poetry", "run","gunicorn", "--bind", ":8000", "--workers", "3", "djangobackend.wsgi"]