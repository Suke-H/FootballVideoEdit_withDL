from keras.models import Sequential, Input, Model
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, Lambda
from keras.optimizers import Adam
import keras
from keras import backend as K
import os

from DataRead import PairDataRead

batch_size = 5
epochs = 50

num_classes = 10

#データ読み込み
input_shape, wide_train, verch_train, y_train, wide_test, verch_test, y_test = PairDataRead("D:/outlaws_videodata/VE/TRANS_DATA")

##########################################################################
#モデル
def VideoEditCNN(input_shape):
    # Define the tensors for the two input images
    left_input = Input(input_shape)
    right_input = Input(input_shape)

    # Convolutional Neural Network
    model = Sequential()
    model.add(Conv2D(64, (3, 3), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D())
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D())
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D())

    model.add(Flatten())
    model.add(Dense(1024, activation='sigmoid'))
    model.add(Dropout(0.3))

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

############################################################################################

if os.path.exists('models/model.h5'):
    model = keras.models.load_model('models/model.h5', compile=False)
    print("models exist.")

else:
    model = VideoEditCNN(input_shape)
    print("models do not exist.")

    optimizer = Adam()
    model.compile(loss="binary_crossentropy",optimizer=optimizer)

    # 訓練
    # validation_dataを入れるとval_loss, val_accも出してくれる
    # lossが下がるがval_lossが上がったら過学習
    model.fit([wide_train, verch_train], y_train,
            batch_size=batch_size,
            epochs=epochs,
            verbose=2,
            validation_data=([wide_test, verch_test], y_test)
            )


# 評価
score = model.predict([wide_test, verch_test])
print('score:{}'.format(score))
print("y:{}".format(y_test))

# 保存
model.save('models/model.h5', include_optimizer=False)




