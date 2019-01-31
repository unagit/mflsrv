FROM	python:3.7
WORKDIR /app

COPY 	.	.
RUN  	pip3 install  --no-cache-dir  -r requirements.txt

EXPOSE	5000
ENV	FLASK_APP=mflsrv
RUN	chmod +x  mflsrv.sh

ENTRYPOINT	["./mflsrv.sh"]