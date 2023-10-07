#!/bin/bash
# The next line spins a http server which is exposedd by localhost (127.0.0.1) and binded to port 8000, exposing the contents of public directory -
# Example if there exists file on path say public/resources/ns/fun.svg can be accessed from browser by
# http://localhost:8000/resources/ns/fun.svg or http://127.0.0.1:8000/resources/ns/fun.svg
python3 -m http.server 8000 --bind 127.0.0.1 --directory ./public/

