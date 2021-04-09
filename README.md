# PurBeurreV2
Pur Beurre is the result of my project 8 as part of my OpenClassRooms training as a Python developer. It is part of the continuity of project 5.
## About
It is a web application that allows users to enter the designation of a food product to find a healthier equivalent. The user has the possibility of registering products in favorites but must then have or create an account.
## Sources
All the informations are from the [OpenFoodFacts](https://fr.openfoodfacts.org/) API.
## Languages, libraries and frameworks
This web app was developed with python 3 and the Django framework version 3.
Dynamic part of the site use [JQuery](https://jquery.com/).
It uses a template from [Bootstrap](https://getbootstrap.com/).
Icones are from [Font Awesome](https://fontawesome.com/).
All required python's libraries are in the requirements.txt file.
## In local mode
### Install
If you want to try it on localhost.
- Fake and clone the [PurBeurrev2 github's repository](https://github.com/screw-pack/PurBeurreV2.git).
- Create a python 3 virtual environement.
- Install the required modules with `pip install -r requirements.txt`.
- Install [postgresql](https://www.postgresql.org/download/).
- Create a data base with it ([Official Documentation](https://www.postgresql.org/docs/)).
- Modify `DATABASES` lines in /settings.py file of the django project with your username and DB name.
- To fill the data base launch `./manage.py runscript dbfeed`. Or use the json file in /purbeurrev2_project/substitute/dumps/.
- To launch the server `./manage.py runserver`.
- Open your web browser at http://127.0.0.1:8000/
### Tests
some tests are available: run `./manage.py test` to perform them.
Note: You'll need [mozilla/geckodriver](https://github.com/mozilla/geckodriver/releases/) to perform Selenium test. Put in the directory that is mentioned in the PATH environment variable. (`echo $PATH` on linux to display a list of all directories that are registered in the PATH variable.)
## Online
You can try it online at: https://sp-purbeurre.herokuapp.com/
