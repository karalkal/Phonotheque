# Phonotheque

### Student project in Django - social media/forum website based on users' favourite music albums

### The web application has been deployed [HERE](https://phonotheque.up.railway.app/)

---

#### The app is still under development... so am I, hence many things will not look right. Up-to-date information about the project's purpose, structure, operation and progress can be found [HERE](https://phonotheque.up.railway.app/about/)

---

#### To run the app locally - [VSCode Instructions](https://code.visualstudio.com/docs/python/tutorial-django):

NB: Won't run with the VPN on!  
`sudo apt-get install python3-venv # If needed (below Python 3.4)`  
`python3 -m venv .venv # Create venv`

Each time activate venv first:  
`source .venv/bin/activate`

Command Palette (View > Command Palette), select the Python: Select Interpreter command: select /.venv or .\\.venv  
`python -m pip install --upgrade pip`  
`pip install -r requirements.txt`  
NB Avoid installing backports.zoneinfo when using python >= 3.9
see [this article](https://stackoverflow.com/questions/71712258/error-could-not-build-wheels-for-backports-zoneinfo-which-is-required-to-insta)  
`sudo docker-compose up`  
Might need to install it first.  
If error "address in use", see section below.
At each reopening of the app:  
`python manage.py migrate`  
`python manage.py runserver`

---

#### To stop/kill postgress container:

Stop all volumes:  
`sudo docker-compose down -v`  
or
if `lsof -i :5432` doesn't show you any output, you can use
`sudo ss -lptn 'sport = :5432'` to see what process is bound to the port.  
Proceed further with `kill <pid>`

#### To compile staticfiles (required for deployment):

python manage.py collectstatic
or
python manage.py collectstatic --noinput --clear # This will clear the statics beforehand.

#### If server hangs

fuser 8080/tcp # will print you PID of process bound on that port.
fuser -k 8080/tcp # will kill that process.
