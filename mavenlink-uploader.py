import json
import gspread
import sys
from datetime import datetime
from oauth2client.client import SignedJwtAssertionCredentials

json_key = json.load(open('google-oauth.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

gc = gspread.authorize(credentials)

spreadsheet = gc.open_by_key('1E3sr_UfCoViA8CFPEtT7eMJo7wzcAoTIIYt-4lGd0ow')
worksheet = spreadsheet.get_worksheet(0)

# load the data.
accounts = json.load(open('accounts.json'))
for account in accounts:
    print account['name'] + " [" + str(account['id']) + "]"
    try:
        cell = worksheet.find(str(account['id']))
        row = cell.row
        worksheet.update_acell("C" + str(cell.row), account['billable'])
        worksheet.update_acell("D" + str(cell.row), account['nonbillable'])
    except:
        print ">> not found"
        worksheet.append_row([account['name'], account['id'], account['billable'], account['nonbillable']])

    #if account['name'] == "Mead Johnson":
    #    break

# Last updated
now = datetime.now()
worksheet.update_acell("A1", "TAM hours for " + now.strftime("%B, %Y"))
worksheet.update_acell("B1", "Last updated " + now.strftime("%Y-%m-%d %H:%M (NZDT)"))
