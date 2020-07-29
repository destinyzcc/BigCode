#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import zipfile
import xlwt
import pandas as pd
import openpyxl
import copy
import time
import datetime

os.chdir('D:/Python project/BigCode/download')
file_chdir = os.getcwd()
file_tem = []
dic_list = []
dic = {}
dic_singleQue = []
dic_ddlBigger3 = []
dic_ddlSmaller3 = []
file_comp = []
questionData = []
allData = []
cases = []
inputs = []
inputsc = []
tempInput = ''
outputs = []
outputsc = []
tempOutput = ''
codeNumbers = []
codeBigNumbers = []
specialKeyWords = ["Yes", "No", "YES", "NO", "yes", "no", "false", "true", "False", "True", "FALSE", "TRUE", "NONE",
                   "None", "none", "UP", "DOWN", "OK", "odd", "even", "Case", "Elephant"
    , "Alien", "Bear", "III", "IV", "MCMXCIV", "IX", "Pending", "Draw", "Poor", "Alex", "Happy", "duplicates",
                   "Infinite", "solutions", "solution", "x", "pairs"
    , "noway"]
specialKeyNumbers = [26, 30, 31, 0,10000]
singleCharactersI = []
singleCharactersO = []
currentQue = ''
code = ''
id = ''
type = ''
score = 0
queName = ''
count = 0
ddlDay = -1
faceCaseCount = 0
faceCaseCasesI = []
stri = "i"
stro = "o"
faceCaseCasesO = []
faceTime = 0
temp = {}
testcases = '.mooctest/testCases.json'
answer = '.mooctest/answer.py'
codename = 'main.py'
singleSubmit = 'D:/Python project/BigCode/part2/data/singleSubmit.xlsx'
singleQue = 'D:/Python project/BigCode/part2/data/singleQue.xlsx'
quePath = 'D:/Python project/BigCode/part2/data/que.xlsx'
personalType = 'D:/Python project/BigCode/part2/data/personalType.xlsx'
personalAll = 'D:/Python project/BigCode/part2/data/personalAll.xlsx'


def export_excel(export, filepath):
    # 将字典列表转换为DataFrame
    pf = pd.DataFrame(list(export))
    # 指定字段顺序
    # order = ['id', 'type', 'queName', 'count', 'faceTime','allCases', 'faceCases', 'originScore', 'realScore',]
    # pf = pf[order]
    columns_map = {
        'id': '用户id',
        'type': '类型',
        'queName': '题目',
        'count': '提交次数',
        'faceTime': '面向用例提交次数',
        'allCases': '总用例个数',
        'faceCases': '面向用例个数',
        'originScore': '原分数',
        'realScore': '实际分数',
        'people': '答题人数',
        'allCount': '总提交次数',
        'allFace': '总面向用例提交次数',
        'allOrigin': '总原始分',
        'aveOrigin': '原始平均分',
        'allReal': '总真实分',
        'aveReal': '真实平均分',
        'queCount': '答题数量',
        'faceQue': '面向对象题目数量',
        'allQue': '总题目数量'
    }
    pf.rename(columns=columns_map, inplace=True)
    # 指定生成的Excel表格名称
    file_path = pd.ExcelWriter(filepath)
    # 替换空单元格
    pf.fillna(' ', inplace=True)
    # 输出
    pf.to_excel(file_path, encoding='utf-8', index=False)
    # 保存表格
    file_path.save()


def getTargetNumbers(s, t):
    numbers = []
    s = str(s)
    i = 0
    l = len(s)
    while i < l:
        num = ''
        symbol = s[i]
        while '0' <= symbol <= '9':  # symbol.isdigit()
            num += symbol
            i += 1
            if i < l:
                symbol = s[i]
            else:
                break
        i += 1
        if num != '' and num != 'n':
            numbers.append(int(num))
            if int(num) > 100 and t=='c':
                codeBigNumbers.append(int(num))
    if t == 'i':
        inputs.append(numbers)
    elif t == 'o':
        outputs.append(numbers)
    else:
        return numbers
    return


# 获取s中出现的字母，s为字符串，t为类型（input,outout,code三种类型）
def getTargetCharacter(s, t):
    characters = []
    s = str(s)
    i = 0
    l = len(s)
    while i < l:
        word = ''
        symbol = s[i]
        while 'a' <= symbol <= 'z' or 'A' <= symbol <= 'Z':  # symbol.isdigit()
            word += symbol
            i += 1
            if i < l:
                symbol = s[i]
            else:
                break
        i += 1
        if word != '' and word != 'n':
            characters.append(word)
    if t == 'i':
        inputsc.append(characters)
    elif t == 'o':
        outputsc.append(characters)
    else:
        return characters
    return


