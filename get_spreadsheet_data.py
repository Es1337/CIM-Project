import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import datetime as dt
from scipy.stats import pearsonr
import numpy as np 
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler, StandardScaler
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.models import Sequential

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

if __name__ == '__main__':
    #print_records(get_all_records_list())
    data = get_all_records_list()
    tests = []
    new_cases = []
    for record in data:
        tests.append(record['Testy'])
        new_cases.append(record['Nowe'])

    tests = np.array(tests)
    new_cases = np.array(new_cases)

    corr, _ = pearsonr(tests, new_cases)
    print('Pearsons correlation: %.3f' % corr)

    scaler_cases = MinMaxScaler(feature_range=(0, 1))
    scaler_tests = MinMaxScaler(feature_range=(0, 1))
    scaled_tests = scaler_tests.fit_transform(tests.reshape(-1,1))
    scaled_new_cases = scaler_cases.fit_transform(new_cases.reshape(-1,1))



    #print(scaled_tests)
    #print(scaled_new_cases)
    scaled_data = np.append(scaled_tests, scaled_new_cases, axis=1)
    training_days = 300
    train_data = scaled_data[:training_days, :]
    test_data = scaled_data[training_days:, :]

    prediction_days = 60


    x_train = []
    y_train = []

    for i in range(prediction_days, len(train_data)):
        x_train.append(train_data[i-prediction_days:i, :])
        y_train.append(train_data[i, 0])
    x_train = np.array(x_train)
    y_train = np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 2))
    #print(x_train)

    x_test = []
    actual_new_cases = []
    for i in range(prediction_days, len(test_data)):
        x_test.append(test_data[i-prediction_days:i, :])
        actual_new_cases.append(test_data[i, 0])

    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 2))
    #actual_new_cases = new_cases[training_days+prediction_days:]

    model = Sequential()
    model.add(LSTM(units=150, input_shape=(x_train.shape[1], 2)))
    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, epochs=50, batch_size=10)
    
    prediction = model.predict(x_test)
    prediction = scaler_cases.inverse_transform(prediction)
    actual_new_cases = np.array(actual_new_cases)
    actual_new_cases = actual_new_cases.reshape(-1, 1)
    actual_new_cases = scaler_cases.inverse_transform(actual_new_cases)


    plt.plot(actual_new_cases, color='black', label='Actual new cases')
    plt.plot(prediction, color='green', label='Predicted cases')
    plt.legend(loc='upper right')
    plt.show()