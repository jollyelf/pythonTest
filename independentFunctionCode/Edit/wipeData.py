# -*- coding: cp936 -*-
import arcpy

#��ʩ�����ռ�
workSpace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"
arcpy.env.workspace=workSpace

def wipeData():
    #��ȡ���ߵ���Ҫ�ؼ��е�����Ҫ����
    featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")
    #��һ����յ��ֶ�Ԫ��
    notWipeTuple=("OBJECTID","Shape","Shape_Length")
    #��������ֶ�����
    for FC in featureClassList:
        if FC!="T_PN_PIPESEGMENT_GEO" and int(arcpy.GetCount_management(FC).getOutput(0))!=0:
            #��ȡ�����Ҫ�ص��ֶ���
            fieldList=[]
            fieldNameList=[]
            fieldList=arcpy.ListFields(FC)  
            for FL in fieldList: 
                fieldNameList.append(FL.name)
            #�������
            for FNL in fieldNameList:
                if FNL not in notWipeTuple:
                    with arcpy.da.UpdateCursor(FC,FNL) as cursor:
                        for row in cursor:
                            row[0]=None
                            cursor.updateRow(row)
wipeData()
        

