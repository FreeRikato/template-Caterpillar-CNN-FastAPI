import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist

"""
    Script Summary:
    => Resizes the MNIST images from 28x28 to 32x32 pixels.
    => Normalizes the pixel values to be between 0 and 1.
    => Repeats the single grayscale channel to create 3 channels (RGB).
    => Uses MobileNetV2 as the base model with input shape (32, 32, 3).
    => Adds additional layers on top of the base model for classification.
    => Compiles and trains the model.
    => Saves the trained model.
"""

# Load and preprocess the MNIST dataset
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# Resize images to 32x32
train_images = tf.image.resize(train_images[..., tf.newaxis], (32, 32)).numpy()
test_images = tf.image.resize(test_images[..., tf.newaxis], (32, 32)).numpy()

# Normalize pixel values to be between 0 and 1
train_images = train_images.astype('float32') / 255
test_images = test_images.astype('float32') / 255

# Repeat the single channel to create 3 channels
train_images = tf.repeat(train_images, 3, axis=-1)
test_images = tf.repeat(test_images, 3, axis=-1)

# Define the base model for transfer learning
base_model = tf.keras.applications.MobileNetV2(input_shape=(32, 32, 3),
                                               include_top=False,
                                               weights='imagenet')
base_model.trainable = False

# Create the model
model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(10, activation='softmax')
])

# Compile and train the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(train_images, train_labels, epochs=10, 
                    validation_data=(test_images, test_labels))

# Save the model in the new format
model.save('mnist_model.keras')

print("Model trained and saved as mnist_model.keras")
