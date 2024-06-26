import tensorflow as tf
import numpy as np
from PIL import Image
import io
import logging

logging.basicConfig(level=logging.DEBUG)

def load_model(model_path='mnist_model.keras'):
    """Load the trained model"""
    logging.debug("Loading model...")
    try:
        return tf.keras.models.load_model(model_path)
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        logging.info("Attempting to reconstruct the model architecture...")
        
        # Reconstruct the model architecture
        base_model = tf.keras.applications.MobileNetV2(input_shape=(32, 32, 3),
                                                       include_top=False,
                                                       weights=None)
        base_model.trainable = False
        model = tf.keras.models.Sequential([
            base_model,
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(10, activation='softmax')
        ])

        # Load weights from the saved model
        model.build((None, 32, 32, 3))
        model.load_weights(model_path)
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        return model

def preprocess_image(image_contents):
    """Preprocess the image for prediction"""
    logging.debug("Preprocessing image...")
    img = Image.open(io.BytesIO(image_contents)).convert('RGB')
    img = img.resize((32, 32))
    img_array = np.array(img).astype('float32') / 255
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict(model, image):
    """Make a prediction on the image"""
    logging.debug("Making prediction...")
    if image.shape != (1, 32, 32, 3):
        raise ValueError(f"Expected image shape (1, 32, 32, 3), but got {image.shape}")
    prediction = model.predict(image)
    return int(np.argmax(prediction[0]))

def predict_image(image_contents, model_path='mnist_model.keras'):
    """Load model, preprocess image, and make a prediction"""
    try:
        model = load_model(model_path)
        if model is None:
            return None
        processed_image = preprocess_image(image_contents)
        result = predict(model, processed_image)
        return result
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Error during prediction: {e}")

# Example usage
if __name__ == "__main__":
    with open("./predict_number_4.jpeg", "rb") as f:
        image_contents = f.read()
    result = predict_image(image_contents)
    print(f"The predicted digit is: {result}")
