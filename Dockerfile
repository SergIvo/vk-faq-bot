FROM python:3.10-alpine

WORKDIR /faq_bot

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "vk_bot.py"]
