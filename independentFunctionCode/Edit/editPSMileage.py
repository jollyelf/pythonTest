# -*- coding: cp936 -*-
import arcpy
import re

# 设置工作空间
workSpace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"
arcpy.env.workspace=workSpace

def editPipesegmentMileage():
    '''
    定义一个自动编写管段里程的函数。
    ***针对管段表中同一管线的管段为首尾相连可以使用
    若管线中存在支线，且支线起点不在主线某一管段的末端时，本函数不适用***
    基本思路：
    编辑之前，管线的长度已经填写
    对于每一条管线其起点必然是编号为001的管段，将0赋值给001号管段的起点里程，那么他的终点里程即为0+长度
    然后找寻管线同一管线下起点坐标为上一条编辑管线终点坐标的管段，将终点里程赋值给找到的管段的起点里程，
    这条管段的终点里程即为起点里程+长度，依次循环，直到所有管段的起点和终点里程填写完成
    '''
    PLCodeList=[]
    PSDateList=[]
    PSEndDateList=[]
    #获取管段数据
    with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",\
                               ("PLCODE","CODE","SHAPE@","LENGTH","MSTART","MEND")) as cursor:
        for row in cursor:
            try:
                if row[1] is not None:
                    PLCodeList.append(row[0])
                    PSDateList.append([row[0],row[1],row[2],row[3],row[4],row[5]])
            except Exception,e:
                print e.message
                pass
            continue
    #填写里程
    for PL in set(PLCodeList):
        print PL
        finishPLList=[]
        noFinishPLList=[]
        for PS in PSDateList:
            if PL==PS[0]:
                if re.search(r'\d{6}GB\d{3}001',PS[1]):
                    PS[4]=0
                    PS[5]=PS[3]
                    finishPLList.append(PS)
                    PSEndDateList.append(PS)
                else:
                    noFinishPLList.append(PS)
        while len(noFinishPLList)!=0:
            for NFP in noFinishPLList:
                for FP in finishPLList:
                    if abs(NFP[2].firstPoint.X-FP[2].lastPoint.X)<1e-10 \
                       and abs(NFP[2].firstPoint.Y-FP[2].lastPoint.Y)<1e-10:
                        NFP[4]=FP[5]
                        NFP[5]=FP[5]+NFP[3]
                        finishPLList.append(NFP)
                        PSEndDateList.append(NFP)
                        noFinishPLList.remove(NFP)
                        
    with arcpy.da.UpdateCursor("T_PN_PIPESEGMENT_GEO",\
                               ("PLCODE","CODE","LENGTH","MSTART","MEND")) as Ucursor:
        for Urow in Ucursor:
            try:
                for PSED in PSEndDateList:
                    if Urow[1]==PSED[1]:
                        Urow[3]=PSED[4]
                        Urow[4]=PSED[5]
                        Ucursor.updateRow(Urow)
            except Exception,e:
                print e.message
                pass
            continue
editPipesegmentMileage()                
        
        
