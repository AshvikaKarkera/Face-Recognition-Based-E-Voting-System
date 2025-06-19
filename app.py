import streamlit as st
import cv2
import numpy as np
import pickle
import os
import csv
import time
from datetime import datetime
from fpdf import FPDF

st.set_page_config(page_title="E-Voting System", layout="centered")
st.title("Face Recognition-Based E-Voting System")

# Ensure data folder exists
if not os.path.exists('data/'):
    os.makedirs('data/')

facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

menu = st.sidebar.selectbox("Select Mode", ["Register Yourself", "Cast Your Vote"])

# Utility functions
def load_pickle(path, default):
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return pickle.load(f)
    return default

def save_pickle(path, data):
    with open(path, 'wb') as f:
        pickle.dump(data, f)

def already_registered(name):
    names = load_pickle("data/names.pkl", [])
    return name in names

def already_voted(name):
    if not os.path.exists("data/Votes.csv"):
        return False
    with open("data/Votes.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0] == name:
                return True
    return False

def generate_receipt(aadhar, vote, date, timestamp):
    masked = "XXXX-XXXX-" + aadhar[-4:]
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="E-Voting Receipt", ln=1, align="C")
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Aadhar Number: {masked}", ln=2)
    pdf.cell(200, 10, txt=f"Voted for: {vote}", ln=3)
    pdf.cell(200, 10, txt=f"Date: {date}", ln=4)
    pdf.cell(200, 10, txt=f"Time: {timestamp}", ln=5)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Thank you for participating in the election.", ln=6)

    file_path = f"data/receipt_{aadhar}.pdf"
    pdf.output(file_path)
    return file_path

# Registration Section
if menu == "Register Yourself":
    st.subheader("Step 1: Face Registration")

    name = st.text_input("Enter your Aadhar number")

    if name:
        if not name.isdigit() or len(name) != 12:
            st.error("Aadhar number must be exactly 12 digits and numeric.")
        elif already_registered(name):
            st.warning("This Aadhar number is already registered.")

    img = st.camera_input("Capture your face")

    if img and name and name.isdigit() and len(name) == 12 and not already_registered(name):
        file_bytes = np.asarray(bytearray(img.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, 1)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facedetect.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            st.warning("No face detected. Please try again.")
        else:
            for (x, y, w, h) in faces:
                crop_img = frame[y:y+h, x:x+w]
                resized_img = cv2.resize(crop_img, (50, 50)).flatten()

                faces_data = load_pickle("data/faces_data.pkl", np.empty((0, 7500)))
                names = load_pickle("data/names.pkl", [])

                faces_data = np.append(faces_data, [resized_img], axis=0)
                names.append(name)

                save_pickle("data/faces_data.pkl", faces_data)
                save_pickle("data/names.pkl", names)

                st.image(crop_img, channels="BGR")
                st.success(f"Face registered for Aadhar: {name}")

# Voting Section
elif menu == "Cast Your Vote":
    st.subheader("Step 2: Cast Your Vote")

    img = st.camera_input("Face recognition to vote")

    if img:
        file_bytes = np.asarray(bytearray(img.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, 1)

        faces_data = load_pickle("data/faces_data.pkl", None)
        names = load_pickle("data/names.pkl", None)

        if faces_data is None or names is None:
            st.error("No registered faces found. Please register first.")
        else:
            from sklearn.neighbors import KNeighborsClassifier
            n_neighbors = min(5, len(names))  # dynamically adjust
            knn = KNeighborsClassifier(n_neighbors=n_neighbors)
            knn.fit(faces_data, names)


            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = facedetect.detectMultiScale(gray, 1.3, 5)

            if len(faces) == 0:
                st.warning("No face detected.")
            else:
                for (x, y, w, h) in faces:
                    crop_img = frame[y:y+h, x:x+w]
                    resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
                    output = knn.predict(resized_img)[0]

                    st.success(f"Face recognized as: {output}")

                    if already_voted(output):
                        st.error("You have already voted.")
                        break

                    vote = st.radio("Choose your party:", ["BJP", "CONGRESS", "APB", "NOTA"])
                    if st.button("Submit Vote"):
                        ts = time.time()
                        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
                        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                        with open("data/Votes.csv", "a", newline="") as f:
                            writer = csv.writer(f)
                            if os.stat("data/Votes.csv").st_size == 0:
                                writer.writerow(["NAME", "VOTE", "DATE", "TIME"])
                            writer.writerow([output, vote, date, timestamp])

                        st.success("Thank you! Your vote has been recorded.")

                        file_path = generate_receipt(output, vote, date, timestamp)
                        with open(file_path, "rb") as f:
                            st.download_button("Download Receipt", f, file_name="voting_receipt.pdf", mime="application/pdf")

                        break
