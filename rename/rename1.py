import os

path = "D:\\Python project\\BigCode\\venv"
path1="D:\\Python project\\BigCode\\venv\\代码"
path2 = "D:\\Python project\\BigCode\\venv\\题目"
str1 = "a"  #题目
str2 = "c"  #代码
filelist = os.listdir(path1)
for file in filelist:
    name = file.split(",")
    olddir = os.path.join(path1,file)
    file = name[0] + "," + name[1] + "," + name[4].split("_")[0] + "," + name[4].split("_")[1].split(".")[0] + "," + "c" + "," + name[3] + ".zip"
    newdir = os.path.join(path,file)
    os.rename(olddir, newdir)

filelist = os.listdir(path2)
for file in filelist:
    name = file.split(",")
    olddir = os.path.join(path2, file)
    try:
        file = name[0] + "," + name[1] + "," + name[4].split("_")[0] + "," + name[4].split("_")[1].split(".")[0] + "," + "a" + "," + name[3] + ".zip"
        newdir = os.path.join(path, file)
        os.rename(olddir, newdir)
    except:
        print("error")