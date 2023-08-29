import pandas as pd
from course import *

df = pd.read_excel(r'C:\Users\drags\OneDrive\Desktop\Programacion\Personal\ClassScheduling\ClassListExcel.xlsx')
df = df.fillna("empty")
List_Of_Taken_Classes = ['MATH586', 'MATH572']
string = '<table border="1" class="dataframe"> <thead> <tr style="text-align: right;"> <th></th> <th>Semester 1</th> <th>Semester 2</th> <th>Semester 3</th> <th>Semester 4</th> <th>Semester 5</th> <th>Semester 6</th> </tr> </thead> <tbody> <tr> <th>1</th> <td>CS121</td> <td>MATH586</td> <td>CH237</td> <td>BSC472</td> <td>CS300</td> <td>CS470</td> </tr> <tr> <th>2</th> <td>ECE380</td> <td>BSC315</td> <td>MATH587</td> <td>CS200</td> <td>CS301</td> <td>CS496</td> </tr> <tr> <th>3</th> <td>BSC300</td> <td>MATH572</td> <td>BSC399</td> <td>CS201</td> <td>MATH566</td> <td>CS499</td> </tr> <tr> <th>4</th> <td>BSC120</td> <td>BSC385</td> <td>CH232</td> <td>MATH565</td> <td>MATH598</td> <td>CS495</td> </tr> <tr> <th>5</th> <td>ENGR103</td> <td>CS101</td> <td>ECE383</td> <td>MATH597</td> <td>MATH599</td> <td>CS497</td> </tr> <tr> <th>6</th> <td>CH231</td> <td>BSC310</td> <td>MATH570</td> <td>None</td> <td>None</td> <td>CS403</td> </tr> <tr> <th>7</th> <td>MATH355</td> <td>UH200</td> <td>MATH585</td> <td>None</td> <td>None</td> <td>CS498</td> </tr> <tr> <th>8</th> <td>21</td> <td>22</td> <td>22</td> <td>18</td> <td>15</td> <td>21</td> </tr> </tbody> </table>'
cool = pd.read_html(string)
cool = cool[0]

cool = cool.iloc[ :-1, 1: ]
print(cool)
mylist = [list(cool[col]) for col in cool.columns]
print(mylist)
#print(df)

print('-----------------')


# def filterPandasOffset(df: pd.DataFrame, filterList: list):
#     df = df[~df['Course Name'].isin(filterList)]
#     df.reset_index(drop=True, inplace=True)
#     for i in range(len(df.index)):
#         preReqStr = df.at[i, 'Prerequisites']
#         for j in filterList:
            
#             if j in preReqStr:
#                 preReqStr = preReqStr.replace(j, '')
            
#         df.at[i,'Prerequisites'] = preReqStr

#     return df


# reducedDf = filterPandasOffset(df, List_Of_Taken_Classes)





def unPackClasses(classList: list):
    return list(map(lambda x: [x.name, x.credits, x.preReq, x.coReq], classList))


def make_Total_Classes_List(df:pd.DataFrame):
    return list(map(lambda x:Course(x[0], x[1], x[2], x[3]), df.values.tolist()))

TotalClasses = make_Total_Classes_List(df)
TotalClasses = unPackClasses(TotalClasses)
newDf = pd.DataFrame(TotalClasses)
newDf.columns = ['Course Name', 'Credit Hours', 'Prerequisites', 'Corequisites']

#print(newDf)


def emptyLists(list: list):
    for i in list:
        if i.preReq == ["empty"]:
            i.preReq = []
        if i.header == ["empty"]:
            i.header = []
        if i.coReq == ["empty"]:
            i.coReq = []

    return list

def filterPandasDataFrame(df: pd.DataFrame, filterList: list):
    return df[df['Course Name'].isin(filterList)]












