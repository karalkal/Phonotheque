# Phonotheque
### Student project in Django - social media/forum website based on users' favourite music albums

##### The web application has been deployed [HERE] (https://web-production-b677.up.railway.app/)
##### The project is still under development... so am I, hence many things will not look right.
##### Up-to-date information about its purpose, structure, operation and progress can be found [HERE] (https://web-production-b677.up.railway.app/about/)
---

##### To run the app locally - [VSCode Instructions] (https://code.visualstudio.com/docs/python/tutorial-django):
NB: Won't run with the VPN on! 
`sudo apt-get install python3-venv    # If needed`
`python3 -m venv .venv` 

Each time activate venv first: 
```source .venv/bin/activate``` 

Command Palette (View > Command Palette), select the Python: Select Interpreter command: select /.venv or .\.venv
`python -m pip install --upgrade pip`
`pip install -r requirements.txt`
NB Avoid installing backports.zoneinfo when using python >= 3.9 
see https://stackoverflow.com/questions/71712258/error-could-not-build-wheels-for-backports-zoneinfo-which-is-required-to-insta
		
`sudo docker-compose up  #might need to install it first, if error "address in use", see section below.`

At each reopening of the app:
	`python manage.py migrate`
	`python manage.py runserver`

##### To stop/kill postgress container:
Stop all volumes:
	```
	sudo docker-compose down -v
	```
OR
If ```lsof -i :5432``` doesn't show you any output, you can use 
```sudo ss -lptn 'sport = :5432'``` to see what process is bound to the port.
Proceed further with ```kill <pid>```

	

