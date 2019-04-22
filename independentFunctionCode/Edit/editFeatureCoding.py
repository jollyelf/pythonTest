# -*- coding: cp936 -*-
import arcpy
import re

# ���ù����ռ�
arcpy.env.workspace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"

#��ȡ���ߵ���Ҫ�ؼ��е�����Ҫ����

featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")


#����ÿһ��ͼ���Ŀ���ַ��ֵ�
featureClassCodeDictionary={"T_BS_ELECMARK_GEO":"DBA","T_BS_GROUNDMARK_GEO":"BSA",\
                            "T_CP_ANODEBED_GEO":"YDA","T_CP_CPPOWER_GEO":"YBD",\
                            "T_CP_DRNGDEVICE_GEO":"PLA","T_CP_FLEXANODE_GEO":"RYA",\
                            "T_CP_RSANODE_GEO":"XYA","T_CP_SANODE_GEO":"XYA",\
                            "T_CP_TESTTRUNK_GEO":"CSA","T_GE_BUILDING_GEO":"GEJ",\
                            "T_GE_EMI_GEO":"GEG","T_GE_GEOHAZARD_GEO":"GEZ",\
                            "T_GE_HLINE_GEO":"GEH","T_GE_HPOLYGON_GEO":"",\
                            "T_GE_OTHPIPEPNT_GEO":"GES","T_GE_RAILWAY_GEO":"GET",\
                            "T_GE_ROAD_GEO":"GED","T_GE_UNDROBSTACLE_GEO":"GEA",\
                            "T_LP_ADDTLYR_GEO":"FSH","T_LP_APPENDANT_GEO":"XXX",\
                            "T_LP_CASING_GEO":"TGA","T_LP_CONDENSER_GEO":"FSJ",\
                            "T_LP_GASCROSS_GEO":"PTA","T_LP_HYDRPROTECT_GEO":"HPA",\
                            "T_LP_OPTICALHOLE_GEO":"GKA","T_LP_TUNNEL_GEO":"FSI",\
                            "T_PN_BELLOW_GEO":"BWA","T_PN_BLOCK_GEO":"FDA",\
                            "T_PN_ELBOW_GEO":"WGA","T_PN_IJOINT_GEO":"JTB",\
                            "T_PN_PEPIPEWELD_GEO":"HKA","T_PN_PIPERISER_GEO":"GDA",\
                            "T_PN_PRYCABINET_GEO":"TYG","T_PN_REDUCER_GEO":"YGA",\
                            "T_PN_REGULATOR_GEO":"TYX","T_PN_SEAMCUT_GEO":"HFA",\
                            "T_PN_SOURCE_GEO":"Z","T_PN_SPE_GEO":"JTC","T_PN_STATION_GEO":"Z",\
                            "T_PN_TAPPING_GEO":"KKA","T_PN_THREEORFOUR_GEO":"STA",\
                            "T_PN_VALVE_GEO":"FMB","T_PN_VALVEPIT_GEO":"FJA",\
                            "T_PN_PIPESEGMENT_GEO":"GB"}

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

