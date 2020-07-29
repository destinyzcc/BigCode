import os

path = "D:\\Python project\\BigCode\\venv"
path1="D:\\Python project\\BigCode\\venv\\pow"
filelist = os.listdir(path1)
for file in filelist:
    name = file.split(",")
    if type(eval(name[2]))==int:
        olddir = os.path.join(path1,file)
        file = name[0] + "," + name[1] + "," + name[3][0:3] + "," + name[4].split("_")[1].split(".")[0] + "," + "a" + "," + name[2] + ".zip"
        newdir = os.path.join(path,file)
        os.rename(olddir, newdir)
