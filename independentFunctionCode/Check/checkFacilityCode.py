# -*- coding: cp936 -*-
import arcpy
import re

# 设置工作空间
arcpy.env.workspace="C:\Users\lenovo\Desktop\PyTest\geodb.gdb"

#获取管线地理要素集中的所有要素类

featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")

#罗列每一个图层的目标字符字典
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



#检查每一个要素编码是否含对应设备设施特征编码
def facilityCodeTest(feature):
    #定义一个用于单独检查的要素列表
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
        print featureClassAliasDictionary[feature],feature,"编码存在错误，错误编码为："
        for cl in codeList:
            print cl[0],cl[1]



            
#检查PIPEGEO数据集中所有要素类的编码是否出错
for fc in featureClassList:
    facilityCodeTest(fc)
                



















        
