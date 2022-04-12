iw

Author: Julia Douvas


Workflow:
1. Run webscrape_basic.py locally (result: ids.json, ids.csv)
2. Run webscrape_moreinfo.py locally (result: moreinfo.json moreinfo.csv)
3. Run fixcsv.py to fix moreinfo.csv (result: moreinfo_newer.csv)
4. Upload CSVs to create providers and providers_moreinfo tables in Heroku App Server in PgAdmin 4 
5. Run runserver.py locally 