import warnings
warnings.filterwarnings("ignore")
import os
import pandas as pd
import nltk
nltk.download('stopwords')

from pyresparser import ResumeParser    

def parse_resumes(resume_folder):
    resumes_data = []
    for filename in os.listdir(resume_folder):
        if filename.endswith('.pdf'):
            resume_path = os.path.join(resume_folder, filename)
            data = ResumeParser(resume_path).get_extracted_data()

            name = data.get('name', None)
            email = data.get('email', None)
            phone = data.get('mobile_number', None)
        

            if phone and not phone.startswith('92'):
                phone = '92' + phone.lstrip('0')  

            resumes_data.append({
                'name': name,
                'email': email,
                'phone': phone,
                'filename': filename
            })

    return resumes_data


resume_folder = os.path.join(os.getcwd(), 'resumes')


extracted_data = parse_resumes(resume_folder)


df = pd.DataFrame(extracted_data)

# Save the extracted data to a CSV file
output_csv = os.path.join(os.getcwd(), 'extracted_resumes.csv')
df.to_csv(output_csv, index=False)

print(f"Extracted data saved to {output_csv}")
