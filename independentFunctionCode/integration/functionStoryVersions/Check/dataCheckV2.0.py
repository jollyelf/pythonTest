# -*- coding: cp936 -*-
import os
import arcpy
import dataCheckFunctionToFile as Function


def main(workSpace):
    """
    ������������ݿ��д��ڵĴ��󣬲�����д���ļ������������¼���������쳣�����
    1���ܶ������е��߼�������ʵ��������>���������������ѹ��>���ѹ����ѹ���ȼ������ѹ��������
        �������ߺ���Դ�����������ιܶ���Ϣδ��д���ܾ��ͱں���쳣��ͳһ�����¹ܶ������ظ��Լ�PE�����˷�����ʽ.
    2��������������д����ظ������.
    3���豸��ʩ��������ܶα��벻ƥ�䲻ƥ������.
    4�������������.
    5���豸��ʩ��Ͷ�����ڡ���Ƶ�λ��ʩ����λ������λ����ⵥλ������ͼֽ����š��ɼ����ڡ��ɼ���λ���Ӧ�ܶβ�ͬ�����.
    6���豸��ֱ���쳣ֵ��������ܶβ�ƥ�估���ǲ��õ�DNֵ�����.
    7������д����ļ�¼�б���Ļ�����Ϣδ��д�����.
    """
    # ���ù����ռ�
    arcpy.env.workspace=workSpace
    #��ȡ���ߵ���Ҫ�ؼ��е�����Ҫ����
    featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")
    #����һ��Ҫ���ļ����ͱ�Ƶ��ֵ�
    featureClassAliasDictionary={"T_BS_ELECMARK_GEO":"���ӱ�ʶ��","T_BS_GROUNDMARK_GEO":"�����ʾ��",\
                                 "T_CP_ANODEBED_GEO":"�����ش�","T_CP_CPPOWER_GEO":"����վ��������Դ��",\
                                 "T_CP_DRNGDEVICE_GEO":"����װ��","T_CP_FLEXANODE_GEO":"��������",\
                                 "T_CP_RSANODE_GEO":"��״��������","T_CP_SANODE_GEO":"��������",\
                                 "T_CP_TESTTRUNK_GEO":"����׮","T_GE_BUILDING_GEO":"������",\
                                 "T_GE_EMI_GEO":"��������","T_GE_GEOHAZARD_GEO":"�����ֺ�",\
                                 "T_GE_HLINE_GEO":"��״ˮϵ","T_GE_HPOLYGON_GEO":"��״ˮϵ",\
                                 "T_GE_OTHPIPEPNT_GEO":"����������λ��","T_GE_RAILWAY_GEO":"��·",\
                                 "T_GE_ROAD_GEO":"��·","T_GE_UNDROBSTACLE_GEO":"�����ϰ���",\
                                 "T_LP_ADDTLYR_GEO":"���ӱ�����","T_LP_APPENDANT_GEO":"������",\
                                 "T_LP_CASING_GEO":"�׹�","T_LP_CONDENSER_GEO":"��ˮ��",\
                                 "T_LP_GASCROSS_GEO":"����Խ","T_LP_HYDRPROTECT_GEO":"ˮ������",\
                                 "T_LP_OPTICALHOLE_GEO":"�������ֿ�","T_LP_TUNNEL_GEO":"���",\
                                 "T_PN_BELLOW_GEO":"���ƹ�","T_PN_BLOCK_GEO":"�����","T_PN_ELBOW_GEO":"��ͷ",\
                                 "T_PN_IJOINT_GEO":"��Ե��ͷ","T_PN_PEPIPEWELD_GEO":"PE�ܺ���",\
                                 "T_PN_PIPERISER_GEO":"����","T_PN_PRYCABINET_GEO":"��װ��",\
                                 "T_PN_REDUCER_GEO":"�쾶��","T_PN_REGULATOR_GEO":"��ѹ��",\
                                 "T_PN_SEAMCUT_GEO":"��������Ͳ���","T_PN_SOURCE_GEO":"��Դ",\
                                 "T_PN_SPE_GEO":"����ת����ͷ","T_PN_STATION_GEO":"��վ","T_PN_TAPPING_GEO":"����",\
                                 "T_PN_THREEORFOUR_GEO":"��ͨ��ͨ","T_PN_VALVE_GEO":"����",\
                                 "T_PN_VALVEPIT_GEO":"��������","T_PN_PIPESEGMENT_GEO":"�ܶ�"}
    #����ÿһ��ͼ���Ŀ���ַ��ֵ�
    featureClassCodeDictionary={"T_BS_ELECMARK_GEO":"DBA","T_BS_GROUNDMARK_GEO":"BS","T_CP_ANODEBED_GEO":"YDA",\
                                "T_CP_CPPOWER_GEO":"YBD","T_CP_DRNGDEVICE_GEO":"PLA","T_CP_FLEXANODE_GEO":"RYA",\
                                "T_CP_RSANODE_GEO":"XYA","T_CP_SANODE_GEO":"XYA","T_CP_TESTTRUNK_GEO":"CSA",\
                                "T_GE_BUILDING_GEO":"GEJ","T_GE_EMI_GEO":"GEG","T_GE_GEOHAZARD_GEO":"GEZ",\
                                "T_GE_HLINE_GEO":"GEH","T_GE_HPOLYGON_GEO":"","T_GE_OTHPIPEPNT_GEO":"GES",\
                                "T_GE_RAILWAY_GEO":"GET","T_GE_ROAD_GEO":"GED","T_GE_UNDROBSTACLE_GEO":"GEA",\
                                "T_LP_ADDTLYR_GEO":"FSH","T_LP_APPENDANT_GEO":"","T_LP_CASING_GEO":"TGA",\
                                "T_LP_CONDENSER_GEO":"FSJ","T_LP_GASCROSS_GEO":"A","T_LP_HYDRPROTECT_GEO":"HPA",\
                                "T_LP_OPTICALHOLE_GEO":"GKA","T_LP_TUNNEL_GEO":"FSI","T_PN_BELLOW_GEO":"BWA",\
                                "T_PN_BLOCK_GEO":"FDA","T_PN_ELBOW_GEO":"WGA","T_PN_IJOINT_GEO":"JTB",\
                                "T_PN_PEPIPEWELD_GEO":"HKA","T_PN_PIPERISER_GEO":"GDA","T_PN_PRYCABINET_GEO":"QZ",\
                                "T_PN_REDUCER_GEO":"YGA","T_PN_REGULATOR_GEO":"TY","T_PN_SEAMCUT_GEO":"HFA",\
                                "T_PN_SOURCE_GEO":"Z","T_PN_SPE_GEO":"JTC","T_PN_STATION_GEO":"Z",\
                                "T_PN_TAPPING_GEO":"KKA","T_PN_THREEORFOUR_GEO":"ST","T_PN_VALVE_GEO":"FM",\
                                "T_PN_VALVEPIT_GEO":"FJ","T_PN_PIPESEGMENT_GEO":"GB"}
    for FC in featureClassList:
        Function.pipeSegmentLogicTest(FC)    #���ܶ������еĸ����߼�����
        Function.fieldIsNonetest(FC)         #�������ֶ��Ƿ�Ϊ��
        Function.codeRepetitionTest(FC)      #�������Ƿ��ظ�
        Function.facilityAffiliationTest(FC) #����豸��ʩ��ܶα����Ƿ�ƥ��
        Function.facilityCodeTest(FC)        #����豸��ʩ�ı����Ƿ���ϱ������
        Function.fieldIsSameTest(FC)         #����豸��ʩ��ĳЩ�ֶ��Ƿ���ܶ���ͬ
        Function.facilityDiameterTest(FC)    #����豸��ʩ��ֱ���Ƿ���ܶ�ƥ��     
    print "Check finished"
    
# arcpy.GetParameter(0)
if __name__ == '__main__':
    #�ڴ˴�����Ҫ�������ݿ�Ŀ¼����
    workSpace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"
    main(workSpace)

    

    
