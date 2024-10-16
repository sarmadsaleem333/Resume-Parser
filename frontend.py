import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, 
                             QProgressBar, QMessageBox)
from PyQt5.QtCore import Qt
import PyPDF2
import pandas as pd

class PDFtoCSVApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the window
        self.setWindowTitle('Resume Info Extractor')
        self.showMaximized()  # Make the window full-screen

        # Set up the layout
        layout = QVBoxLayout()

        # Set main background color for the window
        self.setStyleSheet("background-color: #f5f5f5;")

        # Add a label for title
        title_label = QLabel('Extract Information from PDFs', self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #2c3e50;
            padding: 30px;
        """)
        layout.addWidget(title_label)

        # Add a button for selecting PDF files
        self.select_button = QPushButton('Select PDF Files', self)
        self.select_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 18px;
                padding: 15px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c6e93;
            }
        """)
        self.select_button.clicked.connect(self.select_pdfs)
        layout.addWidget(self.select_button)

        # Label to show the selected PDFs
        self.label = QLabel('No PDFs selected', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 16px; color: #7f8c8d; padding: 15px;")
        layout.addWidget(self.label)

        # Add a button for extracting the information
        self.convert_button = QPushButton('Extract Information', self)
        self.convert_button.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
                font-size: 18px;
                padding: 15px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
            QPushButton:pressed {
                background-color: #a84300;
            }
        """)
        self.convert_button.clicked.connect(self.convert_to_csv)
        self.convert_button.setEnabled(False)
        layout.addWidget(self.convert_button)

        # Add a progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #bdc3c7;
                border-radius: 10px;
                text-align: center;
                font-size: 16px;
                color: black;
                background-color: #ecf0f1;
            }
            QProgressBar::chunk {
                background-color: #27ae60;
                width: 20px;
            }
        """)
        self.progress_bar.setValue(0)  # Initially set to 0
        layout.addWidget(self.progress_bar)

        # Set the layout to the window
        self.setLayout(layout)

        # Store selected PDFs
        self.pdf_files = []

    def select_pdfs(self):
        # Open file dialog to select multiple PDFs
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDF Files", "", "PDF Files (*.pdf)", options=options)
        
        if files:
            self.pdf_files = files
            self.label.setText('\n'.join(files))  # Display the selected files
            self.convert_button.setEnabled(True)

    def extract_text_from_pdf(self, pdf_path):
        # Placeholder for extracting text, can be replaced by Pyresparser later
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
        return text

    def convert_to_csv(self):
        # Disable buttons during conversion
        self.convert_button.setEnabled(False)
        self.select_button.setEnabled(False)

        # Prepare data for CSV
        pdf_data = []
        total_files = len(self.pdf_files)
        
        self.progress_bar.setValue(0)
        step = 100 / total_files  # Progress bar step increment

        for idx, pdf_file in enumerate(self.pdf_files):
            text = self.extract_text_from_pdf(pdf_file)
            pdf_data.append({
                'file_name': os.path.basename(pdf_file),
                'content': text
            })

            # Update progress bar
            self.progress_bar.setValue(int((idx + 1) * step))

        # Convert to DataFrame and save as CSV
        df = pd.DataFrame(pdf_data)
        csv_file_path = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")[0]

        if csv_file_path:
            df.to_csv(csv_file_path, index=False)
            self.label.setText(f"CSV saved: {csv_file_path}")

            # Show success notification
            self.show_success_message(csv_file_path)

        # Reset progress bar and re-enable buttons
        self.progress_bar.setValue(0)
        self.select_button.setEnabled(True)

    def show_success_message(self, file_path):
        # Create a QMessageBox to show the success message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Extraction Completed")
        msg.setText(f"CSV file saved successfully at:\n{file_path}")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDFtoCSVApp()
    window.show()
    sys.exit(app.exec_())
