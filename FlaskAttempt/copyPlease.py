import pandas as pd
from course import *
import random
import math

number_of_schedules = 3000
number_of_semesters = 6
number_of_semesters = int(number_of_semesters)
List_Of_Schedules = []
List_Of_Taken_Classes = []
List_Of_Picked_Classes = []
List_Of_Picked_Classes_Database = []
List_of_Tables = []


df = pd.read_excel(r'C:\Users\drags\OneDrive\Desktop\Programacion\Personal\ClassScheduling\ClassListExcel.xlsx')
df = df.fillna("empty")




def filterPandasDataFrame(df: pd.DataFrame, filterList: list):
    df = df[df['Course Name'].isin(filterList)]
    df.reset_index(drop=True, inplace=True)
    return df

def filterPandasOffset(df: pd.DataFrame, filterList: list):
    for i in range(len(df.index)):
        preReqStr = df.at[i, 'Prerequisites']
        for j in filterList:
            
            if j in preReqStr:
                preReqStr = preReqStr.replace(j, '')
            
        df.at[i,'Prerequisites'] = preReqStr

    return df

def make_Total_Classes_List(df:pd.DataFrame):
    return list(map(lambda x:Course(x[0], x[1], x[2], x[3]), df.values.tolist()))

def unPackClasses(classList: list):
    return list(map(lambda x: [x.name, x.credits], classList))

def unPackClassesInSchedule(classList: list):
    dummyList = []
    for schedule in classList:
        dummyList.append(list(map(lambda x: [x.name, x.credits], schedule)))
    return dummyList


def remove_common(a,b):
    for i in b:
        for j in a:
            if i == j:
                a.remove(i)
    return a

def remove_not_common(a,b):
    for i in b:
        for j in a:
            if i != j:
                a.remove(i)
    return a

def sameSchedule(sched_1, sched_2):
    sum = 0
    if len(sched_1) == len(sched_2):
        for j in range(len(sched_1)):
            if len(sched_1[j]) == len(sched_2[j]):
                for k in range(len(sched_1[j])):
                    if sched_1[j][k] == sched_2[j][k]:
                            sum += 1
                    else:
                        return False
            else:
                return False 
    else:
        return False

    return True


def satisfiesCoReq(sched_1):
    
    for semester in sched_1:
        for i in semester:
            if len(i.coReq) != 0:
                boolean_list_2 = []
                for j in semester:
                    if j.name in i.coReq:
                        boolean_list_2.append(True)
                    else:
                        boolean_list_2.append(False)
                if not any(boolean_list_2):
                    return False
    return True


def rangeCredits(sched_1):
    credit_list = []
    for i in sched_1:
        sum = 0
        for j in i:
            sum += j.credits
        credit_list.append(sum)

    return max(credit_list)-min(credit_list)


def emptyLists(schedule: list):
    for i in schedule:
        if i.preReq == ["empty"]:
            i.preReq = []
        if i.coReq == ["empty"]:
            i.coReq = []

    return schedule

def createPossibleSchedules():
    reducedDf = filterPandasDataFrame(df, List_Of_Picked_Classes)
    reducedDf = filterPandasOffset(reducedDf, List_Of_Taken_Classes)
    average_size = math.ceil(len(List_Of_Picked_Classes) / int(number_of_semesters))
    while len(List_Of_Schedules) < 100:
        Possible_Schedule = []
        Current_List = []
        Total_Classes = make_Total_Classes_List(reducedDf)
        emptyLists(Total_Classes)


        while len(Total_Classes) > 0 or len(Current_List) > 0:
            delete = []

            for i in Total_Classes:
                if len(i.preReq) == 0 or i.preReq == [] or i.preReq == "empty" or i.preReq == ['']:
                    Current_List.append(i)
                    
            if len(Current_List) >= average_size:
                delete = random.sample(Current_List, average_size)
            else:
                for i in Current_List:
                    delete.append(i)

            Total_Classes = remove_common(Total_Classes, Current_List)
            Current_List = remove_common(Current_List, delete)
            
            for i in Total_Classes:
                for j in delete:
                    if j.name in i.preReq:
                        i.preReq.remove(j.name)
                    
            Possible_Schedule.append(delete)

    

        if len(Possible_Schedule) == int(number_of_semesters):
            if satisfiesCoReq(Possible_Schedule):
                if len(List_Of_Schedules) == 0:
                    List_Of_Schedules.append(Possible_Schedule)
                else:
                    boolean_list = []
                    for schedule in List_Of_Schedules:
                        if not sameSchedule(Possible_Schedule, schedule):
                            boolean_list.append(False)
                        else:
                            boolean_list.append(True)
                        
                    if not any(boolean_list):
                        List_Of_Schedules.append(Possible_Schedule)



def minimizeSchedules():
    createPossibleSchedules()
    ranges = []
    minSchedules = []
    for schedule in List_Of_Schedules:
        ranges.append(rangeCredits(schedule))

    for schedule in List_Of_Schedules:
        if rangeCredits(schedule) == min(ranges):
            minSchedules.append(schedule)

    return minSchedules


def makeHTMLTable():
    minSchedules = minimizeSchedules()
    List_of_Tables.clear()
    
    for schedule in minSchedules:

        creditSumList = []
        for semester in schedule:
            creditSum = 0
            for course in semester:
                creditSum += course.credits
            creditSumList.append(creditSum)

        unpackedList = unPackClassesInSchedule(schedule)
        otherDf = pd.DataFrame(unpackedList)
        otherDf = otherDf.transpose()
        otherDf.columns = ['Semester %s' %i for i in range(1,len(otherDf.columns)+ 1)]
        otherDf.index = [i for i in range(1, len(otherDf.index)+1)]
        otherDf.loc[len(otherDf.index)+1] = creditSumList
        List_of_Tables.append(otherDf.to_html())

    return List_of_Tables

def makeBoxes():
    minschedules = minimizeSchedules()
    if len(minschedules) > 0:
        unpackedClasses = unPackClassesInSchedule(minschedules[0])
        return unpackedClasses
    
    return "!!!!!!!!!!!!!!!!!!!!"







