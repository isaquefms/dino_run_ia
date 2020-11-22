# Demais imports
import os
# Game parameters
from game_parameters import IMG_COLS, IMG_ROWS, IMG_CHANNELS, ACTIONS, \
    LEARNING_RATE, LOSS_FILE_PATH
# keras imports
# from keras.models import model_from_json
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.optimizers import Adam
# from keras.callbacks import TensorBoard


def buildmodel():
    print("Now we build the model")
    model = Sequential()
    model.add(Conv2D(32, (8, 8), padding='same', strides=(4, 4), input_shape=(
        IMG_COLS, IMG_ROWS, IMG_CHANNELS)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (4, 4), strides=(2, 2), padding='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3, 3), strides=(1, 1), padding='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Activation('relu'))
    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dense(ACTIONS))
    adam = Adam(lr=LEARNING_RATE)
    model.compile(loss='mse', optimizer=adam)

    # create model file if not present
    if not os.path.isfile(LOSS_FILE_PATH):
        model.save_weights('model.h5')

    print("We finish building the model")
    return model
