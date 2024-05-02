FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /vms_project

COPY requirements.txt /vms_project/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /vms_project/

EXPOSE 8000

CMD ["python", "vms-api/manage.py", "runserver"]