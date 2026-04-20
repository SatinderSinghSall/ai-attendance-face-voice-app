import dlib
import numpy as np
import face_recognition_models
import streamlit as st
from sklearn.svm import SVC

from src.database.db import get_all_students


# ============================================================
# Load and cache all required dlib face recognition models
# This prevents reloading the heavy models every time the
# Streamlit script reruns.
# ============================================================
@st.cache_resource
def load_dlib_models():
    """
    Loads the required dlib models:
    - Face detector
    - Facial landmark predictor
    - Face recognition model

    Returns:
        tuple: (detector, shape_predictor, face_recognition_model)
    """

    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    face = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, face


# ============================================================
# Extract face embeddings from an image
# Each detected face is converted into a 128-dimensional vector
# using dlib's face recognition model.
# ============================================================
def get_face_embeddings(image_np):
    """
    Detects faces in an image and generates embeddings for them.

    Args:
        image_np (numpy array): Image in numpy format

    Returns:
        list: List of face embedding vectors
    """

    detector, sp, face_rec = load_dlib_models()
    faces = detector(image_np, 1)

    encodings = []

    for face in faces:
        shape = sp(image_np, face)

        face_descriptor = face_rec.compute_face_descriptor(
            image_np, shape, 1
        )

        encodings.append(np.array(face_descriptor))

    return encodings


# ============================================================
# Train the SVM classifier using stored student embeddings
# The embeddings are retrieved from the database and used to
# train a face recognition model.
# ============================================================
@st.cache_resource
def get_train_model():
    """
    Trains an SVM classifier on stored student face embeddings.

    Returns:
        dict | None:
        {
            'clf': trained SVM classifier,
            'x': training embeddings,
            'y': corresponding student IDs
        }
    """

    x = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:
        embedding = student.get('face_embedding')

        if embedding:
            x.append(np.array(embedding))
            y.append(student.get('student_id'))

    if len(x) == 0:
        return None

    clf = SVC(
        kernel="linear",
        probability=True,
        class_weight="balanced"
    )

    try:
        clf.fit(x, y)
    except ValueError:
        return None

    return {
        'clf': clf,
        'x': x,
        'y': y
    }


# ============================================================
# Retrain the face recognition classifier
# This is used when new students are added or embeddings change
# ============================================================
def train_classifier():
    """
    Clears cached model and retrains classifier.

    Returns:
        bool: True if model successfully trained
    """

    st.cache_resource.clear()

    model_data = get_train_model()

    return bool(model_data)


# ============================================================
# Predict attendance from a classroom image
# Steps:
# 1. Detect faces
# 2. Generate embeddings
# 3. Predict student ID using SVM classifier
# 4. Verify prediction using distance threshold
# ============================================================
def predict_attendance(class_image_np):
    """
    Predicts which students are present in a classroom image.

    Args:
        class_image_np (numpy array): Classroom image

    Returns:
        tuple:
        - detected_student (dict): {student_id: True}
        - all_students (list): All known student IDs
        - face_count (int): Number of faces detected
    """

    encodings = get_face_embeddings(class_image_np)

    detected_student = {}

    model_data = get_train_model()

    if not model_data:
        return detected_student, [], len(encodings)

    clf = model_data['clf']
    x_train = model_data['x']
    y_train = model_data['y']

    all_students = sorted(list(set(y_train)))

    for encoding in encodings:

        # If multiple students exist, use classifier
        if len(all_students) >= 2:
            predicted_id = int(clf.predict([encoding])[0])
        else:
            predicted_id = int(all_students[0])

        # Retrieve stored embedding for predicted student
        student_embedding = x_train[y_train.index(predicted_id)]

        # Calculate Euclidean distance
        best_match_score = np.linalg.norm(
            student_embedding - encoding
        )

        resemblance_threshold = 0.6

        # If distance below threshold, mark attendance
        if best_match_score <= resemblance_threshold:
            detected_student[predicted_id] = True

    return detected_student, all_students, len(encodings)

