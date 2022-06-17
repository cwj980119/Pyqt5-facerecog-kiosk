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

class Make_model(QThread):
    def __init__(self, p=None):
        QThread.__init__(self,parent=p)
        self.parent = p
        self.working = True

    def run(self):
        print("1")
        history = self.parent.my_model.fit(self.parent.train_generator,
                                         steps_per_epoch=len(self.parent.train_generator),
                                         epochs=self.parent.epochs,
                                         validation_data=self.parent.val_generator,
                                         validation_steps=len(self.parent.val_generator),
                                         callbacks=[self.parent.checkpoint])
        print("2")
        self.parent.my_model.save('face_model.h5')

        # visualizing
        # history.history
        acc = history.history['accuracy']
        val_acc = history.history['val_accuracy']
        loss = history.history['loss']
        val_loss = history.history['val_loss']

        epochs = range(1, len(acc) + 1)

        plt.plot(epochs, acc, 'bo', label='Training acc')
        plt.plot(epochs, val_acc, 'b', label='Validation acc')
        plt.title('Accuracy')
        plt.legend()
        plt.figure()

        plt.plot(epochs, loss, 'ro', label='Training loss')
        plt.plot(epochs, val_loss, 'r', label='Validation loss')
        plt.title('Loss')
        plt.legend()

        plt.show()
        self.working = False


class Learnig(QWidget):
    def __init__(self, main, user):
        QWidget.__init__(self)
        self.main = main
        self.user = user
        self.ui = uic.loadUi("./UI/learning.ui")
        self.ui.btn_main.clicked.connect(self.to_main)
        self.ui.btn_menu.clicked.connect(self.to_menu)
        self.ui.show()
        path = './dataset/train'
        file_list = os.listdir(path)
        self.len = len(file_list)
        #self.init_model()
        #self.init_model()

    def to_main(self):
        self.ui.hide()
        self.main.toMain()

    def to_menu(self):
        self.ui.hide()
        self.main.toMenu(self.user)

    def learn_model(self):
        self.worker = Make_model(self)
        self.worker.start()

    def init_model(self):
        base_model = InceptionResNetV1(weights_path='./facenet_keras_weights.h5',
                                       input_shape=(224, 224, 3),
                                       dropout_keep_prob=0.8)

        for layer in base_model.layers[:]:
            layer.trainable = False

        #base_model.summary()

        classes = self.len
        self.epochs = 20
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

        self.my_model = Model(inputs=base_model.input, outputs=predictions)
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

        self.train_generator = train_datagen.flow_from_directory(train_dir,
                                                            batch_size=200,
                                                            target_size=(targetx, targety),
                                                            shuffle=True,
                                                            class_mode='categorical')

        self.val_generator = val_datagen.flow_from_directory(val_dir,
                                                        batch_size=100,
                                                        target_size=(targetx, targety),
                                                        shuffle=True,
                                                        class_mode='categorical')
        checkpoint_dir = "./model"
        os.makedirs(checkpoint_dir, exist_ok=True)
        self.checkpoint = ModelCheckpoint(filepath=checkpoint_dir + "/" + "weight_1.hdf5",
                                     monitor='loss',
                                     mode='min',
                                     save_best_only=True)

        self.my_model.compile(optimizer='adam',
                         loss="categorical_crossentropy",
                         metrics=["accuracy"])

        print("1")
        self.learn_model()
        '''
        
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
        acc = history.history['accuracy']
        val_acc = history.history['val_accuracy']
        loss = history.history['loss']
        val_loss = history.history['val_loss']

        epochs = range(1, len(acc) + 1)

        plt.plot(epochs, acc, 'bo', label='Training acc')
        plt.plot(epochs, val_acc, 'b', label='Validation acc')
        plt.title('Accuracy')
        plt.legend()
        plt.figure()

        plt.plot(epochs, loss, 'ro', label='Training loss')
        plt.plot(epochs, val_loss, 'r', label='Validation loss')
        plt.title('Loss')
        plt.legend()

        plt.show() 
        '''
