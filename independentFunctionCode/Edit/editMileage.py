# -*- coding: cp936 -*-
import arcpy

# ���ù����ռ�
workSpace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"
arcpy.env.workspace=workSpace


def editMileage():
    '''
    ����һ�������豸��ʩ����̵ĺ�����
    ����֮ǰȷ���ܶα��������̺��յ�����Ѿ���ȷ��д��
    
    ����˼·��
    �������ô���·�����߹����������й��ߵ�·��
    Ȼ���豸��ʩ��·��ͨ����λҪ�ع��߼��������̣��������̺��յ���̣�
    ������ֵд��ÿһ��Ҫ�صĶ�Ӧ����ֶ���

    ��ͨ�������������Ҫ���飨�ر��Ƕ��ڹܶα���Žϴ����ֵΪ0�Ļ��߹ܶα���ֵ��С�����ֵ�ϴ�������Ҫ�ص��飩��
    '''
    #���ùܶ������̺��յ�����ֶδ������ߵ�·��
    arcpy.CreateRoutes_lr("T_PN_PIPESEGMENT_GEO","PLCODE","routes", "TWO_FIELDS", "MSTART","MEND")

    #��ȡ���ߵ���Ҫ�ؼ��е�����Ҫ����
    featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")
    for FC in featureClassList:
        try:
            #�����в�Ϊ�յĵ�״Ҫ�ؽ�����̼���
            if arcpy.Describe(FC).shapeType=="Point" and\
               int(arcpy.GetCount_management(FC).getOutput(0))!=0:
                
                #��ȡ����Ҫ�ص������ֶ�����
                fieldList=[]
                fieldNameList=[]
                fieldList=arcpy.ListFields(FC)  #��ȡ�����ֶ��б�
                for FL in fieldList: #��ȡÿһ����������ֶ�����
                    fieldNameList.append(FL.name)
                if "MILEAGE" in fieldNameList:
                    print FC
                    #���һ���ֶ����ڸ���Ҫ�ص�OBJECTID
                    arcpy.AddField_management(FC,"OBJECTIDCOPY","TEXT")
                    # ��Ŀ����е�OBJECTID�ֶμ��㵽�豸�����
                    arcpy.CalculateField_management(FC,"OBJECTIDCOPY","!OBJECTID!","PYTHON")
                    #����Ŀ��Ҫ�ر���������
                    arcpy.LocateFeaturesAlongRoutes_lr(FC,"routes","PLCODE","0.01 Kilometers","out")
                    #�����������ӽ��������������ݵı���Ŀ��Ҫ�ر�����
                    arcpy.JoinField_management(FC,"OBJECTIDCOPY","out","OBJECTIDCOPY","MEAS")
                    # ���������Ӻ���ֶμ����Ҫ�صĹܶα���
                    arcpy.CalculateField_management(FC,"MILEAGE","!MEAS!","PYTHON")
                    # ɾ������ʱ�������ʱ�ֶ�
                    arcpy.DeleteField_management(FC,["MEAS","OBJECTIDCOPY"])
                    # ɾ���м��ļ�
                    arcpy.Delete_management("out")     
        except Exception,e:
            print e.message
            pass
        continue
    #ɾ�������Ĺ켣ͼ��
    arcpy.Delete_management("routes")
editMileage()
