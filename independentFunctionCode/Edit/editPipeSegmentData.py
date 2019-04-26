# -*- coding: cp936 -*-
import os
import arcpy

# 设置工作空间
workSpace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"
arcpy.env.workspace=workSpace


def editPipesegmentData():
    '''
    定义一个编辑管段表上一管段和下一管段的编码和名称的函数
    基本思路：
    首先获取管段表中输气管线和气源干线的管段数据
    然后比较管线的起止点，如果某一条管段的起点/终点与目标管段的终点/起点一致，则该管段为目标管段的下/上一管段
    最后将相应数据填写如管段表
    '''
    #获取管段数据
    PipeSegmentDataList=[]
    with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("CODE","NAME","SEGTYPE","SHAPE@")) as PPcursor:
        for PC in PPcursor:
            if PC[0] is not None and str(PC[0]).strip()!="":
                if PC[2]==1 or PC[2]==2:
                    PipeSegmentDataList.append([PC[0],PC[1],PC[2],PC[3]])

    #依据位置关系，填写管段相关数据
    with arcpy.da.UpdateCursor("T_PN_PIPESEGMENT_GEO",\
                               ("CODE","SEGTYPE","SHAPE@","PPSNAME","PPSCODE","NPSNAME","NPSCODE")) as cursor:
        for row in cursor:
            try:
                for PSD in PipeSegmentDataList:
                    if row[1] == 1 or row[1] == 2:
                        if abs(row[2].firstPoint.X-PSD[3].lastPoint.X)<1e-5 \
                           and abs(row[2].firstPoint.Y-PSD[3].lastPoint.Y)<1e-5:
                            row[3]=PSD[1]
                            row[4]=PSD[0]
                        if abs(row[2].lastPoint.X-PSD[3].firstPoint.X)<1e-5 \
                           and abs(row[2].lastPoint.Y-PSD[3].firstPoint.Y)<1e-5:
                            row[5]=PSD[1]
                            row[6]=PSD[0]
                        cursor.updateRow(row)
            except Exception,e:
                print e.message
                pass
            continue
editPipesegmentData()
                    
                    
                
