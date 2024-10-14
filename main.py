import warnings
warnings.filterwarnings("ignore")

import os
import nltk
nltk.download('stopwords')

from pyresparser import ResumeParser

# Parse the resume and extract data
data = ResumeParser(os.path.join(os.getcwd(), 'MSS_FinalCV.pdf')).get_extracted_data()

# Print the extracted data
print(data)
