import json
import gspread
import sys
from datetime import datetime
from oauth2client.client import SignedJwtAssertionCredentials

json_key = json.load(open('google-oauth.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

print "Logging into Google"
gc = gspread.authorize(credentials)

print "Loading the Spreadsheet"
spreadsheet = gc.open_by_key('1E3sr_UfCoViA8CFPEtT7eMJo7wzcAoTIIYt-4lGd0ow')
worksheet = spreadsheet.get_worksheet(0)

# Load the cells we care about.
cell_list = worksheet.range('C4:D214')

# load the data.
accounts = json.load(open('accounts.json'))
count = 0
for idx, account in enumerate(accounts):
    print account['name'] + " [" + str(account['id']) + "]"
    try:
        # As long as the accounts.json file matches perfectly to the rows in the
        # spreadsheet, this is 1 API call to update the entire spreadsheet.
        cell_list[count].value = account['billable']
        count += 1
        cell_list[count].value = account['nonbillable']
        count += 1
    except:
        print ">> not found"
        # worksheet.append_row([account['name'], account['id'], account['billable'], account['nonbillable']])

    #if account['name'] == "Mead Johnson":
    #    break

worksheet.update_cells(cell_list)

# Last updated
now = datetime.now()
worksheet.update_acell("A1", "TAM hours for " + now.strftime("%B, %Y"))
worksheet.update_acell("B1", "Last updated " + now.strftime("%Y-%m-%d %H:%M (NZDT)"))
