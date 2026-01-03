import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input

cnn_model = load_model("models/cnn_feature_extractor.h5")
lstm_model = load_model("models/lstm_action_model.h5")

# Same order as training
CLASS_NAMES = [
    "applauding","blowing_bubbles","brushing_teeth","cleaning_the_floor",
    "climbing","cooking","cutting_trees","cutting_vegetables","drinking",
    "feeding_a_horse","fishing","fixing_a_bike","fixing_a_car","gardening",
    "holding_an_umbrella","jumping","looking_through_a_microscope",
    "looking_through_a_telescope","playing_guitar","playing_violin",
    "pouring_liquid","pushing_a_cart","reading","phoning","riding_a_bike",
    "riding_a_horse","rowing_a_boat","running","shooting_an_arrow",
    "smoking","taking_photos","texting_message","throwing_frisby",
    "using_a_computer","walking_the_dog","washing_dishes","watching_TV",
    "waving_hands","writing_on_a_board","writing_on_a_book"
]

def predict_action(image):
    image = cv2.resize(image, (224, 224))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = preprocess_input(image)
    image = np.expand_dims(image, axis=0)

    features = cnn_model.predict(image, verbose=0)
    features = features.reshape((1, 1, features.shape[1]))

    prediction = lstm_model.predict(features)
    class_id = np.argmax(prediction)

    return CLASS_NAMES[class_id]
