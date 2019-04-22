# -*- coding: cp936 -*-
import arcpy
import re

# ���ù����ռ�
workSpace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"
arcpy.env.workspace=workSpace

#��ȡ���ߵ���Ҫ�ؼ��е�����Ҫ����
featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")

#����һ��Ҫ���ļ����ͱ�Ƶ��ֵ�
featureClassAliasDictionary={
"T_BS_ELECMARK_GEO":"���ӱ�ʶ��","T_BS_GROUNDMARK_GEO":"�����ʾ��","T_CP_ANODEBED_GEO":"�����ش�",\
"T_CP_CPPOWER_GEO":"����վ��������Դ��","T_CP_DRNGDEVICE_GEO":"����װ��","T_CP_FLEXANODE_GEO":"��������",\
"T_CP_RSANODE_GEO":"��״��������","T_CP_SANODE_GEO":"��������","T_CP_TESTTRUNK_GEO":"����׮",\
"T_GE_BUILDING_GEO":"������","T_GE_EMI_GEO":"��������","T_GE_GEOHAZARD_GEO":"�����ֺ�","T_GE_HLINE_GEO":"��״ˮϵ",\
"T_GE_HPOLYGON_GEO":"��״ˮϵ","T_GE_OTHPIPEPNT_GEO":"����������λ��","T_GE_RAILWAY_GEO":"��·","T_GE_ROAD_GEO":"��·",\
"T_GE_UNDROBSTACLE_GEO":"�����ϰ���","T_LP_ADDTLYR_GEO":"���ӱ�����","T_LP_APPENDANT_GEO":"������",\
"T_LP_CASING_GEO":"�׹�","T_LP_CONDENSER_GEO":"��ˮ��","T_LP_GASCROSS_GEO":"����Խ","T_LP_HYDRPROTECT_GEO":"ˮ������",\
"T_LP_OPTICALHOLE_GEO":"�������ֿ�","T_LP_TUNNEL_GEO":"���","T_PN_BELLOW_GEO":"���ƹ�","T_PN_BLOCK_GEO":"�����",\
"T_PN_ELBOW_GEO":"��ͷ","T_PN_IJOINT_GEO":"��Ե��ͷ","T_PN_PEPIPEWELD_GEO":"PE�ܺ���","T_PN_PIPERISER_GEO":"����",\
"T_PN_PRYCABINET_GEO":"��װ��","T_PN_REDUCER_GEO":"�쾶��","T_PN_REGULATOR_GEO":"��ѹ��",\
"T_PN_SEAMCUT_GEO":"��������Ͳ���","T_PN_SOURCE_GEO":"��Դ","T_PN_SPE_GEO":"����ת����ͷ","T_PN_STATION_GEO":"��վ",\
"T_PN_TAPPING_GEO":"����","T_PN_THREEORFOUR_GEO":"��ͨ��ͨ","T_PN_VALVE_GEO":"����","T_PN_VALVEPIT_GEO":"��������",
"T_PN_PIPESEGMENT_GEO":"�ܶ�"
}
def coordinateFill(feature):
    '''
    ���������ڶ�Ҫ�ص�����ֵ������д��
    �ڹܶα�����д��ɲ���ȷ������£���д��Ҫ�ص�����ֵ��
    ��дҪ������ֵ֮ǰ����ȷ����������ϵΪ���2000����ϵ;
    
    ���ڵ�״Ҫ����д��XY;
    ������״Ҫ����д����ֹ���XY����д֮ǰһ��ȷ�����͵ķ�����ȷ;
    ����վ������Դ���ܶβ�������XY���ꣻ
    ���ڵ������ܵ�����ַ�ֺ��͵������ţ�����Ϊ��״Ҫ�أ����ֶ���Ϊ��״���ͣ������㣻
    
    '''
    notFillTuple=("T_PN_PIPESEGMENT_GEO","T_PN_SOURCE_GEO","T_PN_STATION_GEO",\
                  "T_GE_OTHPIPEPNT_GEO","T_GE_EMI_GEO","T_GE_GEOHAZARD_GEO")
    if feature not in notFillTuple:
        if arcpy.Describe(feature).spatialReference.name=="GCS_China_Geodetic_Coordinate_System_2000":
            if arcpy.Describe(feature).shapeType=="Point":
                with arcpy.da.UpdateCursor(feature,("PSCODE","X","Y","SHAPE@X","SHAPE@Y")) \
                     as cursor:
                    for row in cursor:
                        try:
                           if row[0] is not None and len(row[0])==14 and\
                              re.search(r'\d{6}GB\d{6}',row[0]):
                               row[1]=row[3]
                               row[2]=row[4]
                               cursor.updateRow(row)
                        except Exception, e:
                            print e.message
                            pass
                        continue
            elif arcpy.Describe(feature).shapeType=="Polyline":
                with arcpy.da.UpdateCursor(feature,("PSCODE","XSTART","YSTART","XEND","YEND",\
                                                    "SHAPE@")) as cursor:
                    for row in cursor:
                        try:
                           if row[0] is not None and len(row[0])==14 and\
                              re.search(r'\d{6}GB\d{6}',row[0]):
                               row[1]=row[5].firstPoint.X
                               row[2]=row[5].firstPoint.Y
                               row[3]=row[5].lastPoint.X
                               row[4]=row[5].lastPoint.Y
                               cursor.updateRow(row)
                        except Exception, e:
                            print e.message
                            pass
                        continue 
        else:
            print arcpy.Describe(feature).spatialReference.name

#���ú�����дҪ��XY����
for FC in featureClassList:
   print featureClassAliasDictionary[FC]
   coordinateFill(FC)
        
    
