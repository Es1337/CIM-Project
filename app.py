import numpy as np
from scipy.stats import pearsonr
from get_spreadsheet_data import get_all_records_list
from data_manipulation import get_testing_data, get_training_data, scale
from plot_data import plot_cases, plot_error
from network_model import setup

if __name__ == '__main__':
    data = get_all_records_list()
    tests = []
    new_cases = []
    for record in data:
        tests.append(record['Testy'])
        new_cases.append(record['Nowe'])

    tests = np.array(tests)
    new_cases = np.array(new_cases)

    corr, _ = pearsonr(tests, new_cases)
    print('\nPearsons correlation: %.3f' % corr)

    [scaled_data, scaler_cases, scaler_tests] = scale(tests, new_cases)

    training_days = 300
    train_data = scaled_data[:training_days, :]
    test_data = scaled_data[training_days:, :]

    prediction_days = 60

    [x_train, y_train] = get_training_data(prediction_days, train_data)
    [x_test, actual_new_cases] = get_testing_data(prediction_days, test_data)

    model = setup(x_train)
    model.fit(x_train, y_train, epochs=50, batch_size=32)
    
    prediction = model.predict(x_test)
    prediction = scaler_cases.inverse_transform(prediction)

    actual_new_cases = np.array(actual_new_cases)
    actual_new_cases = actual_new_cases.reshape(-1, 1)
    actual_new_cases = scaler_cases.inverse_transform(actual_new_cases)

    plot_cases(actual_new_cases, prediction)

    plot_error(actual_new_cases, prediction)