# Paris Collection - Django eCommerce App

Django eComm, API & Frontend technology for mobile App. 

Please follow the following steps to set up and run the project on your local environment.


Steps:

1. Clone the repository onto your local environment.

2. Create a virtual environment (using virtualenv or pipenv).
	- pip install virtualenv or 
	- pip install pipenv

3. Install the requirements located in requirements.txt in requirements directory.

4. Create a postgres database in your local environment or Database server.
	- name      : pcshop_dev
	- user      : pcshop_user
	- password  : pcsPTl@ppUS3R!

(Could be restored from the existing copy if needs be - Ask Mpoyi Tshibuyi).

5. Request config.json file from Mpoyi Tshibuyi which contains remaining sensitive settings' info.

6. Create a directory named 'pcshop' Anywhere in your local environment but not in the project's directory. 
   
7. Make the 'pcshop' directory network sharable. 
   
8. Place the config.json file in the 'pcshop' directory.
   
9. Then run "python manage.py runserver localhost:8000 --settings=config.settings.dev".