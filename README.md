<div align="center">
  <h1><strong>Math Vision:<br>Computer Vision for Handwritten Mathematical Notation Recognition</strong></h1>
</div>

<div align="center">
  
  https://github.com/Roodaki/Math-Vision/assets/89901590/c1929d1b-8961-40ca-9830-9833e5008c94
</div>

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Intruduction](#intruduction)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Requirements](#requirements)
  - [Environment Setup](#environment-setup)
- [Future Developments](#future-developments)
- [License](#license)

## Intruduction

Math Vision is an advanced application that utilizes computer vision techniques for the recognition and classification of handwritten mathematical notations. The project leverages a convolutional neural network model, specifically transfer learning with VGG16 and fine-tuning using the Kaggle "Handwritten Math Symbols" dataset, to achieve high accuracy in recognition of a wide variety of mathematical symbols and expressions. This enables applications in educational tools, digital note-taking systems, and automated grading platforms.

## Features

1. `Drawing Functionality`: Users can draw on the canvas with various brush sizes and utilize undo/redo actions, along with a clear button for erasing all content.
2. `Data Processing and Preparation`:
   - The dataset used is the Kaggle "Handwritten Math Symbols" dataset, which consists of 100,000+ 45x45 pixel JPEG files. These files contain English alphanumeric symbols, math operators, set operators, and basic predefined math functions.
   - The application loads, normalizes and splits images into training, development, and test sets. Preprocessed data is saved to a compressed .npz file for training or fine-tuning a CNN model.
3. `Transfer Learning with VGG16`: Model training leverages transfer learning with VGG16, a convolutional neural network model pre-trained on ImageNet. The model is fine-tuned using the pre-processed dataset to recognize mathematical symbols and expressions. Trained model weights and the entire model are saved in the h5 format for future use.
4. `Fast Prediction`: The application swiftly predicts the corresponding math symbols by processing the drawn handwriting on the canvas through the fine-tuned CNN. The accuracy of each prediction is displayed with colored text: green for predictions with accuracy above 90%, yellow for accuracy above 80%, and red for accuracy above 60%.
5. `User-friendly Interface`: The GUI is meticulously crafted to be intuitive and user-friendly, featuring clear button labels, a well-organized layout, and intuitive navigation, providing easy interaction with the application's various features.
6. `Modular and Extensible`: The codebase is structured in a modular way, allowing for easy extension and integration of new features. New functionalities can be added without significant modifications to existing code.
7. `Well-documented Code`: The codebase is thoroughly documented, with detailed comments explaining the functionality of each module, method, and class. This makes it easier for developers to understand and maintain the code.

## Project Structure

The project follows a specific structure to organize its files and directories:

```
math-notation-recognition-app/
├── data/
│   ├── dataset/                       # Directory containing the original dataset for math notation recognition.
│   └── processed_data/
│       └── math_notation_dataset.npz  # Compressed numpy file containing preprocessed data.
│
├── models/
│   ├── saved_models/
│   │   ├── model_weights.weights.h5   # Weights of the trained model.
│   │   └── trained_model.h5           # Complete trained model including architecture and weights.
│   │
│   └── train_model.py                 # Python script for training the model using transfer learning with VGG16.
│
├── ui/
│   ├── resources/
│   │   └── styles/
│   │       └── stylesheet.qss         # Stylesheet file for UI styling.
│   │
│   ├── canvas_widget.py               # Widget for drawing on the canvas.
│   └── main_window.py                 # Main application window.
│
├── utils/
│   ├── data_processing.py             # Module for loading, preprocessing, and splitting image data.
│   └── image_utils.py                 # Utility functions for image processing.
│
├── main.py                            # Main script file responsible for initializing the application and setting up the main window.
├── .gitignore                         # Specifies which files and directories should be ignored by Git version control.
├── requirements.txt                   # Lists the project's dependencies.
└── README.md                          # Documentation file providing information about the project.
```

## Getting Started

### Requirements

- **Python libraries**:
  - Numpy
  - TensorFlow
  - scikit-learn
  - OpenCV
  - Pillow
  - PyQt
- **"Handwritten Math Symbols" Dataset**: Download the dataset from [Kaggle](https://www.kaggle.com/datasets/xainano/handwrittenmathsymbols) and place it in `data/dataset/`.
- **System Requirements**
  - **OS**: Any platform supported by PyQt5, OpenCV, TensorFlow, and Keras.
  - **Memory**: At least 8 GB RAM is recommended for training models.

### Environment Setup

1. **Install Python**: Ensure Python 3.X is installed. If not, download and install it from [python.org](https://www.python.org/downloads/).
2. **Clone the Repository**:
   ```
   git clone https://github.com/Roodaki/Math-Vision.git
   cd math-vision
   ```
3. **Install required packages**: Use pip to install the necessary Python libraries:
   ```
   pip install -r requirements.txt
   ```
4. \*\*Run the program:
   ```
   python main.py
   ```

## Future Developments

- `Real-time Prediction`: Implement real-time prediction capabilities to classify symbols as they are drawn on the canvas. This enhancement will provide immediate feedback to users and improve the interactive experience.
- `Camera Support`: Integrate camera support to enable users to capture handwritten math symbols directly from a webcam or camera-equipped device. This feature will expand the application's usability and facilitate real-time input.
- `Recognition of Multiple Symbols`: Enhance the model to recognize and classify multiple handwritten symbols captured in a single image. This improvement will enable users to input complex mathematical expressions in one go.
- `Integration with Additional Datasets`: Incorporate additional datasets containing handwritten math symbols to further train and validate the model. This step will improve the model's accuracy and robustness across a wider range of handwritten styles and symbols.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.
