from flask import Flask, session, app, render_template, request, Markup
import sys, io, re
import os, base64
from io import StringIO
from datetime import datetime
import time
import random

app = Flask(__name__)

# get root path for account in cloud
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# survey page
@app.route("/", methods=['POST', 'GET'])
def survey_page():


    _1 =  {"train":"t1 t2,t3"   , "test" :"t1, t2, t3" }		
    _2 =  {"train":"t3,t1,t2"   , "test": "t2, t3, t1" }	
    _3 =  {"train":"t2, t3, t1"	, "test" :"t3, t1, t2" }
    _4 =  {"train":"t1, t2, t3"	, "test" :"t3, t1, t2" }		
    _5 =  {"train":"t3,t1,t2"	, "test" :"t1, t2, t3" }		
    _6 =  {"train":"t2, t3, t1"	, "test" :"t2, t3, t1" }		
    _7 =  {"train":"t1 t2,t3"	, "test" :"t2, t3, t1" }		
    _8 =  {"train":"t3,t1,t2"	, "test" :"t3, t1, t2" }		
    _9 =  {"train":"t2, t3, t1"	, "test" :"t1, t2, t3" }

    methods = [_1, _2, _3, _4, _5, _6, _7, _8, _9]

    method = random.choice(methods)

    t = ["binary", "hateval", "obj_number", "past_present", "sentence_length", "subj_number"]
    tasks = {'binary':["POSITIVE", "NEGATIVE"], 'hateval': ["HATE SPEECH", "NO HATE SPEECH"], 'obj_number':['PLURAL', 'SINGULAR'],
             'past_present': ['PAST', "PRESENT"], 'sentence_length':[1,2,3,4,5], 'subj_number':['PLURAL', 'SINGULAR']}

    train = method['train'].split(",")
    test = method['test'].split(",")

    
    message = ''
    first_name = ''
    last_name = ''
   
    task = random.choice(t)

    print(train, test)

    are_you_happy = "choose one..."

     # check that we have all the required fields to append to file
    
    dropdown_list = tasks[task] 
    questions = [i for i in range(25)]
  
    if request.method == 'POST':  
        first_name = request.form['first_name']
        last_name = request.form['last_name']
       

        

        # check that essential fields have been filled
        
        are_you_happy = request.form['are_you_happy']
        
        # create a unique timestamp for this entry
        entry_time = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')


            # save to file and send thank you note
            
        with open(BASE_DIR + '/surveys/data.csv','a+') as myfile: # use a+ to append and create file if it doesn't exist
            myfile.write(
                str(entry_time) + ',' +
                str(last_name) + ',' + '\n')
        
        # return thank-you message
        message = '<div class="w3-row-padding w3-padding-16 w3-center"><H2><font style="color:blue;">Thank you for taking the time to complete this survey</font></H2></div>'

    
    return render_template('survey.html',
            message = Markup(message),
            first_name = first_name,
            last_name = last_name,
            are_you_happy = are_you_happy, 
            dropdown_list = dropdown_list, 
            questions = questions,
            task = [task])


# used only in local mode
if __name__=='__main__':
    app.run(debug=True)         


