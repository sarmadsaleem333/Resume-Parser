import warnings

warnings.filterwarnings("ignore")

import en_core_web_sm

import os

from pyresparser import ResumeParser


data=ResumeParser(os.path.join(os.getcwd(), 'MSS_FinalCV.pdf')).get_extracted_data

print(data)