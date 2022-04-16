COS BSE IW: ProviderFinder

Author: Julia Douvas

Project Description: Flask web app using a Bootstrap CSS framework and connected to a PostgreSQL database. This web app is designed to make the process of finding a mental healthcare provider in Princeton, NJ easier. Features include: a provider search feature based on webscrapped PsychologyToday profiles and educational materials on different kinds of providers and therapies.

Layout of git repo:

How to set up database to run locally:
1. Activate virtual environment (instructions below)
2. Run webscrape.py locally (result: ids.json, ids.csv, moreinfo.json, moreinfo.csv, moreinfo_newer.csv, moreinfo_newest.csv, psu_ids.json, psy_ids.csv, psy_moreinfo.json, psy_moreinfo.csv, psy_moreinfo_newer.csv, psy_moreinfo_newest.csv)
3. Open PgAdmin 4, create server if you haven't already
4. Create table titled "providers" with columns: name (char var), url (char var), titles (char var[]), phone_number (char var), address (char var), zipcode (char var), city (char var), state (char var), insurancees (char var), telehealth_option (char var), pay_by (char var), specialties_issues (char var), sexuality (char var), therapies_offered (char var), and walkable (char var).
5. Upload moreinfo_newest.csv and psy_moreinfo_newest.csv to "providers" table
6. Fill out walkable column
7. Once the database had been set up, update/create the .env file in the project folder
8. ProviderFinder can now be locally: $ python runserver.py [port]

Computing environment set-up:
1. Create a directory on your computer, git clone from this github
2. Create virtual env in this new cloned directory (helpful tutorial: https://phoenixnap.com/kb/install-flask):
      - Update python: $ brew install python
      - $ cd [your cloned directory]
      - $ python3 -m venv <name of environment>
      - $ . <name of environment>/bin/activate
      - Install Flask: $ pip install Flask
      - Install lxml: $ pip install lxml
      - Install requests: $ pip install requests
      - Install BeautifulSoup: $ pip install beautifulsoup4
      - Install html5lib: $ pip install html5lib
      - Install selenium: $ pip install selenium
      - Chromedriver.exe must be in working directory
      - Install webdriver: $ pip install webdriver_manager
      - Install Postgres: https://www.sqlshack.com/setting-up-a-postgresql-database-on-mac/ 
            - $ brew install postgresql
            - To start/stop postgreSQL: 
                - $ brew services start postgresql
                - $ psql postgres [-U username]
                - $ brew services stop postgresql
      - $ pip install psycopg2-binary
      - $ python -m pip install python-dotenv
      - $ pip install gunicorn

To run project locally:
  - Activate virtual environment in directory
  - $ python runserver.py [port]

To run project on Heroku (https://stackabuse.com/deploying-a-flask-application-to-heroku/)
  - Create requirements.txt with all modules needed (the libraries we're using and their versions)
        - use $ pip list to get a list of all these libraries and versions
  - Create Procfile in main folder and write in it: "web: gunicorn app:app"
  - Update git (which should be connected to heroku application on Heroku.com)
  - Deploy app to Heroku
        $ heroku login -i
        $ heroku git:remote -a {your-project-name}
        $ set git remote heroku to https://git.heroku.com/providerfinder.git
        $ git push heroku HEAD:master
