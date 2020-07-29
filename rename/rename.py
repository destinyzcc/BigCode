import os

path="D:\\Python project\\BigCode\\venv"
str1 = "题目"
str2 = "代码"
filelist = os.listdir(path)
for file in filelist:
    if os.path.isdir(os.path.join(path,file)):
        continue
    filetype = os.path.splitext(file)[1]
    if filetype == ".zip":
        name = file.split(",")
        score = eval(name[2])
        olddir = os.path.join(path,file)
        if type(score)==int:
            file = name[0]+","+name[1]+","+"题目包"+","+name[2]+","+name[3]
            newdir = os.path.join(path,str1,file)
            os.rename(olddir,newdir)
        else:
            file = name[0] + "," + name[1] + "," + "代码包" + "," + name[2] + "," + name[3]
            newdir = os.path.join(path, str2, file)
            os.rename(olddir, newdir)