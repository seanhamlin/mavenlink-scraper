# Mavenlink scraper

This is a script that will suck out the current month's billable and non-billable minutes for each customer.

## Installation

First you will need to install PhantomJS, the [2.1.1 release](http://phantomjs.org/download.html) is preferred. 

Next is CasperJS, you can git clone this repo

```
git clone https://github.com/n1k0/casperjs.git
git checkout master
```

Then symlink the bin/casperjs script to <code>/usr/local/bin/casperjs</code>.

You can verify this works by running:

```
casperjs --version
phantomjs --version
```

From anywhere (as these should now be on your path).

## Configuration

You will need to create a config file, based off the default config file

```
cp default.config.sh config.sh
```

Replace the dummy username and password with your own.

You will also need a Google OAuth Service account with access to "Drive API", save the credentials as a JSON file called 'google-oauth.json'.

## Run on cron

Edit your crontab, and place this or something like it in there.

```
# Mavenlink scraper, run twice a day at 1am and 1pm.
0 1,13 * * 1-5 PHANTOMJS_EXECUTABLE=/usr/local/bin/phantomjs cd /Users/sean.hamlin/projects/mavenlink-scraper && /Users/sean.hamlin/projects/mavenlink-scraper/run.sh > /Users/sean.hamlin/projects/mavenlink-scraper/job.log 2>&1
```
