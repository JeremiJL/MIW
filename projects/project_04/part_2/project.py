
# 1. load data

# 2. split data into test and training set


# 3. plot test set, train set and original data
_, (test_plot, train_plot, org_plot) = plt.subplots(1,3)

test_plot.scatter(X_test, y_test)
test_plot.set_title("test dataset")
train_plot.scatter(X_train, y_train)
train_plot.set_title("train dataset")
org_plot.scatter(x_data, y_data)
org_plot.set_title("original dataset")

plt.show()
plt.savefig("output/part_2_prog_1/input_data.png")

# 4. define the input layer

inputs = Input(shape=(1,), name="input_features")

# 4. define the hidden layers

x = layers.Dense(4, activation="relu", name="hidden_layer_1")(inputs)

x = layers.Dense(2, activation="relu", name="hidden_layer_2")(x)

# 4. define the output layer

outputs = layers.Dense(1, name="predicted_value")(x)

# 5. build the model

model = Model(
    inputs=inputs,
    outputs=outputs,
    name="two_layered_network"
)

# 6. plot model

keras.utils.plot_model(
    model,
    "output/part_2_prog_1/two_layered_network_model.png",
    show_shapes=True,
    show_layer_names=True
)

# 6. compile the model

model.compile(
    optimizer=optimizers.SGD(learning_rate=0.001),
    loss="mse",
    metrics=["mse","accuracy"]
)

# 7. check the model

print(
    model.summary()
)

# 8. train the model

type(X_train)



# # 9. Make predictions
#
# predictions = model.predict(X[:5])
#
# print(predictions)
