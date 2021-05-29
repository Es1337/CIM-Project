import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

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

    for record in records:
        records_clean.append({'Data':record['Data'], 'Nowe': int(record['Nowe przypadki'].strip(' +'))})

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
        print(record)

if __name__ == '__main__':
    print_records(get_all_records_list())

