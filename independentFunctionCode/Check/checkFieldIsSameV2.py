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



#定义一个用于检查设备设施属性是否与管段属性保持一致的函数
def fieldIsSameTest(feature):
    print featureClassAliasDictionary[feature]
    loopNumber=0
    #用列表分类要素类的检查数量
    testFieldTuple=("USEDDATE","DESIGNDEPNAME","CONSTRUNIT","SUPERVISORUNIT","TESTUNIT",\
                    "FDNAME","COLLECTDATE","COLLECTUNIT","INPUTDATETIME")#需要保持与管段一致的字段
    noCheckFeatureList=["T_PN_PIPESEGMENT_GEO","T_PN_STATION_GEO","T_PN_SOURCE_GEO"]#这些表格不用检查
    fieldDataErrorList=[]
    fieldNameList=[]
    fieldList=[]
    if feature not in noCheckFeatureList: 
        fieldList=arcpy.ListFields(feature)  #获取表中字段列表
        for FL in fieldList:                 #获取每一个表的所有字段名称
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
