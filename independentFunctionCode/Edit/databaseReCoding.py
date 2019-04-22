# -*- coding: cp936 -*-
import arcpy
import re

# 设置工作空间
arcpy.env.workspace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"

def databaseReCoding():
    '''
    利用循环，调用要素重新编码函数，实现对整个数据库不同要素的重新编码
    '''
    #定义一个要素重新编码的函数
    def featureReCoding(feature):
        '''
        对已经修改编码特征值的要素类进行重新编码，如穿跨越中已将PTA修改为ACA时，完成要素的重编码
        基本思路：
        首先获取编码的前17位
        其后将其作为字典的健值，依据编码的思路进行重新编码
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
    #获取管线地理要素集中的所有要素类
    featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")            
    #调用函数修改各要素编码
    for FC in featureClassList:
        if int(arcpy.GetCount_management(FC).getOutput(0))!=0:
            featureReCoding(FC)
databaseReCoding()

