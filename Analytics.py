import pandas as pd
import pymongo
import copy
import _datetime
#from MongoClass import Mongoc
import numpy as np
from scipy.optimize import curve_fit
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, max_error


class Analytics:

    def __init__(self, mongoc_obj):
        self.db = mongoc_obj

    def get_peak(self, name, specifier, data):

        my_data = self.db.get_data(specifier, name, data, all=True)
        max_data = max(my_data)
        val_data_per = my_data.count(max_data) / len(my_data)
        return max_data, val_data_per

    def get_low(self, name, specifier, data):
        my_data = self.db.get_data(specifier, name, data, all=True)
        min_data = min(my_data)
        val_data_per = my_data.count(min_data) / len(my_data)
        return min_data, val_data_per

    def get_frequency(self, value, name, specifier, data):
        my_data = self.db.get_data(specifier, name, data)
        freq_lst = []
        counter = 0
        for val in my_data:
            if val == value:
                freq_lst.append(copy.deepcopy(counter))
                counter = 0
            else:
                counter += 1
        if len(freq_lst) != 0:
            return np.mean(freq_lst)[0]

    def get_median(self, name, specifier, data):
        my_data = self.db.get_data(specifier, name, data, all=True)
        return np.median(my_data)

    @staticmethod
    def linear(x, m, n):
        return m*x + n

    @staticmethod
    def sqr(x, a, b, c):
        return (a * x) + (b * x ** 2) + c

    @staticmethod
    def cube(x, a, b, c, d):
        return (a * x) + (b * x ** 2) + (c * x ** 3) + d

    @staticmethod
    def sin(x, a, b, c):
        return a * np.sin(b * x) + c

    @staticmethod
    def log(x, a, b, c):
        return a * np.log(b * x) + c

    def get_y_pred(self, model, param, x_test):

        if model == 'linear':
            a, b = param
            return list(map(lambda x: self.linear(x, a, b), x_test))

        elif model == 'cube':
            a, b, c, d = param
            return list(map(lambda x: self.cube(x, a, b, c, d), x_test))

        elif model == 'square':
            a, b, c = param
            return list(map(lambda x: self.sqr(x, a, b, c), x_test))

        elif model == 'sin':
            a, b, c = param
            return list(map(lambda x: self.sin(x, a, b, c), x_test))

        elif model == 'log':
            a, b, c = param
            return list(map(lambda x: self.log(x, a, b, c), x_test))

    def fit_data(self, models, name, specifier, data):

        # bringing data from mongodb
        x_data = self.db.get_data(specifier, name, data='timestamp', all=True)
        y_data = self.db.get_data(specifier, name, data, all=True)
        # splitting data to train and test
        X_train, X_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2, random_state=0)

        models_lst = []
        # fitting 5 data models(linear, square, cube, sin and log)
        for model in list(models.items()):
            param, _ = curve_fit(model[1], X_train, y_train)
            param = list(param)
            y_pred = self.get_y_pred(model[0], param, X_test)
            models_lst.append([model[0], r2_score(y_test, y_pred), mean_absolute_error(y_test, y_pred), model[1], param])

        # sorting by MAE
        models_lst.sort(key=lambda x: x[2], reverse=True)
        non_rev = []
        top_index = 0
        # filtering models
        for i in range(4):
            # checking if MAE between models is significant
            if abs(models_lst[top_index][2] - models_lst[i][2]) / models_lst[top_index][2] + 0.0001 > 0.05:
                non_rev.append(models_lst[i])
            # checking if R^2 between models is significant
            elif abs(models_lst[top_index][1] - models_lst[i][1]) / models_lst[top_index][1] > 0.05:
                if models_lst[top_index][1] > models_lst[i][1]:
                    non_rev.append(models_lst[top_index])
                    top_index = i
                else:
                    non_rev.append(models_lst[i])
            else:
                non_rev.append(models_lst[i])

        # removing models after filter
        for model1 in non_rev:
            models_lst.remove(model1)

        return models_lst[0]

    def predict(self, name, specifier, data, timestamp):
        models = [Analytics.linear, Analytics.sqr, Analytics.cube, Analytics.sin, Analytics.log]
        fitted_model = self.fit_data(models, name, specifier, data)
        if fitted_model[0] == 'linear':
            return fitted_model[3](fitted_model[4][0], fitted_model[4][1], x=timestamp)
        elif fitted_model[0] == 'cube':
            return fitted_model[3](fitted_model[4][0], fitted_model[4][1], fitted_model[4][2], fitted_model[4][3],
                                   x=timestamp)
        else:  # sqr, sin or log
            return fitted_model[3](fitted_model[4][0], fitted_model[4][1], fitted_model[4][2], x=timestamp)






























