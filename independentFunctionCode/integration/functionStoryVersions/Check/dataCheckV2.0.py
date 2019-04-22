# -*- coding: cp936 -*-
import os
import arcpy
import dataCheckFunctionToFile as Function


def main(workSpace):
    """
    本函数检查数据库中存在的错误，并将其写成文件。包含了以下几个方面的异常情况：
    1、管段数据中的逻辑错误，如实际输送量>设计输送量、运行压力>设计压力、压力等级与设计压力不符、
        输气干线和气源干线中上下游管段信息未填写、管径和壁厚的异常、统一管线下管段名称重复以及PE管填了防腐方式.
    2、所有已填编码中存在重复的情况.
    3、设备设施编码与其管段编码不匹配不匹配的情况.
    4、编码错误的情况.
    5、设备设施的投用日期、设计单位、施工单位、监理单位、检测单位，竣工图纸及编号、采集日期、采集单位与对应管段不同的情况.
    6、设备的直径异常值，包括与管段不匹配及不是采用的DN值的情况.
    7、已填写编码的记录中必填的基础信息未填写的情况.
    """
    # 设置工作空间
    arcpy.env.workspace=workSpace
    #获取管线地理要素集中的所有要素类
    featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")
    #定义一个要素文件名和别称的字典
    featureClassAliasDictionary={"T_BS_ELECMARK_GEO":"电子标识器","T_BS_GROUNDMARK_GEO":"地面标示物",\
                                 "T_CP_ANODEBED_GEO":"阳极地床","T_CP_CPPOWER_GEO":"阴保站（阴保电源）",\
                                 "T_CP_DRNGDEVICE_GEO":"排流装置","T_CP_FLEXANODE_GEO":"柔性阳极",\
                                 "T_CP_RSANODE_GEO":"带状牺牲阳极","T_CP_SANODE_GEO":"牺牲阳极",\
                                 "T_CP_TESTTRUNK_GEO":"测试桩","T_GE_BUILDING_GEO":"建筑物",\
                                 "T_GE_EMI_GEO":"电流干扰","T_GE_GEOHAZARD_GEO":"地质灾害",\
                                 "T_GE_HLINE_GEO":"线状水系","T_GE_HPOLYGON_GEO":"面状水系",\
                                 "T_GE_OTHPIPEPNT_GEO":"第三方管线位置","T_GE_RAILWAY_GEO":"铁路",\
                                 "T_GE_ROAD_GEO":"公路","T_GE_UNDROBSTACLE_GEO":"地下障碍物",\
                                 "T_LP_ADDTLYR_GEO":"附加保护层","T_LP_APPENDANT_GEO":"附属物",\
                                 "T_LP_CASING_GEO":"套管","T_LP_CONDENSER_GEO":"凝水缸",\
                                 "T_LP_GASCROSS_GEO":"穿跨越","T_LP_HYDRPROTECT_GEO":"水工保护",\
                                 "T_LP_OPTICALHOLE_GEO":"光缆人手孔","T_LP_TUNNEL_GEO":"隧道",\
                                 "T_PN_BELLOW_GEO":"波纹管","T_PN_BLOCK_GEO":"封堵物","T_PN_ELBOW_GEO":"弯头",\
                                 "T_PN_IJOINT_GEO":"绝缘接头","T_PN_PEPIPEWELD_GEO":"PE管焊接",\
                                 "T_PN_PIPERISER_GEO":"立管","T_PN_PRYCABINET_GEO":"撬装柜",\
                                 "T_PN_REDUCER_GEO":"异径管","T_PN_REGULATOR_GEO":"调压箱",\
                                 "T_PN_SEAMCUT_GEO":"金属焊缝和补口","T_PN_SOURCE_GEO":"气源",\
                                 "T_PN_SPE_GEO":"钢塑转换接头","T_PN_STATION_GEO":"场站","T_PN_TAPPING_GEO":"开孔",\
                                 "T_PN_THREEORFOUR_GEO":"三通四通","T_PN_VALVE_GEO":"阀门",\
                                 "T_PN_VALVEPIT_GEO":"阀井阀室","T_PN_PIPESEGMENT_GEO":"管段"}
    #罗列每一个图层的目标字符字典
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
        Function.pipeSegmentLogicTest(FC)    #检查管段数据中的各种逻辑错误
        Function.fieldIsNonetest(FC)         #检查必填字段是否为空
        Function.codeRepetitionTest(FC)      #检查编码是否重复
        Function.facilityAffiliationTest(FC) #检查设备设施与管段编码是否匹配
        Function.facilityCodeTest(FC)        #检查设备设施的编码是否符合编码规则
        Function.fieldIsSameTest(FC)         #检查设备设施的某些字段是否与管段相同
        Function.facilityDiameterTest(FC)    #检查设备设施的直径是否与管段匹配     
    print "Check finished"
    
# arcpy.GetParameter(0)
if __name__ == '__main__':
    #在此处将需要检查的数据库目录复制
    workSpace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"
    main(workSpace)

    

    
