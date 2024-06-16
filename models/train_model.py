import numpy as np
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Flatten, Dense, Dropout
from tensorflow.keras.models import Model, save_model


def load_preprocessed_data(data_path):
    """
    Load preprocessed dataset from the given file path.

    Args:
    - data_path (str): Path to the preprocessed data file.

    Returns:
    - Tuple of numpy arrays and variables:
      (X_train, y_train, X_dev, y_dev, X_test, y_test, class_names, input_shape, num_classes)
    """
    # Load the preprocessed dataset
    data = np.load(data_path, allow_pickle=True)

    # Extract data arrays
    X_train = data["X_train"]
    y_train = data["y_train"]
    X_dev = data["X_dev"]
    y_dev = data["y_dev"]
    X_test = data["X_test"]
    y_test = data["y_test"]
    class_names = data["class_names"]
    input_shape = X_train.shape[1:]  # Shape of input data
    num_classes = len(class_names)  # Number of classes

    return (
        X_train,
        y_train,
        X_dev,
        y_dev,
        X_test,
        y_test,
        class_names,
        input_shape,
        num_classes,
    )


def build_model(input_shape, num_classes):
    """
    Build a convolutional neural network model based on VGG16 architecture.

    Args:
    - input_shape (tuple): Shape of the input data (excluding batch dimension).
    - num_classes (int): Number of output classes.

    Returns:
    - TensorFlow Keras Model: Compiled CNN model.
    """
    # Load pre-trained VGG16 model, exclude top layers
    base_model = VGG16(
        weights="imagenet",
        include_top=False,
        input_shape=(input_shape[0], input_shape[1], 3),  # Adjusted for RGB input
    )

    # Add custom top layers
    x = Flatten()(base_model.output)
    x = Dense(512, activation="relu")(x)
    x = Dropout(0.5)(x)
    predictions = Dense(num_classes, activation="softmax")(x)

    # Final model
    model = Model(inputs=base_model.input, outputs=predictions)

    # Freeze the layers of the pre-trained model (optional)
    for layer in base_model.layers:
        layer.trainable = False

    return model


def train_model(model, X_train, y_train, X_dev, y_dev, batch_size=32, epochs=20):
    """
    Train the convolutional neural network model.

    Args:
    - model (TensorFlow Keras Model): Compiled CNN model to train.
    - X_train (numpy.ndarray): Training data.
    - y_train (numpy.ndarray): Training labels.
    - X_dev (numpy.ndarray): Validation data.
    - y_dev (numpy.ndarray): Validation labels.
    - batch_size (int): Batch size for training.
    - epochs (int): Number of epochs for training.

    Returns:
    - Tuple of TensorFlow Keras Model and History:
      (Trained model, Training history)
    """
    # Compile the model
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    # Callbacks
    checkpoint_callback = ModelCheckpoint(
        "models/saved_models/model_weights.weights.h5",
        save_best_only=True,
        save_weights_only=True,
        monitor="val_loss",
        mode="min",
        verbose=1,
    )
    early_stopping_callback = EarlyStopping(
        patience=5,
        monitor="val_loss",
        mode="min",
        verbose=1,
        restore_best_weights=True,
    )

    # Train the model
    history = model.fit(
        X_train,
        y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=(X_dev, y_dev),
        callbacks=[checkpoint_callback, early_stopping_callback],
    )

    return model, history


def evaluate_model(model, X_test, y_test):
    """
    Evaluate the convolutional neural network model on the test set.

    Args:
    - model (TensorFlow Keras Model): Trained CNN model.
    - X_test (numpy.ndarray): Test data.
    - y_test (numpy.ndarray): Test labels.
    """
    # Evaluate the model
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test loss: {loss:.4f}")
    print(f"Test accuracy: {accuracy:.4f}")


def save_trained_model(model, model_path):
    """
    Save the trained convolutional neural network model.

    Args:
    - model (TensorFlow Keras Model): Trained CNN model.
    - model_path (str): File path to save the trained model.
    """
    # Save the trained model
    save_model(model, model_path)
    print(f"Trained model saved to {model_path}")


def main():
    """
    Main function to load data, build, train, evaluate, and save the CNN model.
    """
    # Constants
    data_path = "data/processed_data/math_notation_dataset.npz"
    trained_model_path = "models/saved_models/trained_model.h5"

    # Load preprocessed data and determine input shape and number of classes
    (
        X_train,
        y_train,
        X_dev,
        y_dev,
        X_test,
        y_test,
        class_names,
        input_shape,
        num_classes,
    ) = load_preprocessed_data(data_path)

    # Build the model
    model = build_model(input_shape, num_classes)

    # Train the model
    model, history = train_model(model, X_train, y_train, X_dev, y_dev)

    # Evaluate the model
    evaluate_model(model, X_test, y_test)

    # Save the trained model
    save_trained_model(model, trained_model_path)


if __name__ == "__main__":
    main()