#����һ��Ҫ�ر���ĺ���
def featureCoding(feature):
    '''
    ���������ڶ��ѽ��йܶ�ƥ����豸��ʩ�����Զ����루���뱣֤���ظ����������տռ�˳�������򣩡�
    ÿһ��Ҫ�����ж�����һ��Ĭ�ϵ�������������(������Դ��վ���͹ܶβ����룬���������״ˮϵ����δ������XXX��ʾ)��
    T_PN_VALVEPIT_GEO 	    �������� 	FJA     T_PN_VALVE_GEO 	    ���� 	FMB
    T_PN_THREEORFOUR_GEO    ��ͨ��ͨ 	STA     T_PN_TAPPING_GEO    ���� 	KKA
    T_PN_STATION_GEO 	    ��վ 	Z       T_PN_SPE_GEO 	    ����ת����ͷ 	JTC
    T_PN_SOURCE_GEO 	    ��Դ 	Z       T_PN_SEAMCUT_GEO    ��������Ͳ��� HFA
    T_PN_REGULATOR_GEO     ��ѹ�� 	TYX     T_PN_REDUCER_GEO    �쾶�� 	YGA
    T_PN_PRYCABINET_GEO     ��װ�� 	TYG     T_PN_PIPESEGMENT_GEO�ܶ� 	GB
    T_PN_PIPERISER_GEO 	    ���� 	GDA     T_PN_PEPIPEWELD_GEO PE�ܺ��� 	HKA
    T_PN_IJOINT_GEO 	    ��Ե��ͷ 	JTB     T_PN_ELBOW_GEO 	    ��ͷ 	WGA
    T_PN_BLOCK_GEO 	    ����� 	FDA     T_PN_BELLOW_GEO     ���ƹ� 	BWA
    T_LP_TUNNEL_GEO 	    ��� 	FSI     T_LP_OPTICALHOLE_GEO�������ֿ� 	GKA
    T_LP_HYDRPROTECT_GEO    ˮ������ 	HPA     T_LP_GASCROSS_GEO   ����Խ 	PTA
    T_LP_CONDENSER_GEO 	    ��ˮ�� 	FSJ     T_LP_CASING_GEO     �׹� 	TGA
    T_LP_APPENDANT_GEO 	    ������ 	XXX     T_LP_ADDTLYR_GEO    ���ӱ����� 	FSH
    T_GE_UNDROBSTACLE_GEO   �����ϰ��� 	GEA     T_GE_ROAD_GEO 	    ��· 	GED
    T_GE_RAILWAY_GEO 	    ��· 	GET     T_GE_OTHPIPEPNT_GEO ����������λ�� GES
    T_GE_HPOLYGON_GEO 	    ��״ˮϵ 	XXX     T_GE_HLINE_GEO 	    ��״ˮϵ 	GEH
    T_GE_GEOHAZARD_GEO 	    �����ֺ� 	GEZ     T_GE_EMI_GEO 	    �������� 	GEG
    T_GE_BUILDING_GEO 	    ������ 	GEJ     T_CP_TESTTRUNK_GEO  ����׮ 	CSA
    T_CP_SANODE_GEO 	    �������� 	XYA     T_CP_RSANODE_GEO    ��״�������� 	XYA
    T_CP_FLEXANODE_GEO 	    �������� 	RYA     T_CP_DRNGDEVICE_GEO ����װ�� 	PLA
    T_CP_CPPOWER_GEO  ����վ��������Դ�� 	YBD     T_CP_ANODEBED_GEO   �����ش� 	YDA
    T_BS_GROUNDMARK_GEO     �����ʾ�� 	BSA     T_BS_ELECMARK_GEO   ���ӱ�ʶ�� 	DBA
    '''
    notCodingTuple=("T_PN_SOURCE_GEO","T_PN_STATION_GEO","T_PN_PIPESEGMENT_GEO")
    tempDictionary={}
    if feature not in notCodingTuple:
        with arcpy.da.UpdateCursor(feature,("PSCODE","CODE")) as cursor:
            for row in cursor:
                try:
                    tempValue=0
                    if row[0] is not None and len(row[0])==14 and re.search(r'\d{6}GB\d{6}',row[0]):
                            key=row[0]+featureClassCodeDictionary[feature]
                            if tempDictionary.has_key(key):
                                tempValue=tempDictionary[key]
                                row[1]=key + str(tempValue+1).zfill(3)
                                tempDictionary[key]=tempValue+1
                                cursor.updateRow(row)
                            else:
                                tempDictionary[key]=1
                                row[1]=key + str(tempValue+1).zfill(3)
                                cursor.updateRow(row)
                except Exception, e:
                    print e.message
                    pass
                continue
                    
#���ú�������Ҫ��������Ƿ��ظ�
for FC in featureClassList:
    print featureClassAliasDictionary[FC]
    featureCoding(FC)

