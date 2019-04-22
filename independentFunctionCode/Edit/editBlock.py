# -*- coding: cp936 -*-
import os
import arcpy

# 设置工作空间
workSpace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"
arcpy.env.workspace=workSpace

def editBLOCK():
    #获取管段数据
    PipeSegmentDataList=[]
    with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("CODE","REFOBJEND","OFFSETEND","XEND","YEND","ZEND")) as PPcursor:
        for PC in PPcursor:
            if PC[0] is not None and str(PC[0]).strip()!="":
                PipeSegmentDataList.append([PC[0],PC[1],PC[2],PC[3],PC[4],PC[5]])
    #更新三通数据
    with arcpy.da.UpdateCursor("T_PN_BLOCK_GEO",("PSCODE","REFOBJ","OFFSET","X","Y","Z")) as cursor:
        for row in cursor:
            try:
                for PSD in PipeSegmentDataList:
                    if row[0]==PSD[0]:
                        row[1]=PSD[1]
                        row[2]=PSD[2]
                        row[3]=PSD[3]
                        row[4]=PSD[4]
                        row[5]=PSD[5]
                        cursor.updateRow(row)
            except Exception,e:
                print e.message
                pass
            continue
editBLOCK()
