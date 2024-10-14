import pdfplumber
import spacy
import os
import re
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QLabel, QVBoxLayout, QPushButton, QProgressBar, QWidget

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_name(text):
    name_pattern = r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)' 
    name_matches = re.findall(name_pattern, text)
    return name_matches[0] if name_matches else "Not Found"

def extract_email(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    email_matches = re.findall(email_pattern, text)
    return email_matches[0] if email_matches else "Not Found"

def extract_phone(text):
    phone_pattern = r'(\+?\d{1,3}[-.\s]?(\(?\d{1,4}?\)?[-.\s]?)?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9})'
    phone_matches = re.findall(phone_pattern, text)
    return phone_matches[0][0] if phone_matches else "Not Found"

def extract_skills(text):
    doc = nlp(text)
    skills = [token.text for token in doc if token.pos_ == "NOUN"]
    return list(set(skills))  # Remove duplicates

def extract_experience(text):
    experience = []
    for sent in nlp(text).sents:
        if 'experience' in sent.text.lower() or 'intern' in sent.text.lower():
            experience.append(sent.text)
    return experience

def extract_education(text):
    education = []
    for sent in nlp(text).sents:
        if re.search(r'\b(degree|university|college|education|studied|fsc|bs)\b', sent.text, re.IGNORECASE):
            education.append(sent.text)
    return education

def extract_information(text):
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)
    experience = extract_experience(text)
    education = extract_education(text)
    
    return {
        'name': name,
        'email': email,
        'phone': phone,
        'skills': skills,
        'experience': experience,
        'education': education
    }

def append_to_csv(data, csv_file_path):
    data['skills'] = ', '.join(data['skills'])
    data['experience'] = ' | '.join(data['experience'])  # Using | to separate experiences
    data['education'] = ' | '.join(data['education'])  # Using | to separate education

    df = pd.DataFrame([data])
    df.to_csv(csv_file_path, mode='a', header=not os.path.exists(csv_file_path), index=False)

class ResumeParserApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        # Setup the GUI
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Resume Parser')
        self.setGeometry(100, 100, 500, 400)  # Increased window size

        # Create a layout
        layout = QVBoxLayout()
        
        # Title Label
        titleLabel = QLabel("Resume Parser Application")
        titleLabel.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(titleLabel)

        # Description Label
        descriptionLabel = QLabel("Upload a PDF resume to extract information.")
        descriptionLabel.setStyleSheet("font-size: 14px; margin-bottom: 20px;")
        layout.addWidget(descriptionLabel)

        # Create a button to upload PDF
        self.uploadButton = QPushButton('Upload Resume', self)
        self.uploadButton.setStyleSheet("font-size: 16px; padding: 10px;")
        self.uploadButton.clicked.connect(self.upload_resume)
        layout.addWidget(self.uploadButton)

        # Label to show uploaded file name
        self.fileNameLabel = QLabel("")
        self.fileNameLabel.setStyleSheet("font-size: 14px; margin-top: 20px;")
        layout.addWidget(self.fileNameLabel)

        # Progress Bar
        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 0)  # Indeterminate mode
        self.progressBar.setVisible(False)  # Initially hidden
        layout.addWidget(self.progressBar)

        self.setLayout(layout)

    def upload_resume(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select PDF Resume", "", "PDF Files (*.pdf);;All Files (*)", options=options)

        if file_name:
            self.fileNameLabel.setText(f"Selected File: {os.path.basename(file_name)}")  # Display the file name
            self.process_resume(file_name)

    def process_resume(self, pdf_path):
        self.progressBar.setVisible(True)  # Show progress bar
        self.progressBar.setValue(0)  # Reset value
        
        # Extract text from PDF
        resume_text = extract_text_from_pdf(pdf_path)

        # Extract information from the resume
        extracted_data = extract_information(resume_text)

        # Specify the path to your CSV file
        csv_file_path = 'parsed_resume_data.csv'
        
        # Append extracted data to CSV
        append_to_csv(extracted_data, csv_file_path)

        # Hide progress bar
        self.progressBar.setVisible(False)

        # Show a success message
        QMessageBox.information(self, "Success", f"Data from '{pdf_path}' has been appended to '{csv_file_path}'.\nYou can upload more resumes!")

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    parser = ResumeParserApp()
    parser.show()
    sys.exit(app.exec_())
