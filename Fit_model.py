from inception_resnet_v1_lcl import *
from keras.models import Model
from keras.layers import *
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread
from PyQt5 import uic

import os
import matplotlib.pyplot as plt


class learn_model():
    def __init__(self):
        path = './dataset/train'
        file_list = os.listdir(path)
        self.len = len(file_list)
        print("init")
    def l(self):
        base_model = InceptionResNetV1(weights_path='./facenet_keras_weights.h5',
                                           input_shape=(224, 224, 3),
                                           dropout_keep_prob=0.8)

        for layer in base_model.layers[:]:
            layer.trainable = False

        #base_model.summary()
        print(self.len)
        classes = self.len
        epochs = 20
        # epochs = 500
        targetx = 224
        targety = 224

        x = base_model.get_layer(index=442).output
        x = GlobalAveragePooling2D()(x)
        x = BatchNormalization()(x)
        x = Dropout(0.5)(x)
        x = Dense(1024, activation='relu', kernel_initializer='he_normal', bias_initializer='zeros')(x)
        x = BatchNormalization()(x)
        x = Dropout(0.5)(x)
        predictions = Dense(classes, activation='softmax')(x)

        my_model = Model(inputs=base_model.input, outputs=predictions)
        #my_model.summary()

        # making the instance of 'ImageDataGenerator'
        train_datagen = ImageDataGenerator(rescale=1. / 255,
                                           rotation_range=30,
                                           width_shift_range=0.2,
                                           height_shift_range=0.2,
                                           shear_range=0.2,
                                           zoom_range=0.2,
                                           horizontal_flip=True,
                                           fill_mode='nearest')

        val_datagen = ImageDataGenerator(rescale=1. / 255)

        # setting the path of datasets
        train_dir = './dataset/train'
        val_dir = './dataset/test'

        train_generator = train_datagen.flow_from_directory(train_dir,
                                                            batch_size=200,
                                                            target_size=(targetx, targety),
                                                            shuffle=True,
                                                            class_mode='categorical')

        val_generator = val_datagen.flow_from_directory(val_dir,
                                                        batch_size=100,
                                                        target_size=(targetx, targety),
                                                        shuffle=True,
                                                        class_mode='categorical')
        checkpoint_dir = "./model"
        os.makedirs(checkpoint_dir, exist_ok=True)
        checkpoint = ModelCheckpoint(filepath=checkpoint_dir + "/" + "weight_1.hdf5",
                                     monitor='loss',
                                     mode='min',
                                     save_best_only=True)

        my_model.compile(optimizer='adam',
                         loss="categorical_crossentropy",
                         metrics=["accuracy"])

        history = my_model.fit_generator(train_generator,
                                           steps_per_epoch=len(train_generator),
                                           epochs=epochs,
                                           validation_data=val_generator,
                                           validation_steps=len(val_generator),
                                           callbacks=[checkpoint])
        print("2")
        my_model.save('face_model.h5')

        # visualizing
        # history.history
        # acc = history.history['accuracy']
        # val_acc = history.history['val_accuracy']
        # loss = history.history['loss']
        # val_loss = history.history['val_loss']
        #
        # epochs = range(1, len(acc) + 1)
        #
        # plt.plot(epochs, acc, 'bo', label='Training acc')
        # plt.plot(epochs, val_acc, 'b', label='Validation acc')
        # plt.title('Accuracy')
        # plt.legend()
        # plt.figure()
        #
        # plt.plot(epochs, loss, 'ro', label='Training loss')
        # plt.plot(epochs, val_loss, 'r', label='Validation loss')
        # plt.title('Loss')
        # plt.legend()
        #
        # plt.show()

if __name__ == '__main__':
    a = learn_model()
    a.l()