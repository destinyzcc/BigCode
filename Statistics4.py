import xlwt
import openpyxl

from openpyxl import load_workbook
wb = load_workbook('D:/Python project/BigCode/singleQue.xlsx')
ws2 = wb['查找算法'] # 查找算法
ws3 = wb['排序算法'] # 排序算法
ws4 = wb['树结构'] # 树结构
ws5 = wb['数字操作']# 数字操作
ws6 = wb['数组']# 数组
ws7 = wb['图结构']# 图结构
ws8 = wb['线性表']# 线性表
ws9 = wb['字符串']# 字符串

ws_result = wb['字符串TOPSIS'] # result
ws = ws2 # 做另外题目类型的处理修改此行即刻
allData =[]
for i in ws.rows:
    newData=[]
    for j in i:
        newData.append(j.value)
    allData.append(newData)

UserId=[]

for i in range(1,len(allData)):
    if allData[i][0] not in UserId:
        UserId.append(allData[i][0])

result=[]

for i in range(0,len(UserId)):
    newResult=[UserId[i]]
    count1=0
    count2=0
    count3=0
    for j in range(0,len(allData)):
        if(allData[j][0]==UserId[i]):
            count1=count1+int(allData[j][3])
            count2 = count2 + int(allData[j][4])
            count3 = count3 + int(allData[j][8])
    newResult.append(count1)
    newResult.append(count2)
    newResult.append(count3)
    result.append(newResult)

ws_result.append(['用户Id','总提交次数','面向用例提交次数','总得分','查找算法'])
for i in range(0,len(result)):
    ws_result.append(result[i])
wb.save('D:/Python project/BigCode/singleQue.xlsx')
print('success')