# 判断是否有面向用例的情况，code为代码中的数字组/字母组,case为input/output数组的一个元素，检查case是否为code的子数组
def judgeFaceCases(code, case, t):
    len1 = len(code)
    len2 = len(case)
    if len1 == 0 or len2 == 0:
        return 0

    if len2 == 1 and len(str(case[0])) == 1:  # 小于9的数字跳过，有的用户会写注释，中文会被译码为带数字的字符串
        if (str(case[0]).isdigit()):
            if 0 <= case[0] <= 9:
                if (t == 'i'):
                    singleCharactersI.append(case[0])
                else:
                    singleCharactersO.append(case[0])
        else:
            if (t == 'i'):
                singleCharactersI.append(case[0])
            else:
                singleCharactersO.append(case[0])
        return 0
    if len2 == 1:
        for i in range(0, len(specialKeyWords)):
            if case[0] == specialKeyWords[i]:
                return 0
        for i in range(0, len(specialKeyNumbers)):
            if case[0] == specialKeyNumbers[i]:
                return 0
    if len1 < len2: return 0
    for i in range(0, len1 - len2 + 1):
        if code[i:i + len2] == case:
            if (t == 'i'):
                faceCaseCasesI.append(case)
                return 1
            else:
                faceCaseCasesO.append(case)
                return 1
    return 0


# 判断直接输出一个数字或者字母的面向用例
def singleJudge(code):
    codestr = str(code)
    str1 = 'print('
    str2 = 'print(\''
    str3 = 'print("'
    global singleCharactersO
    global singleCharactersI

    for i in range(0, len(singleCharactersO)):
        if str(singleCharactersO[i]).isdigit():
            if codestr.find(str1 + str(singleCharactersO[i]) + ')') >= 0 or codestr.find(
                    str1 + str(singleCharactersO[i]) + ',') >= 0:
                faceCaseCasesO.append(singleCharactersO[i])
                return 1
        if codestr.find(str2 + str(singleCharactersO[i]) + '\'') >= 0:
            faceCaseCasesO.append(singleCharactersO[i])
            return 1
        if codestr.find(str3 + str(singleCharactersO[i]) + '"') >= 0:
            faceCaseCasesO.append(singleCharactersO[i])
            return 1

    return 0


def BigNumberJudge(input, output):
    global codeBigNumbers
    for i in range(0, len(codeBigNumbers)):
        if codeBigNumbers[i] in input:
            faceCaseCasesI.append(codeBigNumbers[i])
            return 1
        if codeBigNumbers[i] in output:
            faceCaseCasesO.append(codeBigNumbers[i])
            return 1
    return 0


for root, dirs, files in os.walk(file_chdir):
    for file in files:
        file_tem.append(file)
        data = os.path.splitext(file)[0].split(',')
        file_tem.append(data[0])
        file_tem.append(data[1])
        file_tem.append(data[2])  # score
        file_tem.append(str(data[4]).replace(" ", ""))

        timeStamp = float(str(data[3])[0:-3])
        timeArray = time.localtime(timeStamp)
        time1 = time.strftime("%Y-%m-%d", timeArray)
        d1 = datetime.datetime(int(time1[0:4]), int(time1[5:7]), int(time1[8:]))
        d2 = datetime.datetime(2020, 4, 1)
        file_tem.append(str((d2 - d1).days))  # ddlday
        file_comp.append(file_tem)
        file_tem = []
file_comp.sort(key=lambda x: (x[1], x[2], x[4], x[3]))
print("success")
print(str(file_comp[0][0]))

for file in file_comp:
    if '.zip' not in str(file[0]):
        continue
    if file[1] != id:
        id = int(file[1])
    if file[2] != type:
        type = file[2]
    if str(file[4]).split('_')[0] != queName:
        queName = str(file[4]).split('_')[0]
        count = 0
        score = 0
    if file[3] != score:
        score = file[3]
    if str(file[4]).split('_')[0] == queName:
        count += 1
    if int(file[5]) != ddlDay:
        ddlDay = int(file[5])
    questionData.append(id)
    questionData.append(type)
    questionData.append(queName)
    questionData.append(score)
    questionData.append(count)
    questionData.append(file[0])
    questionData.append(ddlDay)
    allData.append(questionData)
    questionData = []
