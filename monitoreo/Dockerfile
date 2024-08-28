from python:3.9-slim
workdir app
copy requirements.txt .
run pip install -r requirements.txt
copy . .
expose 5000
cmd python app.py