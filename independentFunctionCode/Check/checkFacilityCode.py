# -*- coding: cp936 -*-
import arcpy
import re

# ���ù����ռ�
arcpy.env.workspace="C:\Users\lenovo\Desktop\PyTest\geodb.gdb"

#��ȡ���ߵ���Ҫ�ؼ��е�����Ҫ����

featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")

#����ÿһ��ͼ���Ŀ���ַ��ֵ�
featureClassCodeDictionary={
"T_BS_ELECMARK_GEO":"DBA",
"T_BS_GROUNDMARK_GEO":"BS",
"T_CP_ANODEBED_GEO":"YDA",
"T_CP_CPPOWER_GEO":"YBD",
"T_CP_DRNGDEVICE_GEO":"PLA",
"T_CP_FLEXANODE_GEO":"RYA",
"T_CP_RSANODE_GEO":"XYA",
"T_CP_SANODE_GEO":"XYA",
"T_CP_TESTTRUNK_GEO":"CSA",
"T_GE_BUILDING_GEO":"GEJ",
"T_GE_EMI_GEO":"GEG",
"T_GE_GEOHAZARD_GEO":"GEZ",
"T_GE_HLINE_GEO":"GEH",
"T_GE_HPOLYGON_GEO":"",
"T_GE_OTHPIPEPNT_GEO":"GES",
"T_GE_RAILWAY_GEO":"GET",
"T_GE_ROAD_GEO":"GED",
"T_GE_UNDROBSTACLE_GEO":"GEA",
"T_LP_ADDTLYR_GEO":"FSH",
"T_LP_APPENDANT_GEO":"",
"T_LP_CASING_GEO":"TGA",
"T_LP_CONDENSER_GEO":"FSJ",
"T_LP_GASCROSS_GEO":"A",
"T_LP_HYDRPROTECT_GEO":"HPA",
"T_LP_OPTICALHOLE_GEO":"GKA",
"T_LP_TUNNEL_GEO":"FSI",
"T_PN_BELLOW_GEO":"BWA",
"T_PN_BLOCK_GEO":"FDA",
"T_PN_ELBOW_GEO":"WGA",
"T_PN_IJOINT_GEO":"JTB",
"T_PN_PEPIPEWELD_GEO":"HKA",
"T_PN_PIPERISER_GEO":"GDA",
"T_PN_PRYCABINET_GEO":"QZ",
"T_PN_REDUCER_GEO":"YGA",
"T_PN_REGULATOR_GEO":"TY",
"T_PN_SEAMCUT_GEO":"HFA",
"T_PN_SOURCE_GEO":"Z",
"T_PN_SPE_GEO":"JTC",
"T_PN_STATION_GEO":"Z",
"T_PN_TAPPING_GEO":"KKA",
"T_PN_THREEORFOUR_GEO":"ST",
"T_PN_VALVE_GEO":"FM",
"T_PN_VALVEPIT_GEO":"FJ",
"T_PN_PIPESEGMENT_GEO":"GB"
}

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



#���ÿһ��Ҫ�ر����Ƿ񺬶�Ӧ�豸��ʩ��������
def facilityCodeTest(feature):
    #����һ�����ڵ�������Ҫ���б�
    checkAloneList=["T_PN_PIPESEGMENT_GEO","T_PN_SOURCE_GEO","T_PN_STATION_GEO",\
                "T_LP_GASCROSS_GEO","T_BS_GROUNDMARK_GEO","T_PN_THREEORFOUR_GEO"]
    codeList=[]
    if feature not in checkAloneList:
        with arcpy.da.SearchCursor(feature,("CODE","OBJECTID")) as cursor:
            for row in cursor:
                if row[0] is not None:
                    if len(row[0])!=20:
                        codeList.append([row[1],row[0]])
                    elif not re.search(r'\d{6}G[A-Z]\d{6}[A-Z]{3}\d{3}',row[0]):
                        codeList.append([row[1],row[0]])
                    elif(featureClassCodeDictionary[feature] not in row[0]):
                        codeList.append([row[1],row[0]])
    elif feature == "T_PN_PIPESEGMENT_GEO":
        with arcpy.da.SearchCursor(feature,("CODE","OBJECTID")) as cursor:
            for row in cursor:
                if row[0] is not None:
                    if (len(row[0])!=14):
                        codeList.append([row[1],row[0]])
                    elif not re.search(r'\d{6}G[A-Z]\d{6}',row[0]):
                        codeList.append([row[1],row[0]])
    elif feature =="T_PN_SOURCE_GEO":
        with arcpy.da.SearchCursor(feature,("CODE","OBJECTID")) as cursor:
            for row in cursor:
                if row[0] is not None:
                    if (len(row[0])!=11):
                        codeList.append([row[1],row[0]])
                    elif not re.search(r'\d{6}Z[A-Z]\d{3}',row[0]):
                        codeList.append([row[1],row[0]])
    elif feature =="T_PN_STATION_GEO":
        with arcpy.da.SearchCursor(feature,("CODE","OBJECTID")) as cursor:
            for row in cursor:
                if row[0] is not None:
                    if (len(row[0])!=11):
                        codeList.append([row[1],row[0]])
                    elif not re.search(r'\d{6}Z[A-Z]\d{3}',row[0]):
                        codeList.append([row[1],row[0]])                     
    elif feature == "T_LP_GASCROSS_GEO":
        with arcpy.da.SearchCursor(feature,("CODE","OBJECTID")) as cursor:
            for row in cursor:
                if row[0] is not None:
                    if (len(row[0])!=20):
                        codeList.append([row[1],row[0]])
                    elif not re.search(r'\d{6}G[A-Z]\d{6}[A-Z]{3}\d{3}',row[0]):
                        codeList.append([row[1],row[0]])
                    elif "PTA" not in row[0] and "ACA" not in row[0]:
                        codeList.append([row[1],row[0]])
    elif feature == "T_BS_GROUNDMARK_GEO":
        with arcpy.da.SearchCursor(feature,("CODE","OBJECTID")) as cursor:
            for row in cursor:
                if row[0] is not None:
                    if (len(row[0])!=20):
                        codeList.append([row[1],row[0]])
                    elif not re.search(r'\d{6}G[A-Z]\d{6}[A-Z]{3}\d{3}',row[0]):
                        codeList.append([row[1],row[0]])
                    elif "BS" not in row[0] and "MK" not in row[0] and "JSA" not in row[0]:
                        codeList.append([row[1],row[0]])
    elif feature == "T_PN_THREEORFOUR_GEO":
        with arcpy.da.SearchCursor(feature,("CODE","OBJECTID")) as cursor:
            for row in cursor:
                if row[0] is not None:
                    if (len(row[0])!=20):
                        codeList.append([row[1],row[0]])
                    elif not re.search(r'\d{6}G[A-Z]\d{6}[A-Z]{3}\d{3}',row[0]):
                        codeList.append([row[1],row[0]])
                    elif "STA" not in row[0] and "STB" not in row[0]:
                        codeList.append([row[1],row[0]])                  
    if(len(codeList)!=0):
        print featureClassAliasDictionary[feature],feature,"������ڴ��󣬴������Ϊ��"
        for cl in codeList:
            print cl[0],cl[1]



            
#���PIPEGEO���ݼ�������Ҫ����ı����Ƿ����
for fc in featureClassList:
    facilityCodeTest(fc)
                



















        
