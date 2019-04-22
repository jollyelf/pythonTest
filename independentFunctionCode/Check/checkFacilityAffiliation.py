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

#����豸ʵʩ�Ƿ����丸�豸����ƥ��
def facilityAffiliationTest(feature):
    notCheckList=["T_PN_PIPESEGMENT_GEO","T_PN_SOURCE_GEO","T_PN_STATION_GEO"]
    FAErrorList=[]
    if feature not in notCheckList:
        print feature
        with arcpy.da.SearchCursor(feature,("CODE","PSCODE","OBJECTID")) as cursor:
            for row in cursor:
                #�жϸ�����Ϊ�գ��ӱ��벻Ϊ�յ����
                if((row[0] is not None) and (row[1] is None)):
                    FAErrorList.append([row[2],row[1],row[0]])
                #�ж��ӱ���Ϊ�գ������벻Ϊ�յ����
                if((row[0] is None) and (row[1] is not None)):
                    FAErrorList.append([row[2],row[1],row[0]])
                #�жϸ�������ӱ����Ϊ�գ�����ƥ������
                if ((row[0] is not None) and (row[1] is not None)) :
                    if row[1] not in row[0]:
                        FAErrorList.append([row[2],row[1],row[0]])
    if feature =="T_PN_PIPESEGMENT_GEO":
        with arcpy.da.SearchCursor(feature,("CODE","PLCODE","OBJECTID")) as cursor:
            for row in cursor:
                #�жϸ�����Ϊ�գ��ӱ��벻Ϊ�յ����
                if((row[0] is not None) and (row[1] is None)):
                    FAErrorList.append([row[2],row[1],row[0]])
                #�ж��ӱ���Ϊ�գ������벻Ϊ�յ����
                if((row[0] is None) and (row[1] is not None)):
                    FAErrorList.append([row[2],row[1],row[0]])
                #�жϸ�������ӱ����Ϊ�գ�����ƥ������
                if ((row[0] is not None) and (row[1] is not None)) :
                    if row[1] not in row[0]:
                        FAErrorList.append([row[2],row[1],row[0]])
        #�ж��Ƿ�����쳣���������λ�쳣
    if len(FAErrorList)!=0:
        print featureClassAliasDictionary[feature],feature,"���ڱ��벻ƥ�������������޸�"
        for FAE in FAErrorList:
            print FAE[0],FAE[1],FAE[2]

#�ж�Ҫ���б����Ƿ���ڸ�����ϵ,����оͽ��м�飬���û�оͲ����
for FC in featureClassList:
    facilityAffiliationTest(FC)

