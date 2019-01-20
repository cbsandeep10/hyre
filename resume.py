import json, sys
import requests
from nltk.tokenize import RegexpTokenizer

# from flask import Flask
# from flask import request

import pandas as pd
from joblib import dump, load

cl = {"Amazon": "Amazon_interview.joblib" ,"Jacobs":"Jacobs_interview.joblib",
       "Paradox": "Paradox_interview.joblib", "Hedera": "Hadera_interview.joblib",
       "Microsoft":"Microsoft_interview.joblib USAA_interview.joblib"}

jd = {'Microsoft' : {'SDE 1':'Understanding and application of the principles associated with C/C++/C# development using appropriate GNU and Microsoft compilers,Shell scripting languages used in a Windows/Linux multi-platform development'
            },'Amazon': {'Data Analyst': '3+ years of hands on experience in SQL, Excel, Linux and OLAP,3+ years of hands on experience in SAS, R and/or Python,An MS or PhD degree in Computer Science, Mathematics, Statistics, Finance, Machine Learning or related technical field,Experience with big data and object oriented programming languages (python, ruby) Experience in Machine learning (decision trees, multivariate and logistic regression, kNN, kMeans, etc'
            },'Paradox':{'Software Intern':'solid foundation in data structures, algorithms and complexity analysis; A hunger for tracking down root causes - no matter how deep it takes you - and fixing them in systematic ways; Strong understanding of operating systems, file systems and networking; Strong understanding of web technology; Expertise in your favorite modern programming language: Python, Ruby, Java, Objective-C, or C++.'
            },'USAA':{'Cyber Security':'Bachelors, Masters or PhD in Cybersecurity or Information Security or related,Proficiency in one or more of the following-Java, Python, XML, HTML, C#, Objective C; Database design & development including SQL,Basic knowledge of cyber security principles, tools and devices kali linux.Experience working with design recovery, software analysis, and/or reverse engineering tools'
            },'Jacobs':{'Quality Assurance':'strong computer skills including Microsoft Office, QA applications and databases,Bachelors degree preferred,Visit all facilities on a regular basis to monitor quality and provide assistance as needed.C,C++,Java'
            }
}

# app = Flask(__name__)

def score_resume(parsed):
    #skill scoring
    tokenizer = RegexpTokenizer(r'\w+')
    str1 = " ".join(tokenizer.tokenize(str(parsed["skills"])))
    str2 = jd[sys.argv[2]]
    str2 = str2[list(str2.keys())[0]]
    a = set(str1.split())
    b = set(str2.split())
    c = a.intersection(b)

    #experience scoring

    return float(len(c)) / (len(a) + len(b) - len(c))

# @app.route('/',methods=['POST'])
# def index():


if __name__ == '__main__':
    # res = request.files['file']
    # print(request.data)
    # data = json.loads(request.data)
    # print(data['company'])
    # print(data['role'])
    files = {"file": open(sys.argv[1],"rb")}
    parsed = requests.post("http://localhost:9100/", files=files).text
    # print(parsed)
    parsed = json.loads(parsed)
    match = score_resume(parsed)

    clf = load("/Users/sandeepbalaji/Downloads/"+cl[sys.argv[2]])
    d = [{'College Tier': 1, 'Experience': 2, 'ResumeMatch': match, 'Cyber Security': sys.argv[3], 'Data Analyst': sys.argv[4], 'Quality Assurance':sys.argv[5],	'SDE 1':sys.argv[6],	'Software Intern':sys.argv[7]}]
    x_pred = pd.DataFrame(data=d)
    y_pred = clf.predict(x_pred)
    arr = clf.predict_proba(x_pred)
    probability_of_interview = arr[0][1]
    print(round(probability_of_interview*100,2))

# files = {"file": open("/Users/sandeepbalaji/Downloads/Resume-SMM.pdf","rb")}
