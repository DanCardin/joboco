FROM python:3.8

WORKDIR /code
RUN pip install requests

RUN echo 'import time; time.sleep(4); print("task1!")' > main.py

ENTRYPOINT [ "python" ]
CMD [ "/code/main.py" ]
