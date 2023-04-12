FROM python:3.10

WORKDIR /home/app

#If we add the requirements and install dependencies first, docker can use cache if requirements don't change
ADD . /home/app
RUN pip install --no-cache-dir -r ./deployment/composer/requirements/base.txt

CMD python3 src/main.py

EXPOSE 4002
