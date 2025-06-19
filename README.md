# 🗳️ Face Recognition-Based E-Voting System 
A secure, real-time electronic voting system powered by **facial recognition** and built with **Streamlit**.  
Voters register using their Aadhar number and face, and cast votes through live facial authentication.  
Votes are logged securely and a downloadable PDF receipt is generated for transparency.

![Registration Phase](https://github.com/user-attachments/assets/8dcdb5fe-be19-47d2-b3c8-4b95cab91a95)
![Voting Phase](https://github.com/user-attachments/assets/2707b90d-5c04-41b2-ba5a-408ee60dd5f9)
![Vote Receipts](https://github.com/user-attachments/assets/efb753d7-c2bc-4723-aee4-255ca0ea6fae)
![Admin Panel](https://github.com/user-attachments/assets/48d72d13-900a-4709-96b4-a5f1356e40fc)

## 📘 Project Overview

**Face Recognition-Based E-Voting System** is a secure, user-friendly web application that allows individuals to cast their votes electronically using real-time **facial recognition**. Instead of traditional voting methods that rely on ID verification or manual checklists, this system verifies the voter's identity through their face — ensuring a more secure and streamlined process.

### 🎯 Purpose
To build a lightweight and accessible e-voting platform that:
- Prevents impersonation and multiple voting attempts
- Simplifies voter registration through Aadhar-based face capture
- Encourages transparency with receipt generation
- Is deployable on the web using open-source tools

---

## 🔍 How It Works

1. **Registration Phase**  
   - The user enters their **Aadhar number** (must be 12 digits)
   - The system captures their face using a webcam and saves it in the dataset
   - Duplicate registrations are blocked

2. **Voting Phase**  
   - The user verifies their identity via **live facial recognition**
   - Once authenticated, they select their preferred party and cast the vote
   - The vote is logged in a CSV file with a timestamp
   - A **PDF receipt** is generated and offered for download

3. **Admin Panel**  
   - Password-protected access (`password- password1234`)
   - Allows admins to view and download all recorded votes

---

## ✅ Key Highlights
- Built using **Streamlit**, making it lightweight and web-ready
- Uses **OpenCV** for real-time face detection and recognition
- Trains a **KNN classifier** for fast and accurate face matching
- Generates **PDF vote receipts** using the `fpdf` library
- Logs all data in `.csv` format for transparency
- Ready to deploy on **Streamlit Cloud** for live demos

## 🚀 Features
- 👤 Aadhar-based face registration using webcam
- 🧠 Real-time face recognition via OpenCV and KNN
- 🗳️ One vote per person — re-voting is blocked
- 📄 Generates PDF vote receipt with masked Aadhar
- 🧾 Admin panel (password-protected) to view/download all votes
- 📦 Deployed easily on Streamlit Cloud
  
## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io) – Web interface
- [OpenCV](https://opencv.org/) – Face detection
- [scikit-learn](https://scikit-learn.org) – KNN classifier
- [NumPy](https://numpy.org/) – Image array handling
- [FPDF](https://pyfpdf.readthedocs.io) – PDF receipt generation

## 📁 Project Structure
```
.
├── app.py # Main Streamlit app
├── requirements.txt # Python dependencies
├── packages.txt # System dependency for OpenCV
├── README.md # Project overview
├── .gitignore # Files to exclude from Git
└── data/
    └── .gitkeep # Keeps the folder in GitHub
```


## 🧪 Installation & Running Locally

Follow these steps to set up the app on your local machine:

### 1️⃣ Clone the repository

```bash
git clone https://github.com/AshvikaKarkera/Face-Recognition-Based-E-Voting-System.git
cd Face-Recognition-Based-E-Voting-System
```

### 2️⃣ (Optional) Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # On Linux/Mac
venv\Scripts\activate       # On Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the app

```bash
streamlit run app.py
```

> 🔗 You’ll get a local URL (usually http://localhost:8501) to open in your browser.

---

## 🌐 Deploy on Streamlit Cloud

This app is fully compatible with Streamlit Community Cloud: https://streamlit.io/cloud

To deploy:

- Push this repo to GitHub
- Add `packages.txt` with the following inside:
- 
  ```
  libgl1-mesa-glx
  ```
- Create a new app on Streamlit Cloud
- Set `app.py` as the main file

  ---

## 📜 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for more details.

---

## 👨‍💻 Author

**Ashvika Karkera**  
Email: [ashvikavk@gmail.com](ashvikavk@gmail.com)  
GitHub: [@AshvikaKarkera](https://github.com/AshvikaKarkera)





