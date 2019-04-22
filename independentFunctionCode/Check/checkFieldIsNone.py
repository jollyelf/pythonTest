
import arcpy
import re

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


def fieldIsNonetest(feature):
    print feature
    '''
    检查所有要素表中必须填写的字段，在编码已填写的情况下，是否完成数据录入
    列出所有需要检查的字段，检查是否在表格中，如果在就进行判断
    '''
    #定义一个需要检查的所有字段的元组
    testFieldTuple=("NAME","PSCODE","MSTART","REFOBJSTART","OFFSETSTART",\
                    "XSTART","YSTART","MEND","REFOBJEND","OFFSETEND","XEND","YEND",\
                    "LENGTH","ADDRSTART","CROSSWIDTH","AREALEVEL","PLCODE","TRANSMEDIUM",\
                    "ADDREND","X","Y","MILEAGE","REFOBJ","OFFSET","COLLECTDATE","COMPLETBY1",\
                    "COLLECTUNIT","INPUTDATETIME")
    testFieldTuple2=("NAME","PSCODE","REFOBJSTART","REFOBJEND","ADDRSTART","PLCODE",\
                    "ADDREND","REFOBJ","COLLECTUNIT")
    
    fieldIsNoneList=[]   #定义存在字段为空的列表
    fieldList=[]         #定义表中字段的列表
    fieldNameList=[]     #定义表中字段名称的列表
    fieldList=arcpy.ListFields(feature)  #获取表中字段列表
    LoopNumber=0
    for FL in fieldList: #获取每一个表的所有字段名称
        fieldNameList.append(FL.name)
    for FT in testFieldTuple:
        if FT in fieldNameList:
            with arcpy.da.SearchCursor(feature,("OBJECTID","CODE",FT)) as cursor:
                for row in cursor:
                    if (row[1] is not None and str(row[1].encode("utf-8").decode("unicode-escape")).strip()!=""):
                        if row[2] is None:
                            fieldIsNoneList.append([row[0],row[1],FT,row[2]])
    for FT2 in testFieldTuple2:
        if FT2 in fieldNameList:
            with arcpy.da.SearchCursor(feature,("OBJECTID","CODE",FT2)) as cursor:
                for row in cursor:
                    if (row[1] is not None and str(row[1]).strip()!=""):
                        if row[2] is not None and row[2].strip()=="":
                            fieldIsNoneList.append([row[0],row[1],FT2,row[2]])
    if len(fieldIsNoneList)!=0:
        print featureClassAliasDictionary[feature]+str(feature) +"表中存在必填字段未填写的情况：\n"
        for FINL in fieldIsNoneList:
            print FINL[0],FINL[1],FINL[2],FINL[3]
            
for fc in featureClassList:
    fieldIsNonetest(fc)

                        
                    
        
    
    
            
        

