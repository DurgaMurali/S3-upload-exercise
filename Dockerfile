FROM python

RUN mkdir -p /home/durga/Exam_EC2
RUN cd /home/durga/Exam_EC2
COPY server.py /home/durga/Exam_EC2

RUN mkdir -p /home/durga/Exam_EC2/templates
COPY templates/* /home/durga/Exam_EC2/templates

RUN pip3 install flask
RUN pip3 install boto3

CMD ["python3", "/home/durga/Exam_EC2/server.py"]