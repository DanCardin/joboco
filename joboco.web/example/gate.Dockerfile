FROM python:3.8

WORKDIR /code
RUN pip install requests

COPY main.py main.py

ENTRYPOINT [ "python" ]
CMD [ "/code/main.py" ]
