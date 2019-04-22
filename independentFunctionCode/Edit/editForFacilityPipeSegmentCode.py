# -*- coding: cp936 -*-
import arcpy

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

def PPCodeFill(feature):
    #������ЩҪ�ز���Ҫ�Զ����ܶα���
    notFillPSCODEFeatureTuple=("T_PN_PIPESEGMENT_GEO","T_PN_STATION_GEO","T_PN_SOURCE_GEO",\
                               "T_LP_GASCROSS_GEO","T_LP_CASING_GEO")
    if feature not in notFillPSCODEFeatureTuple:
        try:
            arcpy.Delete_management("{}SpatialJoinClass".format(feature))
            if int(arcpy.GetCount_management(feature).getOutput(0))!=0:
                #���һ���ֶ����ڸ���Ҫ�ص�OBJECTID
                arcpy.AddField_management(feature,"OBJECTIDCOPY","TEXT")
                # ��Ŀ����е�OBJECTID�ֶμ��㵽�豸�����
                arcpy.CalculateField_management(feature,"OBJECTIDCOPY","!OBJECTID!","PYTHON")
                # ��Ҫ����ܶα���пռ����ӣ����ӷ�ʽ�����
                arcpy.SpatialJoin_analysis(feature,"T_PN_PIPESEGMENT_GEO","{}SpatialJoinClass".format(feature),\
                                            "","","","CLOSEST","","")
                # ��Ҫ�ر���ռ����Ӻ���м�����ͨ��OBJECTID�����������ӣ�
                arcpy.JoinField_management(feature,"OBJECTIDCOPY","{}SpatialJoinClass".format(feature),"OBJECTIDCOPY","CODE_1")
                # ���������Ӻ���ֶμ����Ҫ�صĹܶα���
                arcpy.CalculateField_management(feature,"PSCODE","!CODE_1!","PYTHON")
                # ɾ�������Ƕ������ʱ�ֶ�
                arcpy.DeleteField_management(feature,["CODE_1","OBJECTIDCOPY"])
                # ɾ���м��ļ�
                arcpy.Delete_management("{}SpatialJoinClass".format(feature))
        except Exception,e:
            print e.message
            pass
#for FC in featureClassList:
    #print featureClassAliasDictionary[FC]
PPCodeFill("T_PN_VALVE_GEO")


    
        
    
