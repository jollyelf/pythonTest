# -*- coding: cp936 -*-
import os
import arcpy

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
'''
�쾶�� 		T_PN_REDUCER_GEO 	INDIAMETER 	OUTDIAMETER
����ת����ͷ 	T_PN_SPE_GEO 		INDIAMETER	OUTDIAMETER
���� 		T_PN_VALVE_GEO 		INDIAMETER 	OUTDIAMETER
��ͷ 		T_PN_ELBOW_GEO 	        INDIAMETER	OUTDIAMETER 
��Ե��ͷ 		T_PN_IJOINT_GEO 	INDIAMETER	OUTDIAMETER
���� 		T_PN_PIPERISER_GEO 	DIAMETER
���� 		T_PN_TAPPING_GEO 	MAINPIPEDIAMETER
��ͨ��ͨ		T_PN_THREEORFOUR_GEO 	MAINDIAMETER 		MINORDIAMETER
�ܶ� 		T_PN_PIPESEGMENT_GEO 	DIAMETER

'''
# ���ù����ռ�
arcpy.env.workspace="C:\Users\lenovo\Desktop\PyTest\geodb.gdb"

#��ȡ���ߵ���Ҫ�ؼ��е�����Ҫ����

featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")

def facilityDiameterTest(feature):
    #�趨�����DNֵ�б�
    DNValueList=[15,20,25,32,40,50,65,80,100,125,150,200,250,300,350,400,450,500,600]
    #���йܾ�ֵ�б�
    DiameterList=[14, 17, 17.2, 18, 20, 21.3, 22, 25, 26.9, 32, 33.7, 34, 38, 40, 42.4, \
                  45, 48, 48.4, 50, 57, 60, 60.3, 63, 73, 75, 76, 76.1, 88.9, 89, 90, \
                  108, 110, 114.3, 125, 133, 140, 159, 160, 168, 168.3, 180, 200, 219, \
                  219.1, 225, 250, 273, 280, 315, 323.9, 325, 355, 355.6, 377, 400, 406.4, \
                  426, 450, 457, 480, 500, 508, 530, 560, 610, 630, 710, 711, 720, 800, 813, \
                  820, 900, 914, 920, 1000, 1016, 1020, 1200]
    #�趨ֱ����DNֵ֮��Ľ�-ֵ��ϵ
    DiameterDNDic={"14.0":10,"17.0":10,"17.2":10,"18.0":15,"20.0":15,"21.3":15,"22.0":15,"25.0":20,"26.9":20,\
                   "32.0":25,"33.7":25,"34.0":25,"38.0":32,"40.0":32,"42":32,"42.4":32,"45.0":40,"48.0":40,\
                   "48.4":40,"50.0":40,"57.0":50,"60.0":50,"60.3":50,"63.0":50,"73.0":65,"75.0":65,"76.0":65,\
                   "76.1":65,"88.9":80,"89.0":80,"90.0":80,"108.0":100,"110.0":100,"114.0":100,"114.3":100,\
                   "125.0":125,"133.0":125,"140.0":125,"159.0":150,"160.0":150,"168.0":150,"168.3":150,\
                   "180.0":150,"200.0":200,"219.0":200,"219.1":200,"225.0":200,"250.0":250,"273.0":250,\
                   "280.0":250,"315.0":300,"323.9":300,"325.0":300,"355.0":350,"355.6":350,"377.0":350,\
                   "400.0":400,"406.4":400,"426.0":400,"450.0":450,"457.0":450,"480.0":450,"500.0":500,\
                   "508.0":500,"530.0":500,"560.0":500,"610.0":600,"630.0":600,"710.0":700,"711.0":700,\
                   "720.0":700,"800.0":800,"813.0":800,"820.0":800,"900.0":900,"914.0":900,"920.0":900,\
                   "1000.0":1000,"1016.0":1000,"1020.0":1000,"1200.0":1000}
    twoDiameterFeatureList=["T_PN_REDUCER_GEO","T_PN_SPE_GEO","T_PN_VALVE_GEO",\
                            "T_PN_ELBOW_GEO","T_PN_IJOINT_GEO"]

    DNErrorList=[]
    PipeSegmentDataList=[]
    with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("CODE","DIAMETER")) as PPcursor:
        for PC in PPcursor:
            if (PC[0] is not None) and (str(PC[0]).strip()!="") and \
               (PC[1] is not None) and (PC[1] in DiameterList):
                PipeSegmentDataList.append([PC[0],PC[1]])
    #�������Ϊ�쾶��/����ת����ͷ/����/��ͷ/��Ե��ͷ
    if feature in twoDiameterFeatureList:
        with arcpy.da.SearchCursor(feature,("OBJECTID","CODE","INDIAMETER","OUTDIAMETER","PSCODE"))\
             as REcursor:
            for RProw in REcursor:
                for PLS in PipeSegmentDataList:
                    if RProw[4]==PLS[0] and RProw[2]!=DiameterDNDic[str(round(PLS[1]))]:
                        DNErrorList.append([RProw[0],PLS[0],PLS[1],RProw[1],"INDIAMETER",RProw[2]])
                    if RProw[4]==PLS[0] and RProw[3] not in DNValueList:
                        DNErrorList.append([RProw[0],PLS[0],PLS[1],RProw[1],"OUTDIAMETER",RProw[3]])

    #�������Ϊ����
    if feature =="T_PN_PIPERISER_GEO":
        with arcpy.da.SearchCursor(feature,("OBJECTID","CODE","DIAMETER","PSCODE"))\
             as REcursor:
            for RProw in REcursor:
                for PLS in PipeSegmentDataList:
                    if RProw[3]==PLS[0] and RProw[2]!=DiameterDNDic[str(round(PLS[1]))]:
                        DNErrorList.append([RProw[0],PLS[0],PLS[1],RProw[1],"DIAMETER",RProw[2]])
    #�������Ϊ����
    if feature =="T_PN_TAPPING_GEO":
        with arcpy.da.SearchCursor(feature,("OBJECTID","CODE","MAINPIPEDIAMETER","PSCODE"))\
             as REcursor:
            for RProw in REcursor:
                for PLS in PipeSegmentDataList:
                    if RProw[3]==PLS[0] and RProw[2]!=DiameterDNDic[str(round(PLS[1]))]:
                        DNErrorList.append([RProw[0],PLS[0],PLS[1],RProw[1],"MAINPIPEDIAMETER",RProw[2]])

    #�������Ϊ��ͨ��ͨ
    if feature=="T_PN_THREEORFOUR_GEO":
        with arcpy.da.SearchCursor(feature,("OBJECTID","CODE","MAINDIAMETER","MINORDIAMETER","PSCODE"))\
             as REcursor:
            for RProw in REcursor:
                for PLS in PipeSegmentDataList:
                    if RProw[4]==PLS[0] and RProw[2]!=DiameterDNDic[str(round(PLS[1]))]:
                        DNErrorList.append([RProw[0],PLS[0],PLS[1],RProw[1],"MAINDIAMETER",RProw[2]])
                    if RProw[4]==PLS[0] and RProw[3] is not None and RProw[3] not in DNValueList:
                        DNErrorList.append([RProw[0],PLS[0],PLS[1],RProw[1],"MINORDIAMETER",RProw[3]])
                        
    if len(DNErrorList)!=0:
        print featureClassAliasDictionary[feature]+"("+str(feature)+")"+"���ڹܾ���д�쳣�����\n"
        for DNEL in DNErrorList:
            print DNEL[0],DNEL[1],DNEL[2],DNEL[3],DNEL[4],DNEL[5]

for fc in featureClassList:
    facilityDiameterTest(fc)
                    

                
            












