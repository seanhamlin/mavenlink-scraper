#!/usr/bin/env bash

# Load credentials.
. /Users/sean.hamlin/projects/mavenlink-scraper/config.sh

start=`date +%s`

# Kick off CasperJS to create the accounts.json file.
/usr/local/bin/casperjs /Users/sean.hamlin/projects/mavenlink-scraper/mavenlink-scraper.js --username=${USERNAME} --password=${PASSWORD}

middle=`date +%s`

# Now upload this to Google Spreadsheets.
/usr/local/bin/python /Users/sean.hamlin/projects/mavenlink-scraper/mavenlink-uploader.py

end=`date +%s`

casper_runtime=$((middle-start))
python_runtime=$((end-middle))
echo "CasperJS took ${casper_runtime} seconds"
echo "Python took ${python_runtime} seconds"
echo "DONE"
