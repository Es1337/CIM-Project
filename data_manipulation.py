import numpy as np 
from sklearn.preprocessing import MinMaxScaler

def scale(tests, new_cases):
    scaler_cases = MinMaxScaler()
    scaler_tests = MinMaxScaler(feature_range=(0, 1))
    scaled_tests = scaler_tests.fit_transform(tests.reshape(-1,1))
    scaled_new_cases = scaler_cases.fit_transform(new_cases.reshape(-1,1))

    return [np.append(scaled_tests, scaled_new_cases, axis=1), scaler_cases, scaler_tests]

def get_training_data(prediction_days, data):
    x_train = []
    y_train = []

    for i in range(prediction_days, len(data)):
        x_train.append(data[i-prediction_days:i, :])
        y_train.append(data[i, 1])

    x_train = np.array(x_train)

    return [np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 2)), np.array(y_train)]

def get_testing_data(prediction_days, data):
    x_test = []
    actual_new_cases = []
    for i in range(prediction_days, len(data)):
        x_test.append(data[i-prediction_days:i, :])
        actual_new_cases.append(data[i, 1])

    x_test = np.array(x_test)

    return [np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 2)), actual_new_cases]