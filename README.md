# Performance History - A django app

This repo contains code for a django app being built for creating charts for performance benchmarks and trending. The app has a mysql server backend. Stay tuned for updates.



Given below are the steps to install an instance of the performance history app. 
(Note: I have only run this on python 2.7. Django 1.9 will require python 2.7. Though I haven't tested on python 3.x. Results may vary.)

- If you don't have virtualenv installed, use the following command:
	
	[sudo] pip install virtualenv

- Use virtual environment and create a virtual enviornment
	
	virtualenv <enviornment-name>

- Activate the virtual environment from the bin directory inside the virtual environment directory:
	
	./bin/activate

- Clone this repository: (You need to have git, of course)
	
	git clone <giturl-of-this-repo>

- Go to the directory created by the cloning of the git repo (and then the perfhistory_app directory) and type:

	pip install -r requirements.txt (You need pip :))

- Install migrations
	
	./manage.py makemigrations
	&& ./manage.py migrate
	&& ./manage.py loaddata dataDump/feb292016.json (or use latest data json file in the dataDump folder)
Currently there isn't a bash script to run the development server as daemon (We are not using a webserver with perfhistory app yet)

- Install screen

	yum -y install screen

- Create a new screen
 
	screen

- Ensure you are in the repo folder

	./manage.py runserver 0.0.0.0:<port> --insecure

	e.g. ./manage.py runserver 0.0.0.0:8081 --insecure

- Exit the screen using Ctl + a, then press d