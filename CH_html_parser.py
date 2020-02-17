# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 20:38:42 2020

@author: yz391
"""

import json as js
from lxml import etree


    
    
       
def generate_tree(file_path):  #generate etree   
    with open(file_path,'r', encoding = 'utf-8') as fs:
        string = fs.read()
    tree = etree.HTML(string)   
    return tree
    
    
    

# course info
def get_course_info(tree): # return dict{'ID':{'title':ICS,'intro':'This course....'}}
    result = dict()
    trunks = tree.xpath("//span[@style = 'background-color: white; font-family: arial; color: black; font-size: 16px; font-weight: normal']")
    
    for trunk in trunks:
        titleID = trunk.xpath("./b/text()")[0].split()
        if len(titleID) > 0:
            ID = ' '.join(titleID[:2])
            ID = ID.split(' ')
            ID = '#'.join(ID)
            title = ' '.join(titleID[2:])
    
            intros = trunk.xpath(".//p/text()")
            if len(intros) > 1:
                intro = intros[-2]
            elif len(intros) == 0:
                intro = None
            else:
                intro = intros[0]
            
            inner = {}
            inner['title'] = title
            inner['intro'] = intro
            result[ID] = inner
            
    return result
    
    




# get session info  
def get_session_info(tree):    #return dict 
    # key --> courseID
    # value --> [dict1,dict2, ...]:
            # params:
            #        units, 
            #        class#, 
            #        session_time, 
            #        section 
            #        class_status, 
            #        grading, 
            #        instruction_mode, 
            #        course_location, 
            #        component 
            #        time
            #        instructor
            #        room
                    
    
    result = dict()
    texts = tree.xpath("//td[@style = 'background-color: white; font-family: arial; font-size: 12px;']//text()")
    i = 0
    while i < (len(texts)):
        if 'SHU' in texts[i] and len(texts[i]) < 20:
            inner = dict()
            
            #getting {   units, 
            #            class#, 
            #            session_time, 
            #            section }            
            units = texts[i+1]
            if len(units) < 5:
                inner['units'] = None
            else:
                inner['units'] = units.strip(' | ')              
            raw_class = texts[i+3].strip('| ')
            clas = raw_class.strip()
            inner['class#'] = clas                  
            inner['session_time'] = texts[i+5].strip('| ')
            inner['section'] = texts[i+7].strip()
                
             
            # getting {  class_status, 
            #            grading, 
            #            instruction_mode, 
            #            course_location, 
            #            component}        
            if texts[i+10] == 'Class Status:':
                k = 2
            else:
                k = 0
            inner['class_status'] = texts[i+10+k]
            inner['grading'] = texts[i+13+k].strip('| ')
            inner['instruction_mode'] = texts[i+15+k].strip()
            inner['course_location'] = texts[i+17+k].strip('| ')
            inner['component'] = texts[i+19+k].strip()
     
        
            # separate time, instructor, room from prof_time
            prof_time = texts[i+20+k].strip()            
            if len(prof_time) < 25:
                inner['instructor'] = None
                inner['time'] = None
                inner['room'] = None
            else:
                sep1 = prof_time.find('with')
                if sep1 == -1:
                    inner['instructor'] = None
                else:
                    inner['instructor'] = prof_time[sep1+4:].strip()
                
                sep2 = prof_time.find('at')
                if sep2 == -1:
                    inner['room'] = None
                    inner['time'] = prof_time[23:].strip()
                else:
                    inner['room'] = prof_time[sep2+2:sep1].strip()
                    inner['time'] = prof_time[23:sep2].strip()
                    
                
            # getting note info
            note_mess = ' '.join(texts[i+23+k:i+100])

            note = note_mess.split('\n\n')[1]
            note = note.strip()
            if len(note) > 0:
                inner['notes'] = note
            else:
                inner['notes'] = None

                    
            # putting sessions into dict[courseID]
            ID = texts[i]
            ID = ID.split()
            ID = '#'.join(ID)
            if ID in result:
                result[ID].append(inner)
            else:
                result[ID] = [inner] 
  
            i += 20
        else:
            i += 1
           
                    
    return result
            

def get_recit_info(session_info):  #return dict: lecture_class# --> [recitation_class#,....]
    result = {}
    parent_components = ['Lecture','Project','Studio','Seminar']

    for sessions in session_info.values():
        lectures = []
        recits = []
        for session in sessions:
            if session['component'] in parent_components:
                if len(recits) > 0:
                    for lecture in lectures:
                        result[lecture] = recits
                        lectures = [session['class#']]
                        recits = []
                else:
                    lectures.append(session['class#'])
            else:
                recits.append(session['class#'])
                
        if len(lectures) > 0:
            for lecture in lectures:
                result[lecture] = recits

    return result                    



def main():
    ID_shift = {'ART-SHU#210':'ART-SHU#310','ART-SHU#1910':'ART-SHU#1911','CHIN-SHU#406': 'CHIN-SHU#430'}
    data = {}
    with open('C:/Users/yz391/Desktop/Course_info/subject_name.txt','r',encoding = 'utf-8') as fs:
        subjects = fs.read().split('\n')
    
    for subject in subjects:
        file_path = 'C:/Users/yz391/Desktop/Course_info/html/' + subject + '.html'
        tree = generate_tree(file_path)
        course_info = get_course_info(tree)
        session_info = get_session_info(tree)
        recit_info = get_recit_info(session_info)
        
        subject_bundle = {} # courseID -->  title (string), intro(string), session(list of dicts)
        for ID  in course_info.keys():
            if ID in ID_shift:
                nID = ID_shift[ID]
            else:
                nID = ID
            
            course_bundle = {} # 'session' --> unit, class# .....
            session_list = session_info[nID]
            course_bundle['title'] = course_info[ID]['title']
            course_bundle['into'] = course_info[ID]['intro']
            course_bundle['session'] = session_list
            lecture_to_recit = {}
            for session in session_list:
                class_num = session['class#']
                if class_num in recit_info:
                    recitations = recit_info[class_num]
                    if len(recitations) > 0:
                        lecture_to_recit[class_num] = recitations
                    else:
                        lecture_to_recit[class_num] = None
                else:
                    lecture_to_recit[class_num] = None
                        
            
            course_bundle['lecture_to_recit']= lecture_to_recit
            subject_bundle[nID] = course_bundle
            
        data[subject] = subject_bundle
    
    js_object = js.dumps(data)
    
    with open('C:/Users/yz391/Desktop/Course_info/course_data.js','w',encoding = 'utf-8') as fs:
        fs.write(js_object)
        
    
            

if __name__ == "__main__":
    main()









