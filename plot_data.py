import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import math

def plot_cases(actual_new_cases, predicted_cases):
    plt.plot(actual_new_cases, color='black', label='Actual new cases')
    plt.plot(predicted_cases, color='green', label='Predicted cases')
    plt.legend(loc='upper right')
    plt.show()

    rms = mean_squared_error(actual_new_cases, predicted_cases, squared=False)
    print("\nRMSE:")
    print(rms)

def plot_error(actual_new_cases, predicted_cases):
    error = []
    for i in range(len(predicted_cases)):
        error.append(math.fabs(predicted_cases[i] - actual_new_cases[i]))

    plt.plot(error, color='red', label='Error: |prediction - actual_value|')
    plt.legend(loc='upper right')
    plt.show()