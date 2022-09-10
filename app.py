# Import required libraries
from flask import Flask, redirect,request,render_template,flash,url_for,send_from_directory
import os
from PIL import Image,ImageDraw
import cgi, os
import cgitb; cgitb.enable()
import PyPDF2
import re
form = cgi.FieldStorage()
import re
from collections import Counter
import string
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image as img  
import pytesseract as PT  
import sys 
import pdf2image
from pdf2image import convert_from_path as CFP  
import pytesseract

#1. Install tesseract using windows installer available at: https://github.com/UB-Mannheim/tesseract/wiki

#2. Note the tesseract path from the installation.Default installation path at the time the time of this edit was: C:\Users\USER\AppData\Local\Tesseract-OCR. It may change so please check the installation path.

#3. pip install pytesseract

#4. Set the tesseract path in the script before calling image_to_string:

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"




app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if request.values['include_area']:
            text_content=[]
            text_content1=[]
            text_content_tmp=[]
            text_content_1=[]
            tmp=0
            length=0

            #Opening the resume that has been uploaded in Flask
            fi = request.files['file']

            #obtain values of Keywords to Search
            text_content_tmp = request.values['include_area']

            #Split the words seperated by commas
            text_content1=text_content_tmp.split(',')

            #Remove the unwanted whtespaces in words and added to new list
            for i in text_content1:
                j=i.replace(' ','')
                text_content.append(j)

            #create a copy of Keywords List  
            text_content2=text_content_tmp.split(',')

            #Keep keywords in the form skill1/skill2 from keywords list2
            letters = set('/')
            text_content2 = [item for item in text_content2 if letters & set(item)]
            for i in text_content2:
                j=i.replace(' ','')
                text_content_1.append(j)

            #Obtain the filename of uploaded file
            fil = os.path.basename(fi.filename)            

            #Save the Resume locally
            fi.save(os.path.join("static/uploads",fil))
            PDF_file_1 ="static/uploads//"+fil

            #Download Poppler from "https://blog.alivate.com.au/poppler-windows" Then extract it.In the code section just add poppler bin_path  
            pages_1 =pdf2image.convert_from_path(PDF_file_1,poppler_path="C:/Users/Adfolks User/Downloads/poppler-0.68.0_x86/poppler-0.68.0/bin/") 

            # Now, we will create a counter for storing images of each page of PDF to image  
            image_counter1 = 1  

            # Iterating through all the pages of the pdf file stored above  

            for page in pages_1:  
                
                # PDF page n: page_n.jpg 
                filename1 = "Page_no_" + str(image_counter1) + " .jpg"  
                 # Now, we will save the image of the page in system  
                page.save(filename1, 'JPEG')  
                # Then, we will increase the counter for updating filenames  
                image_counter1 = image_counter1 + 1  
                # Variable for getting the count of the total number of pages  
            filelimit1 = image_counter1 - 1 
                # then, we will create a text file for writing the output  
            out_file1 = "output_text.txt" 
            # Now, we will open the output file in append mode so that all contents of the # images will be added in the same output file.  
            f_1 = open(out_file1,"a+")
            f_1.truncate(0)
            f_1.seek(0)  
    
 
         # Iterating from 1 to total number of pages 
        for K in range(1, filelimit1 + 1):
            filename1 = "Page_no_" + str(K) + " .jpg"  
            
    # Here, we will write a code for recognizing the text as a string variable in an image file by using the pytesserct module  
            text = str(((PT.image_to_string (img.open (filename1)))))  
    
    # : The recognized text will be stored in variable text  
    # : Any string variable processing may be applied to text content  
    # : Here, basic formatting will be done:-  
      
            text = text.replace('-\n', '')      
    
    # At last, we will write the processed text into the file.  
            f_1.write(text) 
# Closing the file after writing all the text content.
        f_1.close()
              

        # Initializie score counters 
        include = 0
        
        # Create an empty list where the scores will be stored
        scores = []
           

            # open the file for reading file
        file=open(out_file1, 'r+')

        #Read a text file into string and strip newlines
        text = file.read().replace('\n', '')

        #Convert the string into lowercase
        text = text.lower()

        #Removing Digits from a String
        text = re.sub(r'\d+','',text)

        #remove punctuation marks from a string 
        text = text.translate(str.maketrans('','',string.punctuation))

        #Search the keywords in text file and append the keywords to new list 'scores' if found
        for word in text_content:
            if word in text:
                include +=1
                scores.append(word)
        
        #Split the keyword of type skill1/skill2 in text file and append the keywords to new list 'scores' if found
        for tmp in text_content_1:
            lis=[]
            lis=tmp.split('/')
            for i in lis:
                if i in text:
                    if tmp in text_content:
                        text_content.remove(tmp)
                    text_content.append(i)
                    include +=1
                    scores.append(i)
        #length of the keywords list
        length=len(text_content) 
         
    #compare the count of Keywords found in pdf  vs count of keywords to search 
    if include/length >= 0.75:
        return "Shortlist<br>The words to search"+str(text_content)+"<br> The words found in pdf"+str(scores)+"<br>The count of words"+str(include)
    else:
        return "Reject<br>The words to search"+str(text_content)+"<br> The words found in pdf"+str(scores)+"<br>The count of words"+str(include)

# Create a data frame with the scores summary
            #summary = pd.DataFrame(scores,index=text_content,columns=['score']).sort_values(by='score',ascending=False)
            #summary
            # Create pie chart visualization
            #pie = plt.figure(figsize=(10,10))
            #plt.bar(summary.index,summary['score'],width=0.8, bottom=None,align='center')
            #plt.title('Industrial Engineering Candidate - Resume Decomposition by Areas')
            #plt.axis('equal')
            #plt.xlabel("dfsdf")
            #plt.show()

            # Save pie chart as a .png file
            #pie.savefig('resume_screening_results.png')
        
        #return "The words to search"+str(text_content)+"<br> "+str(summary)+"<br>The count of words"+str(count)
        
        #if found_list:
          
          #  return str(count)+"words found"
        
        #else:
          #  return "No Keywords found"
        
        
            
if __name__ == "__main__":
    app.run(debug=True,port=5005)
   