# -*- coding: cp936 -*-
import arcpy

# 设置工作空间
arcpy.env.workspace="C:\Users\lenovo\Desktop\PyTest\geodb.gdb"

#获取管线地理要素集中的所有要素类

featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")

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

#检查设备实施是否与其父设备编码匹配
def facilityAffiliationTest(feature):
    notCheckList=["T_PN_PIPESEGMENT_GEO","T_PN_SOURCE_GEO","T_PN_STATION_GEO"]
    FAErrorList=[]
    if feature not in notCheckList:
        print feature
        with arcpy.da.SearchCursor(feature,("CODE","PSCODE","OBJECTID")) as cursor:
            for row in cursor:
                #判断父编码为空，子编码不为空的情况
                if((row[0] is not None) and (row[1] is None)):
                    FAErrorList.append([row[2],row[1],row[0]])
                #判断子编码为空，父编码不为空的情况
                if((row[0] is None) and (row[1] is not None)):
                    FAErrorList.append([row[2],row[1],row[0]])
                #判断父编码和子编码均为空，但不匹配的情况
                if ((row[0] is not None) and (row[1] is not None)) :
                    if row[1] not in row[0]:
                        FAErrorList.append([row[2],row[1],row[0]])
    if feature =="T_PN_PIPESEGMENT_GEO":
        with arcpy.da.SearchCursor(feature,("CODE","PLCODE","OBJECTID")) as cursor:
            for row in cursor:
                #判断父编码为空，子编码不为空的情况
                if((row[0] is not None) and (row[1] is None)):
                    FAErrorList.append([row[2],row[1],row[0]])
                #判断子编码为空，父编码不为空的情况
                if((row[0] is None) and (row[1] is not None)):
                    FAErrorList.append([row[2],row[1],row[0]])
                #判断父编码和子编码均为空，但不匹配的情况
                if ((row[0] is not None) and (row[1] is not None)) :
                    if row[1] not in row[0]:
                        FAErrorList.append([row[2],row[1],row[0]])
        #判断是否存在异常情况，并定位异常
    if len(FAErrorList)!=0:
        print featureClassAliasDictionary[feature],feature,"存在编码不匹配的情况，请检查修改"
        for FAE in FAErrorList:
            print FAE[0],FAE[1],FAE[2]

#判断要素列表中是否存在附属关系,如果有就进行检查，如果没有就不检查
for FC in featureClassList:
    facilityAffiliationTest(FC)