print('success')

ddlb3 = 0
ddlb3_face = 0
ddls3 = 0
ddls3_face = 0
for data in allData:
    # print(data[4], data[5])
    if '.zip' not in str(data[5]):
        continue
    try:
        read_hey = zipfile.ZipFile(data[5])
        zipname = read_hey.namelist()[0]
        if '.zip' in zipname:
            fp = read_hey.open(zipname)
            read_code = zipfile.ZipFile(fp)
            code = read_code.open(codename).read()  # 获取当前提交代码
            if data[4] == 1:
                if len(dic_list) != 0:
                    temp = copy.deepcopy(dic_list[-1])
                    temp['faceTime'] = faceTime
                    temp['bigger3Submit'] = ddlb3
                    temp['bigger3Face'] = ddlb3_face
                    temp['smallerEqual3Submit'] = ddls3
                    temp['smallerEqual3Face'] = ddls3_face
                    faceTime = 0
                    ddlb3 = 0
                    ddlb3_face = 0
                    ddls3 = 0
                    ddls3_face = 0
                    dic_singleQue.append(temp)
                f = read_code.open(testcases)
                cases = json.load(f)
        else:
            continue
        for i in range(0, len(cases)):
            tempInput = ''.join(cases[i]['input'])
            tempOutput = ''.join(cases[i]['output'])
            getTargetNumbers(tempInput, 'i')
            getTargetNumbers(tempOutput, 'o')
            getTargetCharacter(tempInput, 'i')
            getTargetCharacter(tempOutput, 'o')
        codeBigNumbers = []
        codeCharacter = getTargetCharacter(code, 'c')
        codeNumbers = getTargetNumbers(code, 'c')
        for k in range(0, len(inputs)):  # 遍历input/output数组，检查是否有面向用例的情况
            faceCaseNumber = max(judgeFaceCases(codeNumbers, outputs[k], 'o'),
                                 judgeFaceCases(codeNumbers, inputs[k], 'i'))
            faceCaseCharacter = max(judgeFaceCases(codeCharacter, outputsc[k], 'o'),
                                    judgeFaceCases(codeCharacter, inputsc[k], 'i'))
            faceSingleCharacter = singleJudge(code)
            singleCharactersO = []
            singleCharactersI = []
            faceBigNumber = BigNumberJudge(inputs[k], outputs[k])
            faceCaseCount += max(faceCaseCharacter, faceCaseNumber, faceSingleCharacter, faceBigNumber)
        codeBigNumbers=[]
        faceBigNumber=[]
        if str(code).count('\n') == 1:
            faceCaseCount = len(cases)
        countI = 0
        countO = 0
        len1=len(faceCaseCasesI)
        len2=len(faceCaseCasesO)
        print(data[0], end=' ')
        print(data[1], end=' ')
        print(data[2], end=' ')
        for p in range(0, len1):
            if isinstance(faceCaseCasesI[p], list):
                if str(faceCaseCasesI[p][0]).isdigit():
                    if len(faceCaseCasesI[p])<=5:
                        if (max(faceCaseCasesI[p]) <= 6 and len(faceCaseCasesI[p]) <= 3) or (max(faceCaseCasesI[p]) <= 3 and len(faceCaseCasesI[p]) > 3):
                            faceCaseCount = faceCaseCount - 1
                            countI = countI + 1
                            if countI >= len1:
                                faceCaseCount = 0
        for p in range(0, len2):
            if isinstance(faceCaseCasesO[p], list):
                if str(faceCaseCasesO[p][0]).isdigit():
                    if len(faceCaseCasesO[p]) <= 5 :
                        if (max(faceCaseCasesO[p]) <= 6 and len(faceCaseCasesO[p]) <= 3) or (max(faceCaseCasesO[p]) <= 3 and len(faceCaseCasesO[p]) > 3):
                            faceCaseCount = faceCaseCount - 1
                            countO = countO + 1
                            if countO >= len2:
                                faceCaseCount = 0
        faceCaseCasesI = []
        faceCaseCasesO = []
        if faceCaseCount > 0:
            faceTime += 1
        realScore = float(data[3]) - faceCaseCount / len(cases) * 100
        if realScore < 0:
            realScore = 0
        dic = {'id': data[0], 'type': data[1], 'queName': data[2], 'count': data[4], 'faceTime': '',
               'allCases': len(cases),
               'faceCases': faceCaseCount, 'originScore': data[3], 'realScore': realScore, 'dayRemain': data[6]}
        dic_list.append(dic)
        if int(data[6]) > 3:
            ddlb3 = copy.deepcopy(int(data[4]))
            ddlb3_face = copy.deepcopy(faceTime)
        else:
            ddls3 = int(data[4]) - ddlb3
            ddls3_face = faceTime - ddlb3_face
        dic = {}
        print("第%d次提交" % (data[4]), end=' ')
        print("本题共%d个测试用例" % (len(cases)), end=' ')
        print("本次提交中面向用例个数为：%d" % (faceCaseCount), end=' ')
        faceCaseCount = 0
        print()
        faceCaseCases = []
        inputs = []
        outputs = []
        inputsc = []
        outputsc = []
    except:
        "zipfile.BadZipFile: File is not a zip file"

