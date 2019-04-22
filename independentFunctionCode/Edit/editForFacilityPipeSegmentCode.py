# -*- coding: cp936 -*-
import arcpy

# 设置工作空间
workSpace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"
arcpy.env.workspace=workSpace

#获取管线地理要素集中的所有要素类
featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")

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

def PPCodeFill(feature):
    #下面这些要素不需要自动填充管段编码
    notFillPSCODEFeatureTuple=("T_PN_PIPESEGMENT_GEO","T_PN_STATION_GEO","T_PN_SOURCE_GEO",\
                               "T_LP_GASCROSS_GEO","T_LP_CASING_GEO")
    if feature not in notFillPSCODEFeatureTuple:
        try:
            arcpy.Delete_management("{}SpatialJoinClass".format(feature))
            if int(arcpy.GetCount_management(feature).getOutput(0))!=0:
                #添加一个字段用于复制要素的OBJECTID
                arcpy.AddField_management(feature,"OBJECTIDCOPY","TEXT")
                # 将目标表中的OBJECTID字段计算到设备编号中
                arcpy.CalculateField_management(feature,"OBJECTIDCOPY","!OBJECTID!","PYTHON")
                # 将要素与管段表进行空间连接，连接方式用最近
                arcpy.SpatialJoin_analysis(feature,"T_PN_PIPESEGMENT_GEO","{}SpatialJoinClass".format(feature),\
                                            "","","","CLOSEST","","")
                # 将要素表与空间连接后的中间标格按照通过OBJECTID进行属性连接，
                arcpy.JoinField_management(feature,"OBJECTIDCOPY","{}SpatialJoinClass".format(feature),"OBJECTIDCOPY","CODE_1")
                # 将属性连接后的字段计算成要素的管段编码
                arcpy.CalculateField_management(feature,"PSCODE","!CODE_1!","PYTHON")
                # 删除连接是多出的临时字段
                arcpy.DeleteField_management(feature,["CODE_1","OBJECTIDCOPY"])
                # 删除中间文件
                arcpy.Delete_management("{}SpatialJoinClass".format(feature))
        except Exception,e:
            print e.message
            pass
#for FC in featureClassList:
    #print featureClassAliasDictionary[FC]
PPCodeFill("T_PN_VALVE_GEO")


    
        
    
