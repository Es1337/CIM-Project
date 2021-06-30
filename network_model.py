from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.models import Sequential

def setup(x_train):
    model = Sequential()
    model.add(LSTM(units=150, input_shape=(x_train.shape[1], 2)))
    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss='mean_squared_error')

    return model