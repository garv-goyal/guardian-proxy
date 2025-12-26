#!/bin/bash
python3 app.py &

python3 -m streamlit run frontend.py --server.port 8080 --server.address 0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false