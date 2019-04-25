# -*- coding: cp936 -*-
import os
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
#定义一个特殊字段填充的函数
def fieldsFill(feature):
    '''
    本方法利用已完成的管段表信息，在对要素进行管段匹配之后，进行属性的填充，这些属性包括：投用日期、设计单位、
      施工单位、监理单位、检测单位，竣工图纸及编号、采集日期、采集单位、录入日期、管线名称、管段名称、管径等
    首先获取管段表属性；
    然后获取要素表属性列表，如果需要填充的字段在属性列表中，则依据管段表的数据填充该字段
    特别注意的是管径需要采用管段管径的DN值，部分表格中只需要填充入口直径和壁厚
    '''
    doNotFillTableTuple=("T_PN_PIPESEGMENT_GEO","T_PN_STATION_GEO","T_PN_SOURCE_GEO","T_LP_GASCROSS_GEO","T_LP_CASING_GEO","T_PN_THREEORFOUR_GEO")
    #定义一个通用的填充属性字段元组
    fillGeneralFieldTuple=("PIPENAME","PIPESEGNAME","PIPESEGNO","USEDDATE","DESIGNDEPNAME","CONSTRUNIT",\
                          "SUPERVISORUNIT","TESTUNIT","FDNAME","COLLECTDATE","COLLECTUNIT","INPUTDATETIME")
    
    pipeSegmentdataFieldTuple=("OBJECTID","CODE","PIPENAME","NAME","USEDDATE","DESIGNDEPNAME",\
                              "CONSTRUNIT","SUPERVISORUNIT","TESTUNIT","FDNAME","COLLECTDATE",\
                              "COLLECTUNIT","INPUTDATETIME")
    
    fieldsSequenceDic={"OBJECTID":0,"CODE":1,"PIPENAME":2,"NAME":3,"USEDDATE":4,"DESIGNDEPNAME":5,\
                              "CONSTRUNIT":6,"SUPERVISORUNIT":7,"TESTUNIT":8,"FDNAME":9,"COLLECTDATE":10,\
                              "COLLECTUNIT":11,"INPUTDATETIME":12}
    #获取管段管径数据数据
    PipeSegmentDataList=[]
    with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",pipeSegmentdataFieldTuple) as PPcursor:
        for PC in PPcursor:
            if PC[0] is not None and str(PC[0]).strip()!="":
                PipeSegmentDataList.append([PC[0],PC[1],PC[2],PC[3],PC[4],PC[5],PC[6],\
                                            PC[7],PC[8],PC[9],PC[10],PC[11],PC[12]])

    
    fieldList=[]
    fieldNameList=[]
    if feature not in doNotFillTableTuple and int(arcpy.GetCount_management(feature).getOutput(0))!=0:
        fieldList=arcpy.ListFields(feature)  #获取表中字段列表
        for FL in fieldList: #获取每一个表的所有字段名称
            fieldNameList.append(FL.name)

        #填充列表中一般要素,遍历字典表中的每一个字段，如果该字段在某一个要素表中，该字段的值为空时，将管段表数据写入对应的要素表中
        #    其中各要素类的管段名称字段不统一（存在两种：PIPESEGNAME，PIPESEGNO）
        for FGFT in fillGeneralFieldTuple:
            if FGFT in fieldNameList:
                try:
                    with arcpy.da.UpdateCursor(feature,("PSCODE",FGFT)) as cursor:
                        for row in cursor:
                            if row[0] is not None:
                                for PLS in PipeSegmentDataList:
                                    if FGFT !="PIPESEGNAME" and FGFT !="PIPESEGNO":
                                        #if row[0]==PLS[1] and PLS[fieldsSequenceDic[FGFT]] is not None
                                        if row[0]==PLS[1]:
                                            row[1]=PLS[fieldsSequenceDic[FGFT]]
                                            cursor.updateRow(row)
                                    else:
                                        #if row[0]==PLS[1] and PLS[fieldsSequenceDic["NAME"]] is not None
                                        if row[0]==PLS[1]:
                                            row[1]=PLS[fieldsSequenceDic["NAME"]]
                                            cursor.updateRow(row)
                                    
                except Exception, e:
                    print e.message
                    pass
                continue
for fc in featureClassList:
    print featureClassAliasDictionary[fc]
    fieldsFill(fc)
print "FillFinished"


    

