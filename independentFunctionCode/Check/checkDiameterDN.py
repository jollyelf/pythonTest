# -*- coding: cp936 -*-
import os
import arcpy

#定义一个要素文件名和别称的字典
featureClassAliasDictionary={
"T_BS_ELECMARK_GEO":"电子标识器",
"T_BS_GROUNDMARK_GEO":"地面标示物",
"T_CP_ANODEBED_GEO":"阳极地床",
"T_CP_CPPOWER_GEO":"阴保站（阴保电源）",
"T_CP_DRNGDEVICE_GEO":"排流装置",
"T_CP_FLEXANODE_GEO":"柔性阳极",
"T_CP_RSANODE_GEO":"带状牺牲阳极",
"T_CP_SANODE_GEO":"牺牲阳极",
"T_CP_TESTTRUNK_GEO":"测试桩",
"T_GE_BUILDING_GEO":"建筑物",
"T_GE_EMI_GEO":"电流干扰",
"T_GE_GEOHAZARD_GEO":"地质灾害",
"T_GE_HLINE_GEO":"线状水系",
"T_GE_HPOLYGON_GEO":"面状水系",
"T_GE_OTHPIPEPNT_GEO":"第三方管线位置",
"T_GE_RAILWAY_GEO":"铁路",
"T_GE_ROAD_GEO":"公路",
"T_GE_UNDROBSTACLE_GEO":"地下障碍物",
"T_LP_ADDTLYR_GEO":"附加保护层",
"T_LP_APPENDANT_GEO":"附属物",
"T_LP_CASING_GEO":"套管",
"T_LP_CONDENSER_GEO":"凝水缸",
"T_LP_GASCROSS_GEO":"穿跨越",
"T_LP_HYDRPROTECT_GEO":"水工保护",
"T_LP_OPTICALHOLE_GEO":"光缆人手孔",
"T_LP_TUNNEL_GEO":"隧道",
"T_PN_BELLOW_GEO":"波纹管",
"T_PN_BLOCK_GEO":"封堵物",
"T_PN_ELBOW_GEO":"弯头",
"T_PN_IJOINT_GEO":"绝缘接头",
"T_PN_PEPIPEWELD_GEO":"PE管焊接",
"T_PN_PIPERISER_GEO":"立管",
"T_PN_PRYCABINET_GEO":"撬装柜",
"T_PN_REDUCER_GEO":"异径管",
"T_PN_REGULATOR_GEO":"调压箱",
"T_PN_SEAMCUT_GEO":"金属焊缝和补口",
"T_PN_SOURCE_GEO":"气源",
"T_PN_SPE_GEO":"钢塑转换接头",
"T_PN_STATION_GEO":"场站",
"T_PN_TAPPING_GEO":"开孔",
"T_PN_THREEORFOUR_GEO":"三通四通",
"T_PN_VALVE_GEO":"阀门",
"T_PN_VALVEPIT_GEO":"阀井阀室",
"T_PN_PIPESEGMENT_GEO":"管段"
}
'''
异径管 		T_PN_REDUCER_GEO 	INDIAMETER 	OUTDIAMETER
钢塑转换接头 	T_PN_SPE_GEO 		INDIAMETER	OUTDIAMETER
阀门 		T_PN_VALVE_GEO 		INDIAMETER 	OUTDIAMETER
弯头 		T_PN_ELBOW_GEO 	        INDIAMETER	OUTDIAMETER 
绝缘接头 		T_PN_IJOINT_GEO 	INDIAMETER	OUTDIAMETER
立管 		T_PN_PIPERISER_GEO 	DIAMETER
开孔 		T_PN_TAPPING_GEO 	MAINPIPEDIAMETER
三通四通		T_PN_THREEORFOUR_GEO 	MAINDIAMETER 		MINORDIAMETER
管段 		T_PN_PIPESEGMENT_GEO 	DIAMETER

'''
# 设置工作空间
arcpy.env.workspace="C:\Users\lenovo\Desktop\PyTest\geodb.gdb"

#获取管线地理要素集中的所有要素类

featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")

def facilityDiameterTest(feature):
    #设定允许的DN值列表
    DNValueList=[15,20,25,32,40,50,65,80,100,125,150,200,250,300,350,400,450,500,600]
    #所有管径值列表
    DiameterList=[14, 17, 17.2, 18, 20, 21.3, 22, 25, 26.9, 32, 33.7, 34, 38, 40, 42.4, \
                  45, 48, 48.4, 50, 57, 60, 60.3, 63, 73, 75, 76, 76.1, 88.9, 89, 90, \
                  108, 110, 114.3, 125, 133, 140, 159, 160, 168, 168.3, 180, 200, 219, \
                  219.1, 225, 250, 273, 280, 315, 323.9, 325, 355, 355.6, 377, 400, 406.4, \
                  426, 450, 457, 480, 500, 508, 530, 560, 610, 630, 710, 711, 720, 800, 813, \
                  820, 900, 914, 920, 1000, 1016, 1020, 1200]
    #设定直径与DN值之间的健-值关系
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
    #如果输入为异径管/刚塑转换接头/阀门/弯头/绝缘接头
    if feature in twoDiameterFeatureList:
        with arcpy.da.SearchCursor(feature,("OBJECTID","CODE","INDIAMETER","OUTDIAMETER","PSCODE"))\
             as REcursor:
            for RProw in REcursor:
                for PLS in PipeSegmentDataList:
                    if RProw[4]==PLS[0] and RProw[2]!=DiameterDNDic[str(round(PLS[1]))]:
                        DNErrorList.append([RProw[0],PLS[0],PLS[1],RProw[1],"INDIAMETER",RProw[2]])
                    if RProw[4]==PLS[0] and RProw[3] not in DNValueList:
                        DNErrorList.append([RProw[0],PLS[0],PLS[1],RProw[1],"OUTDIAMETER",RProw[3]])

    #如果输入为立管
    if feature =="T_PN_PIPERISER_GEO":
        with arcpy.da.SearchCursor(feature,("OBJECTID","CODE","DIAMETER","PSCODE"))\
             as REcursor:
            for RProw in REcursor:
                for PLS in PipeSegmentDataList:
                    if RProw[3]==PLS[0] and RProw[2]!=DiameterDNDic[str(round(PLS[1]))]:
                        DNErrorList.append([RProw[0],PLS[0],PLS[1],RProw[1],"DIAMETER",RProw[2]])
    #如果输入为开孔
    if feature =="T_PN_TAPPING_GEO":
        with arcpy.da.SearchCursor(feature,("OBJECTID","CODE","MAINPIPEDIAMETER","PSCODE"))\
             as REcursor:
            for RProw in REcursor:
                for PLS in PipeSegmentDataList:
                    if RProw[3]==PLS[0] and RProw[2]!=DiameterDNDic[str(round(PLS[1]))]:
                        DNErrorList.append([RProw[0],PLS[0],PLS[1],RProw[1],"MAINPIPEDIAMETER",RProw[2]])

    #如果输入为三通四通
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
        print featureClassAliasDictionary[feature]+"("+str(feature)+")"+"存在管径填写异常情况：\n"
        for DNEL in DNErrorList:
            print DNEL[0],DNEL[1],DNEL[2],DNEL[3],DNEL[4],DNEL[5]

for fc in featureClassList:
    facilityDiameterTest(fc)
                    

                
            












