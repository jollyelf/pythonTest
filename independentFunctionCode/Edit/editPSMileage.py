# -*- coding: cp936 -*-
import arcpy
import re

# ���ù����ռ�
workSpace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"
arcpy.env.workspace=workSpace

def editPipesegmentMileage():
    '''
    ����һ���Զ���д�ܶ���̵ĺ�����
    ***��Թܶα���ͬһ���ߵĹܶ�Ϊ��β��������ʹ��
    �������д���֧�ߣ���֧����㲻������ĳһ�ܶε�ĩ��ʱ��������������***
    ����˼·��
    �༭֮ǰ�����ߵĳ����Ѿ���д
    ����ÿһ������������Ȼ�Ǳ��Ϊ001�ĹܶΣ���0��ֵ��001�Źܶε������̣���ô�����յ���̼�Ϊ0+����
    Ȼ����Ѱ����ͬһ�������������Ϊ��һ���༭�����յ�����ĹܶΣ����յ���̸�ֵ���ҵ��Ĺܶε������̣�
    �����ܶε��յ���̼�Ϊ������+���ȣ�����ѭ����ֱ�����йܶε������յ������д���
    '''
    PLCodeList=[]
    PSDateList=[]
    PSEndDateList=[]
    #��ȡ�ܶ�����
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
    #��д���
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
        
        
