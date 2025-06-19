import streamlit as st
import cv2
import numpy as np
import pickle
import os
import csv
import time
import pandas as pd
from datetime import datetime
from fpdf import FPDF

st.set_page_config(page_title="Face Recognition E-Voting", layout="centered")
st.title("Face Recognition-Based E-Voting System")

if not os.path.exists('data/'):
    os.makedirs('data/')

facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


menu = st.sidebar.selectbox("Select Mode", ["Register Yourself", "Cast Your Vote", "Admin Panel"])


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

if menu == "Register Yourself":
    st.subheader("Step 1: Face Registration")

    name = st.text_input("Enter your Aadhar number")
    valid_aadhar = name.isdigit() and len(name) == 12
    already_exists = already_registered(name) if valid_aadhar else False

    if name and not valid_aadhar:
        st.error("Aadhar number must be exactly 12 digits and numeric.")
    elif valid_aadhar and already_exists:
        st.warning("This Aadhar number is already registered.")

    img = st.camera_input("Capture your face")

    if img:
        if not valid_aadhar:
            st.error("Cannot register. Invalid Aadhar number.")
        elif already_exists:
            st.warning("This Aadhar number is already registered.")
        else:
            file_bytes = np.asarray(bytearray(img.read()), dtype=np.uint8)
            frame = cv2.imdecode(file_bytes, 1)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = facedetect.detectMultiScale(gray, 1.3, 5)

            if len(faces) == 0:
                st.warning("No face detected. Please try again.")
            else:
                for (x, y, w, h) in faces[:1]:  # Use only the first face
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
            n_neighbors = min(5, len(names))
            knn = KNeighborsClassifier(n_neighbors=n_neighbors)
            knn.fit(faces_data, names)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = facedetect.detectMultiScale(gray, 1.3, 5)

            if len(faces) == 0:
                st.warning("No face detected.")
            else:
                for (x, y, w, h) in faces[:1]:
                    crop_img = frame[y:y+h, x:x+w]
                    resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
                    output = knn.predict(resized_img)[0]

                    st.success(f"Face recognized as: {output}")

                    if already_voted(output):
                        st.error("You have already voted.")
                        break

                    vote = st.radio("Choose your party:", ["BJP", "CONGRESS", "APB", "NOTA"], key="vote_selection")

                    if st.button("Submit Vote"):
                        ts = time.time()
                        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
                        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                        csv_path = "data/Votes.csv"

                        try:
                            with open(csv_path, "a", newline="") as f:
                                writer = csv.writer(f)
                                if os.stat(csv_path).st_size == 0:
                                    writer.writerow(["NAME", "VOTE", "DATE", "TIME"])
                                writer.writerow([output, vote, date, timestamp])
                            st.success("Thank you! Your vote has been recorded.")
                        except Exception as e:
                            st.error(f"Error writing to CSV: {e}")
                            break

                        file_path = generate_receipt(output, vote, date, timestamp)
                        with open(file_path, "rb") as f:
                            st.download_button("Download Receipt", f, file_name="voting_receipt.pdf", mime="application/pdf")

                
elif menu == "Admin Panel":
    st.subheader("Admin Panel")

    password = st.text_input("Enter admin password", type="password")

    if password == "password1234":
        st.success("Welcome to the admin panel!")

        if os.path.exists("data/Votes.csv"):
            df = pd.read_csv("data/Votes.csv")
            st.dataframe(df)

            with open("data/Votes.csv", "rb") as f:
                st.download_button("Download Votes CSV", f, file_name="Votes.csv", mime="text/csv")
        else:
            st.info("No votes have been recorded yet.")
    elif password:
        st.error("Access Denied.")
