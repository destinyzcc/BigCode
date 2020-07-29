import os

path="D:\\Python project\\rename\\venv"
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
            if len(name)==4:
                file = name[0]+","+name[1]+","+ name[3].split("_")[0] + "," + name[3].split("_")[1].split(".")[0]+ ","+ "a" + "," + name[2] + ".zip"
            else:
                file = name[0] + "," + name[1] + "," + name[3][0:3] + "," + name[4].split("_")[1].split(".")[0] + "," + "a" + "," + name[2] + ".zip"
            newdir = os.path.join(path,file)
            os.rename(olddir,newdir)
        else:
            file = name[0]+","+name[1]+","+ name[3].split("_")[0] + "," + name[3].split("_")[1].split(".")[0]+ ","+ "c" + "," + name[2] + ".zip"
            newdir = os.path.join(path,file)
            os.rename(olddir, newdir)