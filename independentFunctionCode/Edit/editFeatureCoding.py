# -*- coding: cp936 -*-
import arcpy
import re

# 设置工作空间
arcpy.env.workspace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"

#获取管线地理要素集中的所有要素类

featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")


#罗列每一个图层的目标字符字典
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

#定义一个要素文件名和别称的字典
featureClassAliasDictionary={
"T_BS_ELECMARK_GEO":"电子标识器","T_BS_GROUNDMARK_GEO":"地面标示物","T_CP_ANODEBED_GEO":"阳极地床",\
"T_CP_CPPOWER_GEO":"阴保站（阴保电源）","T_CP_DRNGDEVICE_GEO":"排流装置","T_CP_FLEXANODE_GEO":"柔性阳极",\
"T_CP_RSANODE_GEO":"带状牺牲阳极","T_CP_SANODE_GEO":"牺牲阳极","T_CP_TESTTRUNK_GEO":"测试桩",\
"T_GE_BUILDING_GEO":"建筑物","T_GE_EMI_GEO":"电流干扰","T_GE_GEOHAZARD_GEO":"地质灾害","T_GE_HLINE_GEO":"线状水系",\
"T_GE_HPOLYGON_GEO":"面状水系","T_GE_OTHPIPEPNT_GEO":"第三方管线位置","T_GE_RAILWAY_GEO":"铁路","T_GE_ROAD_GEO":"公路",\
"T_GE_UNDROBSTACLE_GEO":"地下障碍物","T_LP_ADDTLYR_GEO":"附加保护层","T_LP_APPENDANT_GEO":"附属物",\
"T_LP_CASING_GEO":"套管","T_LP_CONDENSER_GEO":"凝水缸","T_LP_GASCROSS_GEO":"穿跨越","T_LP_HYDRPROTECT_GEO":"水工保护",\
"T_LP_OPTICALHOLE_GEO":"光缆人手孔","T_LP_TUNNEL_GEO":"隧道","T_PN_BELLOW_GEO":"波纹管","T_PN_BLOCK_GEO":"封堵物",\
"T_PN_ELBOW_GEO":"弯头","T_PN_IJOINT_GEO":"绝缘接头","T_PN_PEPIPEWELD_GEO":"PE管焊接","T_PN_PIPERISER_GEO":"立管",\
"T_PN_PRYCABINET_GEO":"撬装柜","T_PN_REDUCER_GEO":"异径管","T_PN_REGULATOR_GEO":"调压箱",\
"T_PN_SEAMCUT_GEO":"金属焊缝和补口","T_PN_SOURCE_GEO":"气源","T_PN_SPE_GEO":"钢塑转换接头","T_PN_STATION_GEO":"场站",\
"T_PN_TAPPING_GEO":"开孔","T_PN_THREEORFOUR_GEO":"三通四通","T_PN_VALVE_GEO":"阀门","T_PN_VALVEPIT_GEO":"阀井阀室",
"T_PN_PIPESEGMENT_GEO":"管段"
}

#定义一个要素编码的函数
def featureCoding(feature):
    '''
    本函数用于对已进行管段匹配的设备设施进行自动编码（编码保证不重复，但不按照空间顺序来排序）。
    每一个要素类中都给定一个默认的特征编码如下(其中气源、站场和管段不编码，附属物和面状水系编码未定，用XXX表示)：
    T_PN_VALVEPIT_GEO 	    阀井阀室 	FJA     T_PN_VALVE_GEO 	    阀门 	FMB
    T_PN_THREEORFOUR_GEO    三通四通 	STA     T_PN_TAPPING_GEO    开孔 	KKA
    T_PN_STATION_GEO 	    场站 	Z       T_PN_SPE_GEO 	    钢塑转换接头 	JTC
    T_PN_SOURCE_GEO 	    气源 	Z       T_PN_SEAMCUT_GEO    金属焊缝和补口 HFA
    T_PN_REGULATOR_GEO     调压箱 	TYX     T_PN_REDUCER_GEO    异径管 	YGA
    T_PN_PRYCABINET_GEO     撬装柜 	TYG     T_PN_PIPESEGMENT_GEO管段 	GB
    T_PN_PIPERISER_GEO 	    立管 	GDA     T_PN_PEPIPEWELD_GEO PE管焊接 	HKA
    T_PN_IJOINT_GEO 	    绝缘接头 	JTB     T_PN_ELBOW_GEO 	    弯头 	WGA
    T_PN_BLOCK_GEO 	    封堵物 	FDA     T_PN_BELLOW_GEO     波纹管 	BWA
    T_LP_TUNNEL_GEO 	    隧道 	FSI     T_LP_OPTICALHOLE_GEO光缆人手孔 	GKA
    T_LP_HYDRPROTECT_GEO    水工保护 	HPA     T_LP_GASCROSS_GEO   穿跨越 	PTA
    T_LP_CONDENSER_GEO 	    凝水缸 	FSJ     T_LP_CASING_GEO     套管 	TGA
    T_LP_APPENDANT_GEO 	    附属物 	XXX     T_LP_ADDTLYR_GEO    附加保护层 	FSH
    T_GE_UNDROBSTACLE_GEO   地下障碍物 	GEA     T_GE_ROAD_GEO 	    公路 	GED
    T_GE_RAILWAY_GEO 	    铁路 	GET     T_GE_OTHPIPEPNT_GEO 第三方管线位置 GES
    T_GE_HPOLYGON_GEO 	    面状水系 	XXX     T_GE_HLINE_GEO 	    线状水系 	GEH
    T_GE_GEOHAZARD_GEO 	    地质灾害 	GEZ     T_GE_EMI_GEO 	    电流干扰 	GEG
    T_GE_BUILDING_GEO 	    建筑物 	GEJ     T_CP_TESTTRUNK_GEO  测试桩 	CSA
    T_CP_SANODE_GEO 	    牺牲阳极 	XYA     T_CP_RSANODE_GEO    带状牺牲阳极 	XYA
    T_CP_FLEXANODE_GEO 	    柔性阳极 	RYA     T_CP_DRNGDEVICE_GEO 排流装置 	PLA
    T_CP_CPPOWER_GEO  阴保站（阴保电源） 	YBD     T_CP_ANODEBED_GEO   阳极地床 	YDA
    T_BS_GROUNDMARK_GEO     地面标示物 	BSA     T_BS_ELECMARK_GEO   电子标识器 	DBA
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
                    
#调用函数检查各要素类编码是否重复
for FC in featureClassList:
    print featureClassAliasDictionary[FC]
    featureCoding(FC)

