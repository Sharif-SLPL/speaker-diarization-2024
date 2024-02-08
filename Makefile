Path=$(shell pwd)
Python=python3

runserver:
	$(Python) ./api/manage.py runserver

runtelbot:
	$(Python) ./bots/telegram/main.py

rungradio:
	$(Python) ./client/gradio/main.py
