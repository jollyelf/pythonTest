# -*- coding: cp936 -*-
import os
import arcpy

# ���ù����ռ�
workSpace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"
arcpy.env.workspace=workSpace


def editPipesegmentData():
    '''
    ����һ���༭�ܶα���һ�ܶκ���һ�ܶεı�������Ƶĺ���
    ����˼·��
    ���Ȼ�ȡ�ܶα����������ߺ���Դ���ߵĹܶ�����
    Ȼ��ȽϹ��ߵ���ֹ�㣬���ĳһ���ܶε����/�յ���Ŀ��ܶε��յ�/���һ�£���ùܶ�ΪĿ��ܶε���/��һ�ܶ�
    �����Ӧ������д��ܶα�
    '''
    #��ȡ�ܶ�����
    PipeSegmentDataList=[]
    with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("CODE","NAME","SEGTYPE","SHAPE@")) as PPcursor:
        for PC in PPcursor:
            if PC[0] is not None and str(PC[0]).strip()!="":
                if PC[2]==1 or PC[2]==2:
                    PipeSegmentDataList.append([PC[0],PC[1],PC[2],PC[3]])

    #����λ�ù�ϵ����д�ܶ��������
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
                    
                    
                