temp = copy.deepcopy(dic_list[-1])
temp['faceTime'] = faceTime
temp['bigger3Submit'] = ddlb3
temp['bigger3Face'] = ddlb3_face
temp['smallerEqual3Submit'] = ddls3
temp['smallerEqual3Face'] = ddls3_face
faceTime = 0
ddlb3 = 0
ddlb3_face = 0
ddls3 = 0
ddls3_face = 0
dic_singleQue.append(temp)
for x in dic_list:
    del x['faceTime']
print('success')

if __name__ == '__main__':
    export_excel(dic_list, singleSubmit)
    export_excel(dic_singleQue, singleQue)

    dic_singleQue.sort(key=lambda x: (x['type'], x['queName']))
    queName = ''
    type = ''
    allOrigin = 0
    allReal = 0
    allCount = 0
    allFace = 0
    faceQue = 0
    count = 0

    dic_Que = []
    for que in dic_singleQue:
        if queName != que['queName']:
            if allCount != 0:
                dic = {'type': type, 'queName': queName, 'people': count,
                       'facePeople': faceQue, 'scale1': faceQue / count, 'allCount': allCount,
                       'allFace': allFace, 'scale2': allFace / allCount, 'allOrigin': allOrigin,
                       'aveOrigin': allOrigin / count, 'allReal': allReal, 'aveReal': allReal / count,
                       'bigger3Submit': ddlb3,
                       'bigger3Face': ddlb3_face, 'smallerEqual3Submit': ddls3, 'smallerEqual3Face': ddls3_face}
                dic_Que.append(dic)
            queName = que['queName']
            allOrigin = 0
            allReal = 0
            allCount = 0
            allFace = 0
            count = 0
            faceQue = 0
            ddlb3 = 0
            ddlb3_face = 0
            ddls3 = 0
            ddls3_face = 0
            dic = {}
        if type != que['type']:
            type = que['type']
        allOrigin += float(que['originScore'])
        allReal += float(que['realScore'])
        allCount += int(que['count'])
        allFace += int(que['faceTime'])
        ddlb3 += int(que['bigger3Submit'])
        ddlb3_face += int(que['bigger3Face'])
        ddls3 += int(que['smallerEqual3Submit'])
        ddls3_face += int(que['smallerEqual3Face'])
        if float(que['originScore']) != float(que['realScore']):
            faceQue += 1
        count += 1
    dic = {'type': type, 'queName': queName, 'people': count,
           'facePeople': faceQue, 'scale1': faceQue / count, 'allCount': allCount,
           'allFace': allFace, 'scale2': allFace / allCount, 'allOrigin': allOrigin,
           'aveOrigin': allOrigin / count, 'allReal': allReal, 'aveReal': allReal / count, 'bigger3Submit': ddlb3,
           'bigger3Face': ddlb3_face, 'smallerEqual3Submit': ddls3, 'smallerEqual3Face': ddls3_face}
    dic_Que.append(dic)
    export_excel(dic_Que, quePath)

    dic_singleQue.sort(key=lambda x: (x['id'], x['type'], x['queName']))
    queName = ''
    type = ''
    allOrigin = 0
    allOrigin_All = 0
    allReal = 0
    allReal_All = 0
    allCount = 0
    allCount_All = 0
    allFace = 0
    allFace_All = 0
    count = 0
    count_All = 0
    faceQue = 0
    faceQue_All = 0
    id = 0
    ddlb3 = 0
    ddlb3_face = 0
    ddls3 = 0
    ddls3_face = 0
    ddlb3_All = 0
    ddlb3_face_All = 0
    ddls3_All = 0
    ddls3_face_All = 0
    dic = {}
    dic_Personal_type = []
    dic_Personal_all = []
    for que in dic_singleQue:
        if type != que['type']:
            if id != 0:
                dic = {'id': id, 'type': type, 'queCount': count, 'faceQue': faceQue, 'allCount': allCount,
                       'allFace': allFace, 'allOrigin': allOrigin,
                       'aveOrigin': allOrigin / count, 'allReal': allReal, 'aveReal': allReal / count,
                       'bigger3Submit': ddlb3,
                       'bigger3Face': ddlb3_face, 'smallerEqual3Submit': ddls3, 'smallerEqual3Face': ddls3_face}
                dic_Personal_type.append(dic)
            type = que['type']
            allOrigin = 0
            allReal = 0
            allCount = 0
            allFace = 0
            count = 0
            faceQue = 0
            ddlb3 = 0
            ddlb3_face = 0
            ddls3 = 0
            ddls3_face = 0
            dic = {}
        if id != que['id']:
            if id != 0:
                dic = {'id': id, 'allQue': 200, 'queCount': count_All, 'faceQue': faceQue_All,
                       'allCount': allCount_All, 'allFace': allFace_All, 'allOrigin': allOrigin_All,
                       'aveOrigin': allOrigin_All / 200, 'allReal': allReal_All, 'aveReal': allReal_All / 200,
                       'bigger3Submit': ddlb3_All, 'bigger3Face': ddlb3_face_All,
                       'smallerEqual3Submit': ddls3_All, 'smallerEqual3Face': ddls3_face_All}
                dic_Personal_all.append(dic)
            id = que['id']
            allOrigin_All = 0
            allReal_All = 0
            allCount_All = 0
            allFace_All = 0
            count_All = 0
            faceQue_All = 0
            ddlb3_All = 0
            ddlb3_face_All = 0
            ddls3_All = 0
            ddls3_face_All = 0
            dic = {}
        allOrigin += float(que['originScore'])
        allReal += float(que['realScore'])
        allCount += int(que['count'])
        allFace += int(que['faceTime'])
        allOrigin_All += float(que['originScore'])
        allReal_All += float(que['realScore'])
        allCount_All += int(que['count'])
        allFace_All += int(que['faceTime'])
        ddlb3 += int(que['bigger3Submit'])
        ddlb3_face += int(que['bigger3Face'])
        ddls3 += int(que['smallerEqual3Submit'])
        ddls3_face += int(que['smallerEqual3Face'])
        ddlb3_All += int(que['bigger3Submit'])
        ddlb3_face_All += int(que['bigger3Face'])
        ddls3_All += int(que['smallerEqual3Submit'])
        ddls3_face_All += int(que['smallerEqual3Face'])
        if float(que['originScore']) != float(que['realScore']):
            faceQue_All += 1
            faceQue += 1
        count += 1
        count_All += 1
    dic = {'id': id, 'type': type, 'queCount': count, 'faceQue': faceQue, 'allCount': allCount, 'allFace': allFace,
           'allOrigin': allOrigin,
           'aveOrigin': allOrigin / count, 'allReal': allReal, 'aveReal': allReal / count, 'bigger3Submit': ddlb3,
           'bigger3Face': ddlb3_face, 'smallerEqual3Submit': ddls3, 'smallerEqual3Face': ddls3_face}
    dic_Personal_type.append(dic)

    dic = {}
    dic = {'id': id, 'allQue': 200, 'queCount': count_All, 'faceQue': faceQue_All,
           'allCount': allCount_All, 'allFace': allFace_All, 'allOrigin': allOrigin_All,
           'aveOrigin': allOrigin_All / 200, 'allReal': allReal_All, 'aveReal': allReal_All / 200,
           'bigger3Submit': ddlb3_All, 'bigger3Face': ddlb3_face_All,
           'smallerEqual3Submit': ddls3_All, 'smallerEqual3Face': ddls3_face_All}
    dic_Personal_all.append(dic)
    export_excel(dic_Personal_type, personalType)
    export_excel(dic_Personal_all, personalAll)
