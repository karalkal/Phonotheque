# Phonotheque
Student project in Django - social media/forum website based on users' favourite music albums

The web application has been deployed at:
*********

The project is under development now, up-to-date information about its current progress and state can be found in its About section at:
*********


To run app locally:
	# Won't run with the VPN on
	# Instructions at: https://code.visualstudio.com/docs/python/tutorial-django
	sudo apt-get install python3-venv    # If needed
	python3 -m venv .venv
	source .venv/bin/activate
	# Command Palette (View > Command Palette), select the Python: Select Interpreter command: select /.venv or .\.venv

	python -m pip install --upgrade pip
	pip install -r requirements.txt 
		# NB Avoid installing backports.zoneinfo when using python >= 3.9 
		# see https://stackoverflow.com/questions/71712258/error-could-not-build-wheels-for-backports-zoneinfo-which-is-required-to-insta
		
	sudo docker-compose up # might need to install it first
	python manage.py migrate
	python manage.py runserver 
	# default 8000 - otherwise python manage.py runserver 5000
	# Might have to jiggle with the allowed hosts a bit too
	

