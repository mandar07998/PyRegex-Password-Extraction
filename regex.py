import numpy as np
import pandas as pd
import re
import os
import json
import itertools
import time


def removeNestings(a):
    output = []
    for i in a:
        if type(i) == list:
            for data in i:
                output.append(data)
        else:
            output.append(i)
    return output

def extension_extractor(language_used):
    exte_list = []
    with open('language.json') as language_json:
        data_language = json.load(language_json)
        for e, f in data_language.items():
            if e == language_used:
                for key3 in f:
                    if key3 == "primary_extension":
                        list_of_primaryExtensions_Python_Main = [f[key3]]
                        for elem in list_of_primaryExtensions_Python_Main:
                            exte_list.append(elem)
                    if key3 == "extensions":
                        list_of_Extensions_Python_Main = [f[key3]]
                        for elem in list_of_Extensions_Python_Main:
                            exte_list.append(elem)
        for c, d in data_language.items():
            for key in d:
                if key == "group":
                    if d[key] == language_used:
                        for key2 in d:
                            if key2 == "primary_extension":
                                list_of_primary_extensions_python = [d[key2]]
                                for elem in list_of_primary_extensions_python:
                                    exte_list.append(elem)
                            if key2 == "extensions":
                                list_of_extensions_python = [d[key2]]
                                for elem in list_of_extensions_python:
                                    exte_list.append(elem)
    return exte_list

def extension_checker(input_file_name, language_used):
    real_path = os.path.realpath(input_file_name)
    filename, file_extension = os.path.splitext(real_path)
    found = False
    languagesList = removeNestings(extension_extractor(language_used))
    for i in languagesList:
        if file_extension == i:
            found = True
            break
    return found

def removeStartAndEndData(result):
    newRes = []
    for res in result:
        newRes.append(res[1:len(res)-1])
    return newRes

def compactValues(data,language):

    data_val=data.values()
    data_val_list=list(data_val)
    r=re.compile("-----")
    newlist = list(filter(r.match, data_val_list))
    print(newlist)


    match_index = [key for key, val in enumerate(data_val_list)
                      if val in set(newlist)]
    print("The Match indices list is : " + str(match_index))
    print(type(match_index))
    int_list = list(map(int, match_index))
    print(int_list)
    list2=[]

    result_without_SSH=np.delete(data_val_list,int_list)
    result_without_SSH=list(result_without_SSH)
    print(result_without_SSH)
    print(type(result_without_SSH))
    result=''
    for i in result_without_SSH:


        if language == "Python":
            test1='["]'+i+'["]'+ "|"+ r'[\']'+i+'[\']'
            result=result+test1
        if language == "Java" or language =="DotNet":
            test1='["]'+i+'["]'
            result=result+test1
        if language == "Other":
            test1 = '["]'+i+'["]' + "|" + r'[\']'+i+'[\']' + "|" + r'[(]'+i+'[)]' + "|" + r'[ ]'+i+'[ ]'
            result=result + test1







    return result
with open('reegx.json') as json_file:
    data = json.load(json_file)
    cd=compactValues(data=data,language="Other")
    print(cd)


def findData(fileType,path):
    result = ''
    with open('reegx.json') as json_file:
        data = json.load(json_file)





        #print(data)
        file=open(path,'r',encoding="UTF-8").readlines()
        if fileType == "Python":
            res1=compactValues(data=data,language="Python")
            result = re.findall(res1 ,str(file))

        if fileType == "Java" or fileType == "DotNet":
            res1=compactValues(data=data,language="Java")
            result = re.findall(res1 ,str(file))
        if fileType == "Other":
            res1=compactValues(data=data,language="Other")
            result = re.findall(res1 ,str(file))
    result = removeStartAndEndData(result)
    return result

def findDataMain(inputFile):
    if extension_checker(input_file_name=inputFile, language_used="Python"):
        return findData(fileType="Python", path=inputFile)
    elif extension_checker(input_file_name=inputFile, language_used="Visual Basic"):
        return findData(fileType="DotNet", path=inputFile)
    elif extension_checker(input_file_name=inputFile, language_used="Java"):
        return findData(fileType="Java", path=inputFile)
    else:
        return findData(fileType="Other", path=inputFile)


start_time = time.time()
print(findDataMain("sample.txt"))
print("--- %s seconds ---" % (time.time() - start_time))





# Python program for KMP Algorithm
def KMPSearch(pat, txt):
    M = len(pat)
    N = len(txt)

    # create lps[] that will hold the longest prefix suffix
    # values for pattern
    lps = [0]*M
    j = 0 # index for pat[]

    # Preprocess the pattern (calculate lps[] array)
    computeLPSArray(pat, M, lps)

    i = 0 # index for txt[]
    while i < N:
        if pat[j] == txt[i]:
            i += 1
            j += 1

        if j == M:
            print ("Found pattern at index " + str(i-j))
            j = lps[j-1]

        # mismatch after j matches
        elif i < N and pat[j] != txt[i]:
            # Do not match lps[0..lps[j-1]] characters,
            # they will match anyway
            if j != 0:
                j = lps[j-1]
            else:
                i += 1

def computeLPSArray(pat, M, lps):
    len = 0 # length of the previous longest prefix suffix

    lps[0] # lps[0] is always 0
    i = 1

    # the loop calculates lps[i] for i = 1 to M-1
    while i < M:
        if pat[i]== pat[len]:
            len += 1
            lps[i] = len
            i += 1
        else:
            # This is tricky. Consider the example.
            # AAACAAAA and i = 7. The idea is similar
            # to search step.
            if len != 0:
                len = lps[len-1]

                # Also, note that we do not increment i here
            else:
                lps[i] = 0
                i += 1

#with open('fulldata.rpt', 'r',encoding="UTF-8") as file:
#    data = file.read().rstrip()

#txt=data
#pat = "AKIA1111111111111111"
#start_time = time.time()
#c=KMPSearch(pat, txt)
#print(c)
#print("--- %s seconds ---" % (time.time() - start_time))


data=open('reegx.json')
data=json.load(data)








