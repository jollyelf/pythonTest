# -*- coding: cp936 -*-
import arcpy

#设施工作空间
workSpace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"
arcpy.env.workspace=workSpace

def wipeData():
    #获取管线地理要素集中的所有要素类
    featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")
    #第一不清空的字段元组
    notWipeTuple=("OBJECTID","Shape","Shape_Length")
    #清空数据字段数据
    for FC in featureClassList:
        if FC!="T_PN_PIPESEGMENT_GEO" and int(arcpy.GetCount_management(FC).getOutput(0))!=0:
            #获取表格中要素的字段名
            fieldList=[]
            fieldNameList=[]
            fieldList=arcpy.ListFields(FC)  
            for FL in fieldList: 
                fieldNameList.append(FL.name)
            #清空数据
            for FNL in fieldNameList:
                if FNL not in notWipeTuple:
                    with arcpy.da.UpdateCursor(FC,FNL) as cursor:
                        for row in cursor:
                            row[0]=None
                            cursor.updateRow(row)
wipeData()
        

