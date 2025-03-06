import cv2
import numpy as np
import joblib
from skimage.feature import local_binary_pattern, hog
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Function to preprocess images
def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Convert to grayscale
    if img is None:
        raise FileNotFoundError(f"❌ Image not found: {image_path}")

    img = cv2.resize(img, (128, 128))  # Resize for consistency
    img = img / 255.0  # Normalize (0-1 scale)
    return img

# Function to extract features from an image
def extract_features(image):
    lbp_features = local_binary_pattern(image, P=8, R=1, method="uniform").flatten()
    hog_features = hog(image, pixels_per_cell=(8, 8), cells_per_block=(2, 2)).flatten()
    return np.hstack((lbp_features, hog_features))

# Load and process the images
try:
    image1 = preprocess_image("ear_depth_map.jpg")  # Authenticated user
    image2 = preprocess_image("processed_ear.jpg")  # Not recognized user
except FileNotFoundError as e:
    print(e)
    exit()

# Extract features
features1 = extract_features(image1)
features2 = extract_features(image2)

print("✅ Features extracted successfully.")

# Prepare dataset
X_train = np.array([features1, features2])
y_train = np.array([1, 0])  # 1 = Authenticated, 0 = Not Recognized

# 🚀 **FIX: No train-test split since dataset is too small**
# Instead, we train on the small dataset directly

# Train the SVM model
svm_model = SVC(kernel="linear", probability=True)
svm_model.fit(X_train, y_train)

# 🚀 **Test the model on the same training data (since no test set)**
y_pred = svm_model.predict(X_train)
accuracy = accuracy_score(y_train, y_pred)

print(f"✅ Model trained successfully with accuracy: {accuracy:.2f}")

# Save the trained model
joblib.dump(svm_model, "ear_auth_model.pkl")
print("✅ Model saved as 'ear_auth_model.pkl'")
