#-----------------------------------------------------------------------
# webscrape.py
# Author: Julia Douvas
# Description: Webscrapes PsychologyToday therapist and psychiatrist
#              profiles in the Princeton area and stores detailed info
#              about each provider into moreinfo_newest.csv and 
#              psy_moreinfo_newest.csv. Code takes about 1 hour to run.
# Results: creation of files: ids.csv, ids.json, moreinfo_newer.csv,
#          moreinfo_newest,csv, moreinfo.csv, moreinfo.json, psy_ids.csv,
#          psy_ids.json, psy_moreinfo_newer.csv, psy_moreinfo_newest.csv,
#          psy_moreinfo.json
#-----------------------------------------------------------------------
import therapist_webscrape_basic
import therapist_webscrape_moreinfo
import psy_webscrape_basic
import psy_webscrape_moreinfo

def main():
    # run therapist_webscrape_basic.py
    therapist_webscrape_basic.main()

    # run psy_webscrape_basic.py
    psy_webscrape_basic.main()

    # run therapist_webscrape_moreinfo.py
    therapist_webscrape_moreinfo.main()

    # run psy_webscrape_moreinfo.py
    psy_webscrape_moreinfo.main()

if __name__ == '__main__':
    main()
