from flask import Flask, session, app, render_template, request, Markup
import sys, io, re
import os, base64
from io import StringIO
from datetime import datetime
import time
import random
import pandas as pd
import requests


app = Flask(__name__)

# get root path for account in cloud
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# survey page
@app.route("/", methods=['POST', 'GET'])
def survey_page():


    _1 =  {"train":"1,2,3"  , "test" :"1,2,3" }		
    _2 =  {"train":"3,1,2"  , "test": "2,3,1" }	
    _3 =  {"train":"2,3,1"	, "test" :"3,1,2" }
    _4 =  {"train":"1,2,3"	, "test" :"3,1,2" }		
    _5 =  {"train":"3,1,2"	, "test" :"1,2,3" }		
    _6 =  {"train":"2,3,1"	, "test" :"2,3,1" }		
    _7 =  {"train":"1,2,3"	, "test" :"2,3,1" }		
    _8 =  {"train":"3,1,2"	, "test" :"3,1,2" }		
    _9 =  {"train":"2,3,1"  , "test" :"1,2,3" }

    methods = [_1, _2, _3, _4, _5, _6, _7, _8, _9]

    method = random.choice(methods)

    t = ["binary", "hateval", "obj_number", "past_present", "sentence_length", "subj_number"]
    tasks = {'binary':["NEGATIVE", "POSITIVE"], 'hateval': [ "NO HATE SPEECH", "HATE SPEECH"], 'obj_number':[ 'SINGULAR', 'PLURAL'],
             'past_present': ['PAST', "PRESENT"], 'sentence_length':[0,1,2,3,4,5], 'subj_number':[ 'SINGULAR', 'PLURAL']}

    train = method['train'].split(",")
    test = method['test'].split(",")

    
    message = ''
    first_name = ''
    last_name = ''
   
    task = random.choice(t)

    #at index 0: no explanation
    #at index 1: lime
    #at index 2: shap
    dropdown_list = tasks[task] 
    questions = [i for i in range(25)]

    #train data
    pred_location = "http://AnaValeriaGonzalez.github.io/data/stimuli_presentations/preds/"+task+"/train_set"+train[0]+".csv"
    lime_location = "http://AnaValeriaGonzalez.github.io/data/stimuli_presentations/lime/"+task+"/train_set"+train[1]+"/"
    shap_location = "http://AnaValeriaGonzalez.github.io/data/stimuli_presentations/shap/"+task+"/train_set"+train[2]+"/"

    answerfile_LIME = "http://AnaValeriaGonzalez.github.io/data/stimuli_presentations/preds/"+task+"/train_set"+train[1]+".csv"
    answerfile_SHAP = "http://AnaValeriaGonzalez.github.io/data/stimuli_presentations/preds/"+task+"/train_set"+train[2]+".csv"


    s=requests.get(answerfile_LIME).content
    data = pd.read_csv(StringIO(s.decode('utf-8')))
    ids = data['Unnamed: 0'].tolist()
    
    labels = [dropdown_list[int(i)] for i in data['train_model_pred'].tolist()]
    texts = data['train_text'].tolist()

    displays = []
    for i in ids:
        displays.append(lime_location+str(i)+".png")

    #test data

    testpred_location = "http://AnaValeriaGonzalez.github.io/data/stimuli_presentations/preds/"+task+"/test_set"+test[0]+".csv"
    testlime_location = "http://AnaValeriaGonzalez.github.io/data/stimuli_presentations/lime/"+task+"/test_set"+test[1]+"/"
    testshap_location = "http://AnaValeriaGonzalez.github.io/data/stimuli_presentations/shap/"+task+"/test_set"+test[2]+"/"

    testanswerfile_LIME = "http://AnaValeriaGonzalez.github.io/data/stimuli_presentations/preds/"+task+"/test_set"+test[1]+".csv"
    testanswerfile_SHAP = "http://AnaValeriaGonzalez.github.io/data/stimuli_presentations/preds/"+task+"/test_set"+test[2]+".csv"


    s=requests.get(testanswerfile_LIME).content
    testdata = pd.read_csv(StringIO(s.decode('utf-8')))

    testids = testdata['Unnamed: 0'].tolist()
    testlabels = [dropdown_list[int(i)] for i in testdata['test_model_pred'].tolist()]
    testtexts = testdata['test_text'].tolist()

    testdisplays = []
    for i in testids:
        testdisplays.append(testlime_location+str(i)+".png")
        

     # check that we have all the required fields to append to file
    
    DIR = BASE_DIR + '/surveys/data.csv'
    
    if request.method == 'POST':  
        first_name = request.form['first_name']
        last_name = request.form['last_name']
       

       
        # create a unique timestamp for this entry
        entry_time = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')


            # save to file and send thank you note
           
        with open(DIR,'a+') as myfile: # use a+ to append and create file if it doesn't exist
            myfile.write(
                str(entry_time) + ',' + '\n')
        
        # return thank-you message
        message = '<div class="w3-row-padding w3-padding-16 w3-center"><H2><font style="color:blue;">Thank you for taking the time to complete this survey</font></H2></div>'

        
    
    return render_template('survey.html',
            message = Markup(message),
            first_name = first_name,
            last_name = last_name,
            dropdown_list = dropdown_list, 
            questions = questions,
            task = task,
            displays = displays, 
            labels=labels,
            testlabels=testlabels,
            testdisplays=testdisplays,
            texts=texts,
            testtexts=testtexts,
            dir=DIR)


# used only in local mode
if __name__=='__main__':
    app.run(debug=True)         


