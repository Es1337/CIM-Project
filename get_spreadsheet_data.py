import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import datetime as dt

def get_all_spreadsheet_records(json_file: str, spreadsheet_url: str) -> list:
    # define the scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
    # authorize the clientsheet 
    client = gspread.authorize(creds)
    # get the instance of the Spreadsheet
    sheet = client.open_by_url(spreadsheet_url)
    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)

    return sheet_instance.get_all_records()

def clean_records(records:  list) -> list:
    records_clean = []
    year = 2020
    for record in records:
        date_tmp = str(record['Data']).split('.')
        if date_tmp[1] == "1":
            date_tmp[1] = "10"
        date = dt.date(year, int(date_tmp[1]), int(date_tmp[0]))
        records_clean.append({'Data':date, 'Nowe': int(record['Nowe przypadki'].strip(' +')), 'Testy': int(record['Dobowa liczba wykonanych testów'])})
        if date_tmp[0] == "31" and date_tmp[1] == "12":
            year += 1

    return records_clean

def get_all_records_list() -> list:
    records_data = get_all_spreadsheet_records(
                        'mio-cov-cases.json', 
                        'https://docs.google.com/spreadsheets/d/19-pUdErRJR_PCjy_oDeG89_z2VV5YdWRB9saPfFPkSw')

    return clean_records(records_data)

def get_all_records_dataframe() -> pd.DataFrame:
    return pd.DataFrame.from_dict(get_all_records_list())

def print_records(records: list) -> None:
    for record in records:
        print(f"{record['Data']} {record['Nowe']} {record['Testy']}")
