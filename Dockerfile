FROM python:3.10
WORKDIR /app/
ENV HEADLESS=true
RUN pip install playwright
RUN playwright install
RUN playwright install-deps
COPY . .
CMD [ "python", "main.py" ]
