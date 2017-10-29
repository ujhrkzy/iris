"""
Train our RNN on extracted features or images.
"""
from keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping, CSVLogger
from models import ResearchModels
from data import DataSet
import time
from keras.models import load_model

def train(data_type, seq_length, model, saved_model=None,
          concat=False, class_limit=None, image_shape=None,
          load_to_memory=False):
    # Set variables.
    nb_epoch = 1000000
    batch_size = 32

    # Helper: Save the model.
    checkpointer = ModelCheckpoint(
        filepath='./data/checkpoints/' + model + '-' + data_type + \
            '.{epoch:03d}-{val_loss:.3f}.hdf5',
        verbose=1,
        save_best_only=True)

    # Helper: TensorBoard
    tb = TensorBoard(log_dir='./data/logs')

    # Helper: Stop when we stop learning.
    early_stopper = EarlyStopping(patience=100000)

    # Helper: Save results.
    timestamp = time.time()
    csv_logger = CSVLogger('./data/logs/' + model + '-' + 'training-' + \
        str(timestamp) + '.log')

    # Get the data and process it.
    if image_shape is None:
        data = DataSet(
            seq_length=seq_length,
            class_limit=class_limit
        )
    else:
        data = DataSet(
            seq_length=seq_length,
            class_limit=class_limit,
            image_shape=image_shape
        )

    # Get samples per epoch.
    # Multiply by 0.7 to attempt to guess how much of data.data is the train set.
    steps_per_epoch = (len(data.data) * 0.7) // batch_size

    if load_to_memory:
        # Get data.
        X, y = data.get_all_sequences_in_memory('train', data_type, concat)
        X_test, y_test = data.get_all_sequences_in_memory('test', data_type, concat)
    else:
        # Get generators.
        generator = data.frame_generator(batch_size, 'train', data_type, concat)
        val_generator = data.frame_generator(batch_size, 'test', data_type, concat)

    import pdb; pdb.set_trace()
    # Get the model.
    model = load_model("result_c3d.h5")
    loss_and_metrics = model.evaluate(X_test, y_test)
    import pdb; pdb.set_trace()
    print("\nloss:{} accuracy:{}".format(loss_and_metrics[0],loss_and_metrics[1]))


def main():
    """These are the main training settings. Set each before running
    this file."""
    model = 'conv_3d'  # see `models.py` for more
    saved_model = None  # None or weights file
    class_limit = 100  # int, can be 1-101 or None
    seq_length = 40
    load_to_memory = True  # pre-load the sequences into memory

    # Chose images or features and image shape based on network.
    if model == 'conv_3d':
        data_type = 'images'
        image_shape = (80, 80, 3)
    elif model == 'lrcn':
        data_type = 'image'
        image_shape = (150, 150, 3)
    else:
        data_type = 'features'
        image_shape = None

    # MLP requires flattened features.
    if model == 'mlp':
        concat = True
    else:
        concat = False

    train(data_type, seq_length, model, saved_model=saved_model,
          class_limit=class_limit, concat=concat, image_shape=image_shape,
          load_to_memory=load_to_memory)

if __name__ == '__main__':
    main()
