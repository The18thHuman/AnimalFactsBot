FROM python:3.11
LABEL authors="The18thHuman"
ADD animalfactsbot.py .
ADD handlers.py .
ADD utils.py .
ADD kb.py .
ADD text.py .
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
CMD ["python","./animalfactsbot.py"]
