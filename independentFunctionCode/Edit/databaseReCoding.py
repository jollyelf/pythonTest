# -*- coding: cp936 -*-
import arcpy
import re

# ���ù����ռ�
arcpy.env.workspace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"

def databaseReCoding():
    '''
    ����ѭ��������Ҫ�����±��뺯����ʵ�ֶ��������ݿⲻͬҪ�ص����±���
    '''
    #����һ��Ҫ�����±���ĺ���
    def featureReCoding(feature):
        '''
        ���Ѿ��޸ı�������ֵ��Ҫ����������±��룬�紩��Խ���ѽ�PTA�޸�ΪACAʱ�����Ҫ�ص��ر���
        ����˼·��
        ���Ȼ�ȡ�����ǰ17λ
        �������Ϊ�ֵ�Ľ�ֵ�����ݱ����˼·�������±���
        '''
        notCodingTuple=("T_PN_SOURCE_GEO","T_PN_STATION_GEO","T_PN_PIPESEGMENT_GEO")
        tempDictionary={}
        if feature not in notCodingTuple:
            with arcpy.da.UpdateCursor(feature,("CODE")) as cursor:
                for row in cursor:
                    try:
                        tempValue=0
                        if row[0] is not None and len(row[0])==20 \
                           and re.search(r'\d{6}GB\d{6}[A-Z]{3}\d{3}',row[0]):
                                key=row[0][:17]
                                if tempDictionary.has_key(key):
                                    tempValue=tempDictionary[key]
                                    row[0]=key + str(tempValue+1).zfill(3)
                                    tempDictionary[key]=tempValue+1
                                    cursor.updateRow(row)
                                else:
                                    tempDictionary[key]=1
                                    row[0]=key + str(tempValue+1).zfill(3)
                                    cursor.updateRow(row)
                    except Exception, e:
                        print e.message
                        pass
                    continue
    #��ȡ���ߵ���Ҫ�ؼ��е�����Ҫ����
    featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")            
    #���ú����޸ĸ�Ҫ�ر���
    for FC in featureClassList:
        if int(arcpy.GetCount_management(FC).getOutput(0))!=0:
            featureReCoding(FC)
databaseReCoding()

