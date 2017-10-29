# -*- coding: utf-8 -*-
from keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping, CSVLogger
from models import ModelContainer
from data_set import DataSet
import time

__author__ = "ujihirokazuya"
__date__ = "2017/10/28"


def train():
    model = "conv3d"
    class_size_limit = 100  # int, can be 1-101 or None
    seq_length = 40
    image_shape = (80, 80, 1)
    # image_shape = (80, 80, 3)

    input_shape = [seq_length]
    input_shape.extend(image_shape)
    input_shape = tuple(input_shape)

    # nb_epoch = 1000
    nb_epoch = 1
    batch_size = 32

    tb = TensorBoard(log_dir="./data/logs")
    early_stopper = EarlyStopping(patience=100000)
    timestamp = time.time()
    csv_logger = CSVLogger("./data/logs/{}-training-{}.log".format(model, str(timestamp)))

    data_set = DataSet(seq_length=seq_length, class_size_limit=class_size_limit, image_shape=image_shape)
    train_data_file_list, test_data_file_list = data_set.split_train_test()
    X, y = data_set.get_all_sequences_in_memory(train_data_file_list)
    X_test, y_test = data_set.get_all_sequences_in_memory(test_data_file_list)

    model_container = ModelContainer(class_size=len(data_set.class_names), input_shape=input_shape, loaded_model=None)
    model_container.model.fit(X,
                              y,
                              batch_size=batch_size,
                              validation_data=(X_test, y_test),
                              verbose=1,
                              callbacks=[tb, early_stopper, csv_logger],
                              epochs=nb_epoch)
    """
    # Helper: Save the model.
    check_point_file_path = "./data/checkpoints/{m}-{d}.{epoch:03d}-{val_loss:.3f}.hdf5'".format(m=model, d=data_type)
    check_pointer = ModelCheckpoint(filepath=check_point_file_path, verbose=1, save_best_only=True)

    # Get samples per epoch.
    # Multiply by 0.7 to attempt to guess how much of data.data is the train set.
    steps_per_epoch = (len(data_set.data_list) * 0.7) // batch_size
    model_container.model.fit_generator(generator=generator,
                                        steps_per_epoch=steps_per_epoch,
                                        epochs=nb_epoch,
                                        verbose=1,
                                        callbacks=[tb, early_stopper, csv_logger],
                                        validation_data=val_generator,
                                        validation_steps=10)
    """
    model_container.model.save("result_tmp.h5")


def main():
    train()


if __name__ == '__main__':
    main()
