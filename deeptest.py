from keras.models import Sequential, Input, Model
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, Lambda
import keras
from keras import backend as K
from DataRead import NormalDataRead

batch_size = 128
epochs = 1

num_classes = 10

#データ読み込み
input_shape, x_train, y_train, x_test, y_test = NormalDataRead()

##########################################################################
#モデル
def MNISTmodel(input_shape):
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=input_shape))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))

    #損失関数、optimizerを決定
    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])

    return model

def VideoEditCNN(input_shape):
    # Define the tensors for the two input images
    left_input = Input(input_shape)
    right_input = Input(input_shape)

    # Convolutional Neural Network
    model = Sequential()
    model.add(Conv2D(64, (10, 10), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D())
    model.add(Conv2D(128, (7, 7), activation='relu'))
    model.add(MaxPooling2D())
    model.add(Conv2D(128, (4, 4), activation='relu'))
    model.add(MaxPooling2D())
    model.add(Conv2D(256, (4, 4), activation='relu'))
    model.add(Flatten())
    model.add(Dense(4096, activation='sigmoid'))

    # Generate the encodings (feature vectors) for the two images
    encoded_l = model(left_input)
    encoded_r = model(right_input)

    # Add a customized layer to compute the absolute difference between the encodings
    L1_layer = Lambda(lambda tensors: K.abs(tensors[0] - tensors[1]))
    L1_distance = L1_layer([encoded_l, encoded_r])

    # Add a dense layer with a sigmoid unit to generate the similarity score
    prediction = Dense(1, activation='sigmoid')(L1_distance)

    # Connect the inputs with the outputs
    siamese_net = Model(inputs=[left_input, right_input], outputs=prediction)

    # return the model
    return siamese_net

model = MNISTmodel(input_shape)

#訓練
#validation_dataを入れるとval_loss, val_accも出してくれる
#lossが下がるがval_lossが上がったら過学習
model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=2,
          validation_data=(x_test, y_test)
        )

#評価
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])





