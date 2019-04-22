# -*- coding: cp936 -*-
import arcpy

# 设置工作空间
arcpy.env.workspace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"

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
    PipeSegmentList=[]
    with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("CODE","USEDDATE","DESIGNDEPNAME",\
                                                    "CONSTRUNIT","SUPERVISORUNIT","TESTUNIT",\
                                                    "FDNAME","COLLECTDATE","COLLECTUNIT",\
                                                    "INPUTDATETIME")) as PPcursor:
        for PC in PPcursor:
            if (PC[0] is not None) and (PC[0]!=""):
                PipeSegmentList.append([PC[0],PC[1],PC[2],PC[3],PC[4],PC[5],PC[6],PC[7],PC[8],PC[9]])

    
    #用列表分类要素类的检查数量
    checkZeroFieldsList=["T_PN_SOURCE_GEO","T_PN_STATION_GEO","T_PN_PIPESEGMENT_GEO"]
    checkThreeFieldsList=["T_GE_BUILDING_GEO","T_GE_EMI_GEO","T_GE_GEOHAZARD_GEO",\
                      "T_GE_HLINE_GEO","T_GE_HPOLYGON_GEO","T_GE_OTHPIPEPNT_GEO",\
                      "T_GE_RAILWAY_GEO","T_GE_ROAD_GEO","T_GE_UNDROBSTACLE_GEO"]
    checkSevenFieldsList=["T_BS_ELECMARK_GEO","T_BS_GROUNDMARK_GEO","T_CP_CPPOWER_GEO",\
                      "T_CP_TESTTRUNK_GEO","T_LP_ADDTLYR_GEO","T_LP_APPENDANT_GEO",\
                      "T_LP_CONDENSER_GEO","T_LP_OPTICALHOLE_GEO","T_PN_BELLOW_GEO",\
                      "T_PN_BLOCK_GEO","T_PN_IJOINT_GEO","T_PN_PRYCABINET_GEO",\
                      "T_PN_REDUCER_GEO","T_PN_REGULATOR_GEO","T_PN_SPE_GEO",\
                      "T_PN_TAPPING_GEO","T_PN_VALVEPIT_GEO"]
    checkEightFieldsList=["T_CP_ANODEBED_GEO","T_CP_DRNGDEVICE_GEO","T_CP_FLEXANODE_GEO",\
                      "T_CP_RSANODE_GEO","T_CP_SANODE_GEO","T_LP_CASING_GEO",\
                      "T_LP_GASCROSS_GEO","T_LP_HYDRPROTECT_GEO","T_LP_TUNNEL_GEO",\
                      "T_PN_ELBOW_GEO","T_PN_PEPIPEWELD_GEO","T_PN_SEAMCUT_GEO",\
                      "T_PN_THREEORFOUR_GEO","T_PN_VALVE_GEO"]
    checkNineFieldsList=["T_PN_PIPERISER_GEO"]
    #检查九个参数中仅能检查三个参数的要素
    if feature in checkThreeFieldsList:
        CDErrorList=[]
        CUErrorList=[]
        #IDErrorList=[]
        with arcpy.da.SearchCursor(feature,("OBJECTID","PSCODE","COLLECTDATE","COLLECTUNIT",\
                                            "INPUTDATETIME","CODE")) as Tcousor:
            for TC in Tcousor:
                for PSL in PipeSegmentList:
                    if TC[1] is not None and TC[1]==PSL[0]:
                        if TC[2]!=PSL[7]:
                            CDErrorList.append([TC[0],TC[5],TC[2],TC[1],PSL[7]])
                        if TC[3]!=PSL[8]:
                            CUErrorList.append([TC[0],TC[5],TC[3],TC[1],PSL[8]])
                        #if TC[4]!=PSL[9]:
                            #IDErrorList.append([TC[0],TC[1]])
        if len(CDErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"中存在采集时间与管段采集时间不匹配的情况：\n"
            for CEL in CDErrorList:
                print CEL[0],CEL[1],CEL[2],CEL[3],CEL[4]
        if len(CUErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"中存在采集单位与管段采集单位不匹配的情况：\n"
            for CUL in CUErrorList:
                print CUL[0],CUL[1],CUL[2],CUL[3],CUL[4]
        #if len(IDErrorList)!=0:
            #print featureClassAliasDictionary[feature],feature, "中存在录入时间与管段录入时间不匹配的情况："
            #for IEL in IDErrorList:
                #print IEL

    #检查九个参数中仅能检查七个参数的要素            
    if feature in checkSevenFieldsList:
        UDErrorList=[]
        COUErrorList=[]
        SUErrorList=[]
        FDErrorList=[]
        CDErrorList=[]
        CUErrorList=[]
        #IDErrorList=[]
        with arcpy.da.SearchCursor(feature,("OBJECTID","PSCODE","USEDDATE",\
                                            "CONSTRUNIT","SUPERVISORUNIT",\
                                            "FDNAME","COLLECTDATE","COLLECTUNIT",\
                                            "INPUTDATETIME","CODE")) as Tcousor:
            for TC in Tcousor:
                for PSL in PipeSegmentList:
                    if TC[1] is not None and TC[1]==PSL[0]:
                        if TC[2]!=PSL[1]:
                            UDErrorList.append([TC[0],TC[9],TC[2],TC[1],PSL[1]])
                        if TC[3]!=PSL[3]:
                            COUErrorList.append([TC[0],TC[9],TC[3],TC[1],PSL[3]])
                        if TC[4]!=PSL[4]:
                            SUErrorList.append([TC[0],TC[9],TC[4],TC[1],PSL[4]])
                        if TC[5]!=PSL[6]:
                            FDErrorList.append([TC[0],TC[9],TC[5],TC[1],PSL[6]])
                        if TC[6]!=PSL[7]:
                            CDErrorList.append([TC[0],TC[9],TC[6],TC[1],PSL[7]])
                        if TC[7]!=PSL[8]:
                            CUErrorList.append([TC[0],TC[9],TC[7],TC[1],PSL[8]])
                        #if TC[8]!=PSL[9]:
                            #IDErrorList.append([TC[0],TC[1]])
        if len(UDErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"中存在投用日期与管段投用日期不匹配的情况：\n"
            for UDL in UDErrorList:
                print UDL[0],UDL[1],UDL[2],UDL[3],UDL[4]
        if len(COUErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"中存在施工单位与管段施工单位不匹配的情况：\n"
            for COL in COUErrorList:
                print COL[0],COL[1],COL[2],COL[3],COL[4]
        if len(SUErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"中存在监理单位与管段监理单位不匹配的情况：\n"
            for SUL in SUErrorList:
                print SUL[0],SUL[1],SUL[2],SUL[3],SUL[4]
        if len(FDErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"中存在竣工图纸及编号与管段竣工图纸及编号不匹配的情况：\n"
            for FDL in FDErrorList:
                print FDL[0],FDL[1],FDL[2],FDL[3],FDL[4]
        if len(CDErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"中存在采集时间与管段采集时间不匹配的情况：\n"
            for CEL in CDErrorList:
                print CEL[0],CEL[1],CEL[2],CEL[3],CEL[4]
        if len(CUErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"中存在采集单位与管段采集单位不匹配的情况：\n"
            for CUL in CUErrorList:
                print CUL[0],CUL[1],CUL[2],CUL[3],CUL[4]
        #if len(IDErrorList)!=0:
            #print featureClassAliasDictionary[feature],feature, "中存在录入时间与管段录入时间不匹配的情况："
            #for IEL in IDErrorList:
                #print IEL

    #检查九个参数中仅能检查八个参数的要素            
    if feature in checkEightFieldsList:
        UDErrorList=[]
        COUErrorList=[]
        SUErrorList=[]
        FDErrorList=[]
        TUErrorList=[]
        CDErrorList=[]
        CUErrorList=[]
        #IDErrorList=[]
        with arcpy.da.SearchCursor(feature,("OBJECTID","PSCODE","USEDDATE",\
                                            "CONSTRUNIT","SUPERVISORUNIT","TESTUNIT",\
                                            "FDNAME","COLLECTDATE","COLLECTUNIT",\
                                            "INPUTDATETIME","CODE")) as Tcousor:
            for TC in Tcousor:
                for PSL in PipeSegmentList:
                    if TC[1] is not None and TC[1]==PSL[0]:
                        if TC[2]!=PSL[1]:
                            UDErrorList.append([TC[0],TC[10],TC[2],TC[1],PSL[1]])
                        if TC[3]!=PSL[3]:
                            COUErrorList.append([TC[0],TC[10],TC[3],TC[1],PSL[3]])
                        if TC[4]!=PSL[4]:
                            SUErrorList.append([TC[0],TC[10],TC[4],TC[1],PSL[4]])
                        if TC[5]!=PSL[5]:
                           TUErrorList.append([TC[0],TC[10],TC[5],TC[1],PSL[5]]) 
                        if TC[6]!=PSL[6]:
                            FDErrorList.append([TC[0],TC[10],TC[6],TC[1],PSL[6]])
                        if TC[7]!=PSL[7]:
                            CDErrorList.append([TC[0],TC[10],TC[7],TC[1],PSL[7]])
                        if TC[8]!=PSL[8]:
                            CUErrorList.append([TC[0],TC[10],TC[8],TC[1],PSL[8]])
                        #if TC[9]!=PSL[9]:
                            #IDErrorList.append([TC[0],TC[1]])

        if len(UDErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"中存在投用日期与管段投用日期不匹配的情况：\n"
            for UDL in UDErrorList:
                print UDL[0],UDL[1],UDL[2],UDL[3],UDL[4]
        if len(COUErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"中存在施工单位与管段施工单位不匹配的情况：\n"
            for COL in COUErrorList:
                print COL[0],COL[1],COL[2],COL[3],COL[4]
        if len(SUErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"中存在监理单位与管段监理单位不匹配的情况：\n"
            for SUL in SUErrorList:
                print SUL[0],SUL[1],SUL[2],SUL[3],SUL[4]
        if len(TUErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"中存在检测单位与管段检测单位不匹配的情况：\n"
            for TUL in TUErrorList:
                print TUL[0],TUL[1],TUL[2],TUL[3],TUL[4]
        if len(FDErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"中存在竣工图纸及编号与管段竣工图纸及编号不匹配的情况：\n"
            for FDL in FDErrorList:
                print FDL[0],FDL[1],FDL[2],FDL[3],FDL[4]
        if len(CDErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"中存在采集时间与管段采集时间不匹配的情况：\n"
            for CEL in CDErrorList:
                print CEL[0],CEL[1],CEL[2],CEL[3],CEL[4]
        if len(CUErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"中存在采集单位与管段采集单位不匹配的情况：\n"
            for CUL in CUErrorList:
                print CUL[0],CUL[1],CUL[2],CUL[3],CUL[4]
        #if len(IDErrorList)!=0:
         #   print featureClassAliasDictionary[feature],feature, "中存在录入时间与管段录入时间不匹配的情况："
          #  for IEL in IDErrorList:
           #     print IEL


    #检查九个参数中能检查九个参数的要素 立管中缺竣工图纸字段           
    if feature in checkNineFieldsList:
        UDErrorList=[]
        DUErrorList=[]
        COUErrorList=[]
        SUErrorList=[]
        TUErrorList=[]
        CDErrorList=[]
        CUErrorList=[]
        #IDErrorList=[]
        with arcpy.da.SearchCursor(feature,("OBJECTID","PSCODE","USEDDATE","DESIGNDEPNAME",\
                                            "CONSTRUNIT","SUPERVISORUNIT","TESTUNIT",\
                                            "COLLECTDATE","COLLECTUNIT","INPUTDATETIME",\
                                            "CODE")) as Tcousor:
            for TC in Tcousor:
                for PSL in PipeSegmentList:
                    if TC[1] is not None and TC[1]==PSL[0]:
                        if TC[2]!=PSL[1]:
                            UDErrorList.append([TC[0],TC[10],TC[2],TC[1],PSL[1]])
                        if TC[3]!=PSL[2]:
                            DUErrorList.append([TC[0],TC[10],TC[3],TC[1],PSL[2]])
                        if TC[4]!=PSL[3]:
                            COUErrorList.append([TC[0],TC[10],TC[4],TC[1],PSL[3]])
                        if TC[5]!=PSL[4]:
                            SUErrorList.append([TC[0],TC[10],TC[5],TC[1],PSL[4]])
                        if TC[6]!=PSL[5]:
                           TUErrorList.append([TC[0],TC[10],TC[6],TC[1],PSL[5]]) 
                        if TC[7]!=PSL[7]:
                            CDErrorList.append([TC[0],TC[10],TC[7],TC[1],PSL[7]])
                        if TC[8]!=PSL[8]:
                            CUErrorList.append([TC[0],TC[10],TC[8],TC[1],PSL[8]])
                        #if TC[9]!=PSL[9]:
                         #   IDErrorList.append([TC[0],TC[1]])
        if len(UDErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"中存在投用日期与管段投用日期不匹配的情况：\n"
            for UDL in UDErrorList:
                print UDL[0],UDL[1],UDL[2],UDL[3],UDL[4]
        if len(DUErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"中存在设计单位与管段设计单位不匹配的情况：\n"
            for DUL in DUErrorList:
                print DUL[0],DUL[1],DUL[2],DUL[3],DUL[4]
        if len(COUErrorList)!=0:
            print featureClassAliasDictionary[feature]+feature,"中存在施工单位与管段施工单位不匹配的情况：\n"
            for COL in COUErrorList:
                print COL[0],COL[1],COL[2],COL[3],COL[4]
        if len(SUErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"中存在监理单位与管段监理单位不匹配的情况：\n"
            for SUL in SUErrorList:
                print SUL[0],SUL[1],SUL[2],SUL[3],SUL[4]
        if len(TUErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"中存在检测单位与管段检测单位不匹配的情况：\n"
            for TUL in TUErrorList:
                print TUL[0],TUL[1],TUL[2],TUL[3],TUL[4]
        if len(CDErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"中存在采集时间与管段采集时间不匹配的情况：\n"
            for CEL in CDErrorList:
                print CEL[0],CEL[1],CEL[2],CEL[3],CEL[4]
        if len(CUErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"中存在采集单位与管段采集单位不匹配的情况：\n"
            for CUL in CUErrorList:
                print CUL[0],CUL[1],CUL[2],CUL[3],CUL[4]
        #if len(IDErrorList)!=0:
         #   print featureClassAliasDictionary[feature],feature, "中存在录入时间与管段录入时间不匹配的情况："
          #  for IEL in IDErrorList:
           #     print IEL




for fc in featureClassList:
    fieldIsSameTest(fc)
