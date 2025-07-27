import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_sheet_data():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open("BOOM SET GO  Open Gym (Responses)").get_worksheet(0) 
    data = sheet.get_all_records()
    return data
