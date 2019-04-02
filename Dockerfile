# Python runtime
FROM python:3.7.2-alpine

# Set working directory
WORKDIR /home

# Copy source
COPY . .

# Install dependencies
RUN pip install python-dotenv
RUN pip install babel
RUN pip install certifi
RUN pip install wincertstore
RUN pip install flask-babel
RUN pip install markupsafe
RUN pip install flask_table
RUN pip install pytz
RUN pip install jsonschema

# Open port
EXPOSE 5000

# Execute command
CMD ["python", "applicatie.py"]
