cd server
gunicorn -k uvicorn.workers.UvicornWorker server_main:app --bind 0.0.0.0:$PORT