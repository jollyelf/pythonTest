# -*- coding: cp936 -*-
import arcpy

# ���ù����ռ�
arcpy.env.workspace="C:\Users\lenovo\Desktop\PyTest\geodb.gdb"

#��ȡ���ߵ���Ҫ�ؼ��е�����Ҫ����

featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")

#����һ��Ҫ���ļ����ͱ�Ƶ��ֵ�
featureClassAliasDictionary={
"T_BS_ELECMARK_GEO":"���ӱ�ʶ��",
"T_BS_GROUNDMARK_GEO":"�����ʾ��",
"T_CP_ANODEBED_GEO":"�����ش�",
"T_CP_CPPOWER_GEO":"����վ��������Դ��",
"T_CP_DRNGDEVICE_GEO":"����װ��",
"T_CP_FLEXANODE_GEO":"��������",
"T_CP_RSANODE_GEO":"��״��������",
"T_CP_SANODE_GEO":"��������",
"T_CP_TESTTRUNK_GEO":"����׮",
"T_GE_BUILDING_GEO":"������",
"T_GE_EMI_GEO":"��������",
"T_GE_GEOHAZARD_GEO":"�����ֺ�",
"T_GE_HLINE_GEO":"��״ˮϵ",
"T_GE_HPOLYGON_GEO":"��״ˮϵ",
"T_GE_OTHPIPEPNT_GEO":"����������λ��",
"T_GE_RAILWAY_GEO":"��·",
"T_GE_ROAD_GEO":"��·",
"T_GE_UNDROBSTACLE_GEO":"�����ϰ���",
"T_LP_ADDTLYR_GEO":"���ӱ�����",
"T_LP_APPENDANT_GEO":"������",
"T_LP_CASING_GEO":"�׹�",
"T_LP_CONDENSER_GEO":"��ˮ��",
"T_LP_GASCROSS_GEO":"����Խ",
"T_LP_HYDRPROTECT_GEO":"ˮ������",
"T_LP_OPTICALHOLE_GEO":"�������ֿ�",
"T_LP_TUNNEL_GEO":"���",
"T_PN_BELLOW_GEO":"���ƹ�",
"T_PN_BLOCK_GEO":"�����",
"T_PN_ELBOW_GEO":"��ͷ",
"T_PN_IJOINT_GEO":"��Ե��ͷ",
"T_PN_PEPIPEWELD_GEO":"PE�ܺ���",
"T_PN_PIPERISER_GEO":"����",
"T_PN_PRYCABINET_GEO":"��װ��",
"T_PN_REDUCER_GEO":"�쾶��",
"T_PN_REGULATOR_GEO":"��ѹ��",
"T_PN_SEAMCUT_GEO":"��������Ͳ���",
"T_PN_SOURCE_GEO":"��Դ",
"T_PN_SPE_GEO":"����ת����ͷ",
"T_PN_STATION_GEO":"��վ",
"T_PN_TAPPING_GEO":"����",
"T_PN_THREEORFOUR_GEO":"��ͨ��ͨ",
"T_PN_VALVE_GEO":"����",
"T_PN_VALVEPIT_GEO":"��������",
"T_PN_PIPESEGMENT_GEO":"�ܶ�"
}



#����һ�����ڼ���豸��ʩ�����Ƿ���ܶ����Ա���һ�µĺ���
def fieldIsSameTest(feature):
    print featureClassAliasDictionary[feature]
    loopNumber=0
    #���б����Ҫ����ļ������
    testFieldTuple=("USEDDATE","DESIGNDEPNAME","CONSTRUNIT","SUPERVISORUNIT","TESTUNIT",\
                    "FDNAME","COLLECTDATE","COLLECTUNIT","INPUTDATETIME")#��Ҫ������ܶ�һ�µ��ֶ�
    noCheckFeatureList=["T_PN_PIPESEGMENT_GEO","T_PN_STATION_GEO","T_PN_SOURCE_GEO"]#��Щ����ü��
    fieldDataErrorList=[]
    fieldNameList=[]
    fieldList=[]
    if feature not in noCheckFeatureList: 
        fieldList=arcpy.ListFields(feature)  #��ȡ�����ֶ��б�
        for FL in fieldList:                 #��ȡÿһ����������ֶ�����
            fieldNameList.append(FL.name)
        for TFT in testFieldTuple:
            if TFT in fieldNameList:
                PPDataList=[]
                with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("CODE",TFT)) as PPcursor:
                    for Prow in PPcursor:
                        PPDataList.append([Prow[0],Prow[1]])
                with arcpy.da.SearchCursor(feature,("OBJECTID","CODE","PSCODE",TFT)) as cursor:
                    for row in cursor:
                        for PDL in PPDataList:
                            loopNumber+=1
                            if row[2]==PDL[0] and row[3]!=PDL[1]:
                                    fieldDataErrorList.append([row[0],TFT,row[1],row[3],\
                                                               PDL[0],PDL[1]])
    if len(fieldDataErrorList)!=0:
        for FDEL in fieldDataErrorList:
            print FDEL[0],FDEL[1],FDEL[2],FDEL[3],FDEL[4],FDEL[5]
    print loopNumber
                                
                            
    
for fc in featureClassList:
    fieldIsSameTest(fc)
