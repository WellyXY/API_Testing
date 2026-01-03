# Railway (Railpack) default gunicorn timeout can kill long requests.
# Seedream i2i can take 50-120s; increase timeout and allow limited concurrency.
web: gunicorn -b 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 300 parrot_proxy_server:app
