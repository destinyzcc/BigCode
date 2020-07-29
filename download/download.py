import json
import os
import urllib.request, urllib.parse

def down(url, filename):
    try:
        if not os.path.exists(filename):
            if not filename=="49823,树结构,16.67,1585452800166,奶牛舞蹈_1585452799217.zip" \
                    and not filename=="60623,图结构,30.0,1585587794583,新生舞会_1585587793615.zip" \
                    and not filename=="60810,图结构,0.0,1585578439814,新生舞会_1585578438642.zip"\
                    and not filename=="60810,数字操作,11.11,1585667692818,信息传递_1585667691815.zip" :
                urllib.request.urlretrieve(url, filename)
    except:
        down(url, filename)

def down2(url, filename):
    try:
        urllib.request.urlretrieve(url, filename)
    except:
        down2(url, filename)


f = open('test_data.json', encoding='utf-8')
res = f.read()
data = json.loads(res)
for d in iter(data):
    # print(d)
    print(data[str(d)]['cases'])
    cases = data[str(d)]['cases']
    for case in cases:
        print(case["case_id"], case["case_type"])
        filename = str(d) + "," + case["case_type"] + "," + str(case["final_score"]) + "," + urllib.parse.unquote(os.path.basename(case["case_zip"]))
        print(filename)
        u = str(case["case_zip"]).split("/")
        u[-1] = urllib.parse.quote(u[-1])
        url = ""
        for i in range(len(u)):
            if i == 1 | i == 0:
                continue
            elif i != len(u) - 1:
                url += u[i] + "/"
            else:
                url += u[i]
        print(url)
        if filename.find("*") != -1:
            index = filename.find("*")
            filename = filename[0:index] + "X" + filename[index+1:]
        #urllib.request.urlretrieve(url, filename)
        #down(url,filename)
        upload_records = case["upload_records"]
        for records in upload_records:
            print(records["upload_id"])
            print(records["code_url"])
            print(records["upload_time"])
            filename = str(d) + ","+ case["case_type"] + "," + str(records["score"]) + "," + str(records["upload_time"]) + "," + urllib.parse.unquote(os.path.basename(records["code_url"]))
            print(filename)
            if filename.find("*") != -1:
                index = filename.find("*")
                filename = filename[0:index] + "X" + filename[index + 1:]
            #urllib.request.urlretrieve(records["code_url"], filename)
            down(records["code_url"], filename)