import os
import pandas as pd
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
crypto_json_path = os.path.abspath(os.path.join(
    (__file__), '..', '..', 'json', 'crypto'))
btcusd_df = pd.read_json(os.path.join(crypto_json_path, 'btcusd_1Day'))


def generate_dataset(price, seq_len):
    X_list, y_list = [], []
    for i in range(len(price)-seq_len):
        X = np.array(price[i:i+seq_len])
        y = np.array([price[i:i+seq_len]])
        X_list.append(X)
        y_list.append(y)
    return np.array(X_list), np.array(y_list)


class MLP_stock:
    def build_model(self):
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Dense(64, activation=tf.nn.relu))
        model.add(tf.keras.layers.Dense(64, activation=tf.nn.relu))
        model.add(tf.keras.layers.Dense(64, activation=tf.nn.relu))
        model.add(tf.keras.layers.Dense(1, activation=tf.nn.relu))
        optimizer = tf.keras.optimizers.Adam(lr=0.01)
        model.compile(optimizer=optimizer, loss="mse")
        return model

    def train(self, X_train, y_train, bs=32, ntry=10):
        model = self.build_model()
        model.fit(X_train, y_train, batch_size=32, epochs=100, shuffle=True)
        self.best_model = model
        best_loss = model.evaluate(X_train[-50:], y_train[-50:])

        for i in range(ntry):
            model = self.build_model()
            model.fit(X_train, y_train, batch_size=32,
                      epochs=100, shuffle=True)
            if model.evaluate(X_train, y_train) < best_loss:
                self.best_model = model
                best_loss = model.evaluate(X_train[-50:], y_train[-50:])

    def predict(self, X_test):
        return self.best_model.predict(X_test)


train_len = 800

stock_train = btcusd_df["Close"].iloc[:train_len].values
stock_test = btcusd_df["Close"].iloc[train_len:].values

X_train, y_train = generate_dataset(stock_train, 5)
X_test, y_test = generate_dataset(stock_test, 5)

MLP = MLP_stock()
MLP.train(X_train, y_train)
y_pred = np.squeeze(MLP.predict(X_test))

test_len = len(y_pred)

plt.figure(figsize=(15, 10))
plt.rcParams['font.size'] = "20"
plt.plot(range(test_len), y_test, label='true')
plt.plot(range(test_len), y_pred, label='predict')
