# -*- coding: cp936 -*-
import os
import sys
import arcpy
import re



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

#定义一个检测管段数据逻辑性检查的函数
def pipeSegmentLogicTest(feature):
    '''
    该函数用于检查管段表中可能存在的逻辑错误：
    1、一般认为实际输送量应该小于设计输送量，如果实际输送量的值大于了设计输送量的值，认为出错；
    2、规定气源干线和输气干线必须填写上下游管线的编码和名称，如果未填写，则认为出错
    3、规定压力级别和设计压力之间存在逻辑关系，如果不符合该逻辑关系，则认为出错
    4、一般认为PE管是没有防腐方式的，如果错填为其他防腐方式，认为出错
    5、一般认为填写的实际运行压力需要小于设计压力，如果大于，认为出错
    6、规定同一管线下的管段名称不能重复，如果重复，认为出错
    7、常用钢管的的管径和壁厚都有规定的值，如果所填数据非不在这一范围内，认为出错
    '''
    #获取用于检查的管线表数据
    TRANSAMOUNTErrorList=[] #存在输送量错误的列表
    PNPErrorList=[]         #存在输气管线和气源干线上一管段和下一管段填写均为空的列表
    PLDPErrorList=[]        #存在压力级别与设计压力不匹配的情况的列表
    ANMErrorList=[]         #检查PE管的防腐方式是否填写正确
    PRLDPErrorList=[]       #检查运行压力是否小于设计压力
    MileageErrorList=[]     #检查管段里程可能出错的记录
    NameAndOtherList=[]     #管段名称及其相关的字段列表
    NameAndPLList=[]        #管段名称和管线编码列表
    
    steelDiameterList=[14,17,17.2,18,21.3,22,25,26.9,32,33.7,34,38,42.4,45,48,48.4,57,60,60.3,63,73,76,76.1,88.9,\
                       89,108,114,174,114.3,133,140,159,168,168.3,219,219.1,273,323.9,325,355.6,377,406.4,426,\
                       457,480,508,530,610,630,711,720,813,820,914,920,1016,1020] #定义常用钢管管径列表
    PEDiameterList=[20,25,32,40,50,63,75,90,110,125,160,180,200,225,250,280,315,\
                    355,400,450,500,560,630,710,800,900,1000,1200]#定义PE管直径列表
    steelThicknessList=[1.2,1.6,2.0,2.8,3.0,3.5,4.0,4.5,4.6,5.0,5.6,5.8,6.0,6.3,6.5,7.0,8.0,\
                        8.2,9.5,10.0,11.0,12.0,13.0,14.0,15.0,\
                        17.0,18.0,19.0,20.0,22.0,24.0,25.0,26.0,28.0,30.0,32.0,35.0,38.0,40.0,42.0,\
                        45.0,48.0,50.0,54.0] #定义钢管壁厚列表
    DiameterErrorList=[]
    ThicknessErrorList=[]
    if feature=="T_PN_PIPESEGMENT_GEO":
        with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("OBJECTID","CODE","SEGTYPE",\
                                                           "SEGMATERIAL2","DIAMETER","THICKNESS",\
                                                           "PRESSURELEVEL","RUNPRESSURE","PPSNAME",\
                                                           "PPSCODE","NPSNAME","NPSCODE","ANTISEPTICMODE",\
                                                           "TRANSAMOUNTDESIGN","TRANSAMOUNTREAL",\
                                                           "DESIGNPRESURE","NAME","PLCODE",\
                                                           "COLLECTDATE","COLLECTUNIT","INPUTDATETIME",\
                                                           "LENGTH","MSTART","MEND")) as PPcursor:
            for PC in PPcursor:
                try:
                     #设定管段编码已完成才进行下列检查
                    if (PC[1] is not None) and (str(PC[1]).strip()!=""):
                        #检查实际输送量是否小于设计输送量
                        if (PC[13] is not None) and (PC[14] is not None):
                            if PC[13]< PC[14]:
                                TRANSAMOUNTErrorList.append([PC[0],PC[1],PC[13],PC[14]])

                        #检查输气干线和气源干线的上一和下一段是否已填写
                        if (PC[2]==1 or PC[2]==2) and (PC[8] is None and PC[9] is None and \
                                                       PC[10] is None and PC[11] is None ):
                            PNPErrorList.append([PC[0],PC[1]])

                        #检查不同压力级别下的设计压力是否有误
                        if (PC[6] is not None) and (PC[15] is not None):
                            if(PC[6]==1) and (PC[15]<=1.6 or PC[15]>4):    #高压的范围为(1.6,4]
                                PLDPErrorList.append([PC[0],PC[1],PC[6],PC[15]])
                            if(PC[6]==2) and (PC[15]<=0.4 or PC[15]>1.6):  #次高压的范围为(0.4,1.6]
                                PLDPErrorList.append([PC[0],PC[1],PC[6],PC[15]])
                            if(PC[6]==3) and (PC[15]<0.01 or PC[15]>0.4):  #中压的范围为[0.01,0.4]
                                PLDPErrorList.append([PC[0],PC[1],PC[6],PC[15]])
                            if(PC[6]==4) and (PC[15]<0 or PC[15]>0.01):    #低压的范围为(0,0.01)
                                PLDPErrorList.append([PC[0],PC[1],PC[6],PC[15]])

                        #检查PE管的防腐方式应该为空
                        if (PC[3]==22 or PC[3]==23 or PC[3]==24 or PC[3]==25):
                            if PC[12]!=7 and PC[12] is not None:
                                ANMErrorList.append([PC[0],PC[1],PC[3],PC[12]])
                        
                        #检查运行压力是否是小于设计压力
                        if (PC[15] is not None) and (PC[7] is not None) and (str(PC[7]).strip()!=""):
                            if "-" in PC[7]:
                                if float(re.search(r'[^-]+$',PC[7]).group())>PC[15]:
                                    PRLDPErrorList.append([PC[0],PC[1],PC[7],PC[15]])
                            elif "~" in PC[7]:
                                if float(re.search(r'[^~]+$',PC[7]).group())>PC[15]:
                                    PRLDPErrorList.append([PC[0],PC[1],PC[7],PC[15]])                        
                            else:
                                if float(PC[7])>PC[15]:
                                    PRLDPErrorList.append([PC[0],PC[1],PC[7],PC[15]])

                        #管段名称及其相关字段数据加入列表
                        if(PC[16] is not None):
                            NameAndPLList.append(PC[17]+PC[16])
                            NameAndOtherList.append([PC[0],PC[1],PC[17],PC[16]])

                            

                        #管径检查(钢管和PE管)
                        if(PC[3]!=22 and PC[3]!=23 and PC[3]!=24 and PC[3]!=25):
                            if (PC[4] is not None) and (PC[4] not in steelDiameterList):
                                DiameterErrorList.append([PC[0],PC[1],PC[4]])
                        elif (PC[4] is not None) and (PC[4] not in PEDiameterList):
                            DiameterErrorList.append([PC[0],PC[1],PC[4]])


                        #钢管壁厚检查
                        if(PC[3]!=22 and PC[3]!=23 and PC[3]!=24 and PC[3]!=25):
                            if (PC[5] is not None) and (PC[5] not in steelThicknessList):
                                ThicknessErrorList.append([PC[0],PC[1],PC[5]])

                        #管段里程检查
                        if PC[22]is not None and PC[23] is not None and \
                           re.search(r'\d{6}GB\d{3}001',PC[1]) and PC[22]!=0:
                            MileageErrorList.append([PC[0],PC[1],PC[21],PC[22],PC[23]])
                        if PC[22]is not None and PC[23] is not None and abs(abs(PC[23]-PC[22])-PC[21])>0.001:
                            MileageErrorList.append([PC[0],PC[1],PC[21],PC[22],PC[23]])
                            
                except:
                    print PC[0],PC[1],PC[2],PC[3],PC[4],PC[5],PC[6],PC[7],PC[8],PC[9],PC[10],\
                          PC[11],PC[12],PC[13],PC[14],PC[15],PC[16],PC[17],PC[18],PC[19],PC[20]
                    pass
                continue
                
    f=open("result.txt","a+")            
    if len(TRANSAMOUNTErrorList) !=0:
        f.write("管段表中存在实际输送量大于设计输送量的情况：\n")
        for TMEL in TRANSAMOUNTErrorList:
            f.write(str(TMEL[0])+"\t"+str(TMEL[1])+"\t"+str(TMEL[2])+"\t"+str(TMEL[3])+"\n")
    if len(PNPErrorList) !=0:
        f.write("管段表中气源干线或输气干线存在上一管段和下一管段未填写的情况：\n")
        for PNPEL in PNPErrorList:
            f.write(str(PNPEL[0])+"\t"+str(PNPEL[1])+"\n")
    if len(PLDPErrorList) !=0:
        f.write("管段表中存在压力级别与设计压力填写不匹配的情况：\n")
        for PLDPEL in PLDPErrorList:
            f.write(str(PLDPEL[0])+"\t"+str(PLDPEL[1])+"\t"+str(PLDPEL[2])+"\t"+str(PLDPEL[3])+"\n")
    if len(ANMErrorList) !=0:
        f.write("管段表中存在PE管有防腐方式的情况：\n")
        for ANMEL in ANMErrorList:
            f.write(str(ANMEL[0])+"\t"+str(ANMEL[1])+"\t"+str(ANMEL[2])+"\t"+str(ANMEL[3])+"\n")
    if len(PRLDPErrorList) !=0:
        f.write("管段表中存在运行压力大于设计压力的情况：\n")
        for PRLDPEL in PRLDPErrorList:
            f.write(str(PRLDPEL[0])+"\t"+str(PRLDPEL[1])+"\t"+str(PRLDPEL[2])+"\t"+str(PRLDPEL[3])+"\n")
    if len(DiameterErrorList)!=0:
        f.write("管段表中存在管径异常的情况：\n")
        for DEL in DiameterErrorList:
            f.write(str(DEL[0])+"\t"+str(DEL[1])+"\t"+str(DEL[2])+"\n")
    if len(ThicknessErrorList)!=0:
        f.write("管段表中存在壁厚异常的情况：\n")
        for TEL in ThicknessErrorList:
            f.write(str(TEL[0])+"\t"+str(TEL[1])+"\t"+str(TEL[2])+"\n")
    if len(MileageErrorList)!=0:
        f.write("管段表中存在里程异常的情况：\n")
        for MLE in MileageErrorList:
            f.write(str(MLE[0])+"\t"+str(MLE[1])+"\t"+str(MLE[2])+"\t"+str(MLE[3])+"\t"+str(MLE[4])+"\n")
    

            
            
    #检查管段名称重复情况
    if len(NameAndPLList)!=len(set(NameAndPLList)):
        f.write("管段表中存在同一管线下管段名称重复的情况：\n")
        duNameList=[]
        for NL in NameAndPLList:
            if NameAndPLList.count(NL)>1:
                duNameList.append(NL)
        for dc in set(duNameList):
            for NAO in NameAndOtherList:
                try:
                    if NAO[3] in dc:
                        f.write(str(NAO[0])+"\t"+str(NAO[1])+"\t"+str(NAO[2])+"\t"\
                                +str(NAO[3].encode('gb2312'))+"\n")
                except UnicodeEncodeError:
                    print NAO[0],NAO[1],NAO[2],NAO[3],"管段名称重复"
                    pass
                continue
                    
    f.close()
                    


#定义一个检查必填字段是否为空的函数
def fieldIsNonetest(feature):
    '''
    检查所有要素表中必须填写的字段，在编码已填写的情况下，是否完成数据录入
    列出所有需要检查的字段，检查是否在表格中，如果在就进行判断
    '''
    #定义一个需要检查的所有字段的元组
    testFieldTuple=("NAME","PSCODE","MSTART","REFOBJSTART","OFFSETSTART",\
                    "XSTART","YSTART","MEND","REFOBJEND","OFFSETEND","XEND","YEND",\
                    "LENGTH","ADDRSTART","CROSSWIDTH","AREALEVEL","PLCODE","TRANSMEDIUM",\
                    "ADDREND","X","Y","MILEAGE","REFOBJ","OFFSET","COLLECTDATE","COMPLETBY1",\
                    "COLLECTUNIT","INPUTDATETIME")#检查如果只为None的所有错误
    testFieldTuple2=("NAME","PSCODE","REFOBJSTART","REFOBJEND","ADDRSTART","PLCODE",\
                    "ADDREND","REFOBJ","COLLECTUNIT")#检查字符型字段不为None但为""的错误
    FieldNameDic={"NAME":"名称","PSCODE":"管段编码","MSTART":"起点里程","REFOBJSTART":"起点相对位置参照物",\
                  "OFFSETSTART":"起点相对位置偏移量","XSTART":"起点X坐标","YSTART":"起点Y坐标","MEND":"终点里程",\
                  "REFOBJEND":"终点相对位置参照物","OFFSETEND":"终点相对位置偏移量","XEND":"终点X坐标",\
                  "YEND":"终点Y坐标","LENGTH":"长度","ADDRSTART":"起点位置地名","CROSSWIDTH":"穿跨越宽度",\
                  "AREALEVEL":"地区等级","PLCODE":"管线编码","TRANSMEDIUM":"输送介质","ADDREND":"终点位置地名",\
                  "X":"X坐标","Y":"Y坐标","MILEAGE":"里程","REFOBJ":"相对位置参照物","OFFSET":"相对位置偏移量",\
                  "COLLECTDATE":"采集日期","COMPLETBY1":"完成人","COLLECTUNIT":"采集单位","INPUTDATETIME":"录入时间"}
    
    fieldIsNoneList=[]   #定义存在字段为空的列表
    fieldList=[]         #定义表中字段的列表
    fieldNameList=[]     #定义表中字段名称的列表
    fieldList=arcpy.ListFields(feature)  #获取表中字段列表
    for FL in fieldList: #获取每一个表的所有字段名称
        fieldNameList.append(FL.name)
    for FT in testFieldTuple:
        if FT in fieldNameList:
            with arcpy.da.SearchCursor(feature,("OBJECTID","CODE",FT)) as cursor:
                for row in cursor:
                    try:
                        if (row[1] is not None) and (str(row[1]).strip()!=""):
                            if row[2] is None:
                                fieldIsNoneList.append([row[0],row[1],FT,row[2]])
                    except UnicodeEncodeError:
                        print row[0],row[1],FT,row[2]
                        pass
                    continue
    for FT2 in testFieldTuple2:
        if FT2 in fieldNameList:
            with arcpy.da.SearchCursor(feature,("OBJECTID","CODE",FT2)) as cursor:
                for row in cursor:
                    try:
                        if (row[1] is not None) and (str(row[1]).strip()!=""):
                            if row[2] is not None and row[2].strip()=="":
                                fieldIsNoneList.append([row[0],row[1],FT2,row[2]])
                    except:
                        print row[0],row[1],FT2,row[2]
                        pass
                    continue
    with open("result.txt","a+") as f:
        if len(fieldIsNoneList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"表中存在必填字段未填写的情况：\n")
            for FINL in fieldIsNoneList:
                try:
                    f.write(str(FINL[0])+"\t"+str(FINL[1])+"\t"+str(FieldNameDic[FINL[2]])+"\t"+str(FINL[3])+"\n")
                except:
                    print FINL[0],FINL[1],FieldNameDic[FINL[2]],FINL[3],"必填字段为空"
                    pass
                continue

                        
#定义一个检查编码是否重复的函数,并将结果打印至文件
def codeRepetitionTest(featureClass):
    codeList=[]
    codeAndObjList=[]
    with arcpy.da.SearchCursor(featureClass,("CODE","OBJECTID")) as cursor:
        for row in cursor:
            if row[0] is not None:
                codeAndObjList.append([row[1],row[0]])
                codeList.append(row[0])
    f=open("result.txt","a+")
    if len(codeList)!=len(set(codeList)):
        f.write(featureClassAliasDictionary[featureClass]+"("+str(featureClass)+")"+"存在编码重复，重复的编码为：\n")
        #将重复编码写入结果文件
        ducodeList=[]
        for cd in codeList:
            if codeList.count(cd)>1:
                ducodeList.append(cd)
        for dc in set(ducodeList):
            for CAO in codeAndObjList:
                try:
                    if dc == CAO[1]:
                        f.write(str(CAO[0])+"\t"+str(CAO[1])+"\n")
                except:
                    print CAO[0],CAO[1],"编码重复"
                    pass
                continue
    f.close()


#检查设备实施是否与其父设备编码匹配
def facilityAffiliationTest(feature):
    '''
    在原来检查设备设施和管段是否匹配的基础上做了优化，当前管段的编码直接通过设备实施与管段空间连接而来，而不是通过设备设施表中的管段编码字段
    '''
    #下面这些要素不需要自动填充管段编码
    notCheckFeatureTuple=("T_PN_PIPESEGMENT_GEO","T_PN_STATION_GEO","T_PN_SOURCE_GEO",\
                          "T_LP_GASCROSS_GEO","T_LP_CASING_GEO","T_PN_THREEORFOUR_GEO")
    FAErrorList=[]
    if feature not in notCheckFeatureTuple:
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
                #arcpy.JoinField_management(feature,"OBJECTIDCOPY","{}SpatialJoinClass".format(feature),"OBJECTIDCOPY","CODE_1")
                # 将属性连接后的字段计算成要素的管段编码
                with arcpy.da.SearchCursor("{}SpatialJoinClass".format(feature),\
                                           ("OBJECTIDCOPY","CODE","CODE_1")) as cursor:
                    for row in cursor:
                        if row[1] is not None and row[2] is not None and row[2] not in row[1]:
                            FAErrorList.append([row[0],row[1],row[2]])
                # 删除添加的临时字段
                arcpy.DeleteField_management(feature,"OBJECTIDCOPY")
                # 删除中间文件
                arcpy.Delete_management("{}SpatialJoinClass".format(feature))
                #打印存在错误的信息到文件
                with open("result.txt","a+") as f:
                    if len(FAErrorList)!=0:
                        f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"存在设备设施编码不匹配的情况：\n")
                        for FAE in FAErrorList:
                            f.write(str(FAE[0])+"\t"+str(FAE[1])+"\t"+str(FAE[2])+"\n")
                    
        except Exception,e:
            print e.message
            pass
                
#判断字段列表中是否存在CODE和PSCODE字段
def checkFieldIsIn(feature,Code):
    fieldList=arcpy.ListFields(feature)
    fieldNameList=[]
    for f in fieldList:
        fieldNameList.append(f.name)
    if Code in fieldNameList:
        return True
    else:
        return False

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
        f=open("result.txt","a+")
        f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"编码存在错误，错误编码为：\n")
        for cl in codeList:
            try:
                f.write(str(cl[0])+"\t"+str(cl[1])+"\n")
            except UnicodeEncodeError:
                print cl[0],cl[1],"设备设施编码有误"
                pass
            continue
        f.close()

#定义一个获取管段表数据的函数
def getPipeSegmentData():
    PipeSegmentList=[]
    with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("CODE","USEDDATE","DESIGNDEPNAME",\
                                                    "CONSTRUNIT","SUPERVISORUNIT","TESTUNIT",\
                                                    "FDNAME","COLLECTDATE","COLLECTUNIT",\
                                                    "INPUTDATETIME")) as PPcursor:
        for PC in PPcursor:
            if (PC[0] is not None) and (PC[0]!=""):
                PipeSegmentList.append([PC[0],PC[1],PC[2],PC[3],PC[4],PC[5],PC[6],PC[7],PC[8],PC[9]])
    return PipeSegmentList

#定义一个用于检查设备设施属性是否与管段属性保持一致的函数
def fieldIsSameTest(feature):
    #获取管段数据
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

    f=open("result.txt","a+")
    #检查九个参数中仅能检查三个参数的要素
    if feature in checkThreeFieldsList:
        CDErrorList=[]
        CUErrorList=[]
        #IDErrorList=[]
        with arcpy.da.SearchCursor(feature,("OBJECTID","PSCODE","COLLECTDATE","COLLECTUNIT",\
                                            "INPUTDATETIME","CODE")) as Tcousor:
            for TC in Tcousor:
                for PSL in PipeSegmentList:
                    if TC[5] is not None and TC[1]==PSL[0]:
                        if TC[2]!=PSL[7]:
                            CDErrorList.append([TC[0],TC[5],TC[2],TC[1],PSL[7]])
                        if TC[3]!=PSL[8]:
                            CUErrorList.append([TC[0],TC[5],TC[3],TC[1],PSL[8]])
                        #if TC[4]!=PSL[9]:
                            #IDErrorList.append([TC[0],TC[1]])
        if len(CDErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"中存在采集时间与管段采集时间不匹配的情况：\n")
            for CEL in CDErrorList:
                try:
                    f.write(str(CEL[0])+"\t"+str(CEL[1])+"\t"+str(CEL[2])+"\t"+str(CEL[3])+"\t"+str(CEL[4])+"\n")
                except:
                    print CEL[0],CEL[1],CEL[2],CEL[3],CEL[4],"采集时间不匹配"
                    pass
                continue
        if len(CUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"中存在采集单位与管段采集单位不匹配的情况：\n")
            for CUL in CUErrorList:
                try:
                    if CUL[2] is not None and CUL[4] is not None:
                        f.write(str(CUL[0])+"\t"+str(CUL[1])+"\t"+str(CUL[2].encode('gb2312'))\
                                +"\t"+str(CUL[3])+"\t"+str(CUL[4].encode('gb2312'))+"\n")
                    elif CUL[2] is None and CUL[4] is not None:
                        f.write(str(CUL[0])+"\t"+str(CUL[1])+"\t"+str(CUL[2])\
                                +"\t"+str(CUL[3])+"\t"+str(CUL[4].encode('gb2312'))+"\n")
                    elif CUL[2] is not None and CUL[4] is None:
                        f.write(str(CUL[0])+"\t"+str(CUL[1])+"\t"+str(CUL[2].encode('gb2312'))\
                                +"\t"+str(CUL[3])+"\t"+str(CUL[4])+"\n")
                except UnicodeEncodeError:
                    print CUL[0],CUL[1],CUL[2],CUL[3],CUL[4],"采集时间不匹配"
                    pass
                continue
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
                    if TC[9] is not None and TC[1]==PSL[0]:
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
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"中存在投用日期与管段投用日期不匹配的情况：\n")
            for UDL in UDErrorList:
                try:
                    f.write(str(UDL[0])+"\t"+str(UDL[1])+"\t"+str(UDL[2])+"\t"+str(UDL[3])+"\t"+str(UDL[4])+"\n")
                except:
                    print UDL[0],UDL[1],UDL[2],UDL[3],UDL[4],"投用日期不匹配"
                    pass
                continue
        if len(COUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"中存在施工单位与管段施工单位不匹配的情况：\n")
            for COL in COUErrorList:
                try:
                    if COL[2] is not None and COL[4] is not None:
                        f.write(str(COL[0])+"\t"+str(COL[1])+"\t"+str(COL[2].encode('gb2312'))\
                                +"\t"+str(COL[3])+"\t"+str(COL[4].encode('gb2312'))+"\n")
                    elif COL[2] is None and COL[4] is not None:
                        f.write(str(COL[0])+"\t"+str(COL[1])+"\t"+str(COL[2])\
                                +"\t"+str(COL[3])+"\t"+str(COL[4].encode('gb2312'))+"\n")
                    elif COL[2] is not None and COL[4] is None:
                        f.write(str(COL[0])+"\t"+str(COL[1])+"\t"+str(COL[2].encode('gb2312'))\
                                +"\t"+str(COL[3])+"\t"+str(COL[4])+"\n")
                except:
                    print COL[0],COL[1],COL[2],COL[3],COL[4],"施工单位不匹配"
                    pass
                continue
        if len(SUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"中存在监理单位与管段监理单位不匹配的情况：\n")
            for SUL in SUErrorList:
                try:
                    if SUL[2] is not None and SUL[4] is not None:
                        f.write(str(SUL[0])+"\t"+str(SUL[1])+"\t"+str(SUL[2].encode('gb2312'))\
                                +"\t"+str(SUL[3])+"\t"+str(SUL[4].encode('gb2312'))+"\n")
                    elif SUL[2] is None and SUL[4] is not None:
                        f.write(str(SUL[0])+"\t"+str(SUL[1])+"\t"+str(SUL[2])\
                                +"\t"+str(SUL[3])+"\t"+str(SUL[4].encode('gb2312'))+"\n")
                    elif SUL[2] is not None and SUL[4] is None:
                        f.write(str(SUL[0])+"\t"+str(SUL[1])+"\t"+str(SUL[2].encode('gb2312'))\
                                +"\t"+str(SUL[3])+"\t"+str(SUL[4])+"\n")
                except:
                    print SUL[0],SUL[1],SUL[2],SUL[3],SUL[4],"监理单位不匹配"
                    pass
                continue
        if len(FDErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"中存在竣工图纸及编号与管段竣工图纸及编号不匹配的情况：\n")
            for FDL in FDErrorList:
                try:
                    if FDL[2] is not None and FDL[4] is not None:
                        f.write(str(FDL[0])+"\t"+str(FDL[1])+"\t"+str(FDL[2].encode('gb2312'))\
                                +"\t"+str(FDL[3])+"\t"+str(FDL[4].encode('gb2312'))+"\n")
                    elif FDL[2] is None and FDL[4] is not None:
                        f.write(str(FDL[0])+"\t"+str(FDL[1])+"\t"+str(FDL[2])\
                                +"\t"+str(FDL[3])+"\t"+str(FDL[4].encode('gb2312'))+"\n")
                    elif FDL[2] is not None and FDL[4] is None:
                        f.write(str(FDL[0])+"\t"+str(FDL[1])+"\t"+str(FDL[2].encode('gb2312'))\
                                +"\t"+str(FDL[3])+"\t"+str(FDL[4])+"\n")
                except:
                    print FDL[0],FDL[1],FDL[2],FDL[3],FDL[4],"竣工图纸不匹配"
                    pass
                continue
        if len(CDErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"中存在采集时间与管段采集时间不匹配的情况：\n")
            for CEL in CDErrorList:
                try:
                    f.write(str(CEL[0])+"\t"+str(CEL[1])+"\t"+str(CEL[2])+"\t"+str(CEL[3])+"\t"+str(CEL[4])+"\n")
                except:
                    print CEL[0],CEL[0],CEL[0],CEL[0],CEL[0],"采集时间不匹配"
                    pass
                continue
        if len(CUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"中存在采集单位与管段采集单位不匹配的情况：\n")
            for CUL in CUErrorList:
                try:
                    if CUL[2] is not None and CUL[4] is not None:
                        f.write(str(CUL[0])+"\t"+str(CUL[1])+"\t"+str(CUL[2].encode('gb2312'))\
                                +"\t"+str(CUL[3])+"\t"+str(CUL[4].encode('gb2312'))+"\n")
                    elif CUL[2] is None and CUL[4] is not None:
                        f.write(str(CUL[0])+"\t"+str(CUL[1])+"\t"+str(CUL[2])\
                                +"\t"+str(CUL[3])+"\t"+str(CUL[4].encode('gb2312'))+"\n")
                    elif CUL[2] is not None and CUL[4] is None:
                        f.write(str(CUL[0])+"\t"+str(CUL[1])+"\t"+str(CUL[2].encode('gb2312'))\
                                +"\t"+str(CUL[3])+"\t"+str(CUL[4])+"\n")
                except:
                    print CUL[0],CUL[1],CUL[2],CUL[3],CUL[4],"采集单位不匹配"
                    pass
                continue
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
                    if TC[10] is not None and TC[1]==PSL[0]:
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
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"中存在投用日期与管段投用日期不匹配的情况：\n")
            for UDL in UDErrorList:
                try:
                    f.write(str(UDL[0])+"\t"+str(UDL[1])+"\t"+str(UDL[2])+"\t"+str(UDL[3])+"\t"+str(UDL[4])+"\n")
                except:
                    print UDL[0],UDL[1],UDL[2],UDL[3],UDL[4],"投用日期不匹配"
                    pass
                continue
        if len(COUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"中存在施工单位与管段施工单位不匹配的情况：\n")
            for COL in COUErrorList:
                try:
                    if COL[2] is not None and COL[4] is not None:
                        f.write(str(COL[0])+"\t"+str(COL[1])+"\t"+str(COL[2].encode('gb2312'))\
                                +"\t"+str(COL[3])+"\t"+str(COL[4].encode('gb2312'))+"\n")
                    elif COL[2] is None and COL[4] is not None:
                        f.write(str(COL[0])+"\t"+str(COL[1])+"\t"+str(COL[2])\
                                +"\t"+str(COL[3])+"\t"+str(COL[4].encode('gb2312'))+"\n")
                    elif COL[2] is not None and COL[4] is None:
                        f.write(str(COL[0])+"\t"+str(COL[1])+"\t"+str(COL[2].encode('gb2312'))\
                                +"\t"+str(COL[3])+"\t"+str(COL[4])+"\n")
                except:
                    print COL[0],COL[1],COL[2],COL[3],COL[4],"施工单位不匹配"
                    pass
                continue
        if len(SUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"中存在监理单位与管段监理单位不匹配的情况：\n")
            for SUL in SUErrorList:
                try:
                    if SUL[2] is not None and SUL[4] is not None:
                        f.write(str(SUL[0])+"\t"+str(SUL[1])+"\t"+str(SUL[2].encode('gb2312'))\
                                +"\t"+str(SUL[3])+"\t"+str(SUL[4].encode('gb2312'))+"\n")
                    elif SUL[2] is None and SUL[4] is not None:
                        f.write(str(SUL[0])+"\t"+str(SUL[1])+"\t"+str(SUL[2])\
                                +"\t"+str(SUL[3])+"\t"+str(SUL[4].encode('gb2312'))+"\n")
                    elif SUL[2] is not None and SUL[4] is None:
                        f.write(str(SUL[0])+"\t"+str(SUL[1])+"\t"+str(SUL[2].encode('gb2312'))\
                                +"\t"+str(SUL[3])+"\t"+str(SUL[4])+"\n")
                except:
                    print SUL[0],SUL[1],SUL[2],SUL[3],SUL[4],"监理单位不匹配"
                    pass
                continue
        if len(TUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"中存在检测单位与管段检测单位不匹配的情况：\n")
            for TUL in TUErrorList:
                try:
                    if TUL[2] is not None and TUL[4] is not None:
                        f.write(str(TUL[0])+"\t"+str(TUL[1])+"\t"+str(TUL[2].encode('gb2312'))\
                                +"\t"+str(TUL[3])+"\t"+str(TUL[4].encode('gb2312'))+"\n")
                    elif TUL[2] is None and TUL[4] is not None:
                        f.write(str(TUL[0])+"\t"+str(TUL[1])+"\t"+str(TUL[2])\
                                +"\t"+str(TUL[3])+"\t"+str(TUL[4].encode('gb2312'))+"\n")
                    elif TUL[2] is not None and TUL[4] is None:  
                        f.write(str(TUL[0])+"\t"+str(TUL[1])+"\t"+str(TUL[2].encode('gb2312'))\
                                +"\t"+str(TUL[3])+"\t"+str(TUL[4])+"\n")
                except:
                    print TUL[0],TUL[1],TUL[2],TUL[3],TUL[4],"检测单位不匹配"
                    pass
                continue
        if len(FDErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"中存在竣工图纸及编号与管段竣工图纸及编号不匹配的情况：\n")
            for FDL in FDErrorList:
                try:
                    if FDL[2] is not None and FDL[4] is not None:
                        f.write(str(FDL[0])+"\t"+str(FDL[1])+"\t"+str(FDL[2].encode('gb2312'))\
                                +"\t"+str(FDL[3])+"\t"+str(FDL[4].encode('gb2312'))+"\n")
                    elif FDL[2] is None and FDL[4] is not None:
                        f.write(str(FDL[0])+"\t"+str(FDL[1])+"\t"+str(FDL[2])\
                                +"\t"+str(FDL[3])+"\t"+str(FDL[4].encode('gb2312'))+"\n")
                    elif FDL[2] is not None and FDL[4] is None:
                        f.write(str(FDL[0])+"\t"+str(FDL[1])+"\t"+str(FDL[2].encode('gb2312'))\
                                +"\t"+str(FDL[3])+"\t"+str(FDL[4])+"\n")
                except:
                    print FDL[0],FDL[1],FDL[2],FDL[3],FDL[4],"竣工图纸不匹配"
                    pass
                continue
        if len(CDErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"中存在采集时间与管段采集时间不匹配的情况：\n")
            for CEL in CDErrorList:
                try:
                    f.write(str(CEL[0])+"\t"+str(CEL[1])+"\t"+str(CEL[2])+"\t"+str(CEL[3])+"\t"+str(CEL[4])+"\n")
                except:
                    print CEL[0],CEL[1],CEL[2],CEL[3],CEL[4],"采集时间不匹配"
                    pass
                continue
        if len(CUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"中存在采集单位与管段采集单位不匹配的情况：\n")
            for CUL in CUErrorList:
                try:
                    if CUL[2] is not None and CUL[4] is not None:
                        f.write(str(CUL[0])+"\t"+str(CUL[1])+"\t"+str(CUL[2].encode('gb2312'))\
                                +"\t"+str(CUL[3])+"\t"+str(CUL[4].encode('gb2312'))+"\n")
                    elif CUL[2] is None and CUL[4] is not None:
                        f.write(str(CUL[0])+"\t"+str(CUL[1])+"\t"+str(CUL[2])\
                                +"\t"+str(CUL[3])+"\t"+str(CUL[4].encode('gb2312'))+"\n")
                    elif CUL[2] is not None and CUL[4] is None:
                        f.write(str(CUL[0])+"\t"+str(CUL[1])+"\t"+str(CUL[2].encode('gb2312'))\
                                +"\t"+str(CUL[3])+"\t"+str(CUL[4])+"\n")
                except:
                    print CUL[0],CUL[1],CUL[2],CUL[3],CUL[4],"采集单位不匹配"
                    pass
                continue
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
                                            "COLLECTDATE","COLLECTUNIT","INPUTDATETIME","CODE")) as Tcousor:
            for TC in Tcousor:
                for PSL in PipeSegmentList:
                    if TC[10] is not None and TC[1]==PSL[0]:
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
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"中存在投用日期与管段投用日期不匹配的情况：\n")
            for UDL in UDErrorList:
                try:
                    f.write(str(UDL[0])+"\t"+str(UDL[1])+"\t"+str(UDL[2])+"\t"+str(UDL[3])+"\t"+str(UDL[4])+"\n")
                except:
                    print UDL[0],UDL[1],UDL[2],UDL[3],UDL[4],"投用日期不匹配"
                    pass
                continue
        if len(DUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"中存在设计单位与管段设计单位不匹配的情况：\n")
            for DUL in DUErrorList:
                try:
                    if DUL[2] is not None and DUL[4] is not None:
                        f.write(str(DUL[0])+"\t"+str(DUL[1])+"\t"+str(DUL[2].encode('gb2312'))\
                                +"\t"+str(DUL[3])+"\t"+str(DUL[4].encode('gb2312'))+"\n")
                    if DUL[2] is None and DUL[4] is not None:
                        f.write(str(DUL[0])+"\t"+str(DUL[1])+"\t"+str(DUL[2])\
                                +"\t"+str(DUL[3])+"\t"+str(DUL[4].encode('gb2312'))+"\n")
                    if DUL[2] is not None and DUL[4] is None:
                        f.write(str(DUL[0])+"\t"+str(DUL[1])+"\t"+str(DUL[2].encode('gb2312'))\
                                +"\t"+str(DUL[3])+"\t"+str(DUL[4])+"\n")
                except:
                    print DUL[0],DUL[0],DUL[0],DUL[0],DUL[0],"设计单位不匹配"
                    pass
                continue
        if len(COUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"中存在施工单位与管段施工单位不匹配的情况：\n")
            for COL in COUErrorList:
                try:
                    if COL[2] is not None and COL[4] is not None:
                        f.write(str(COL[0])+"\t"+str(COL[1])+"\t"+str(COL[2].encode('gb2312'))\
                                +"\t"+str(COL[3])+"\t"+str(COL[4].encode('gb2312'))+"\n")
                    elif COL[2] is None and COL[4] is not None:
                        f.write(str(COL[0])+"\t"+str(COL[1])+"\t"+str(COL[2])\
                                +"\t"+str(COL[3])+"\t"+str(COL[4].encode('gb2312'))+"\n")
                    elif COL[2] is not None and COL[4] is None:
                        f.write(str(COL[0])+"\t"+str(COL[1])+"\t"+str(COL[2].encode('gb2312'))\
                                +"\t"+str(COL[3])+"\t"+str(COL[4])+"\n")
                except:
                    print COL[0],COL[1],COL[2],COL[3],COL[4],"施工单位不匹配"
                    pass
                continue
        if len(SUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"中存在监理单位与管段监理单位不匹配的情况：\n")
            for SUL in SUErrorList:
                try:
                    if SUL[2] is not None and SUL[4] is not None:
                        f.write(str(SUL[0])+"\t"+str(SUL[1])+"\t"+str(SUL[2].encode('gb2312'))\
                                +"\t"+str(SUL[3])+"\t"+str(SUL[4].encode('gb2312'))+"\n")
                    elif SUL[2] is None and SUL[4] is not None:
                        f.write(str(SUL[0])+"\t"+str(SUL[1])+"\t"+str(SUL[2])\
                                +"\t"+str(SUL[3])+"\t"+str(SUL[4].encode('gb2312'))+"\n")
                    elif SUL[2] is not None and SUL[4] is None:
                        f.write(str(SUL[0])+"\t"+str(SUL[1])+"\t"+str(SUL[2].encode('gb2312'))\
                                +"\t"+str(SUL[3])+"\t"+str(SUL[4])+"\n")
                except:
                    print SUL[0],SUL[1],SUL[2],SUL[3],SUL[4],"监理单位不匹配"
                    pass
                continue
        if len(TUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"中存在检测单位与管段检测单位不匹配的情况：\n")
            for TUL in TUErrorList:
                try:
                    if TUL[2] is not None and TUL[4] is not None:
                        f.write(str(TUL[0])+"\t"+str(TUL[1])+"\t"+str(TUL[2].encode('gb2312'))\
                                +"\t"+str(TUL[3])+"\t"+str(TUL[4].encode('gb2312'))+"\n")
                    elif TUL[2] is None and TUL[4] is not None:
                        f.write(str(TUL[0])+"\t"+str(TUL[1])+"\t"+str(TUL[2])\
                                +"\t"+str(TUL[3])+"\t"+str(TUL[4].encode('gb2312'))+"\n")
                    elif TUL[2] is not None and TUL[4] is None:  
                        f.write(str(TUL[0])+"\t"+str(TUL[1])+"\t"+str(TUL[2].encode('gb2312'))\
                                +"\t"+str(TUL[3])+"\t"+str(TUL[4])+"\n")
                except:
                    print TUL[0],TUL[1],TUL[2],TUL[3],TUL[4],"检测单位不匹配"
                    pass
                continue
        if len(CDErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"中存在采集时间与管段采集时间不匹配的情况：\n")
            for CEL in CDErrorList:
                try:
                    f.write(str(CEL[0])+"\t"+str(CEL[1])+"\t"+str(CEL[2])+"\t"+str(CEL[3])+"\t"+str(CEL[4])+"\n")
                except:
                    print CEL[0],CEL[1],CEL[2],CEL[3],CEL[4],"采集时间不匹配"
                    pass
                continue
        if len(CUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"中存在采集单位与管段采集单位不匹配的情况：\n")
            for CUL in CUErrorList:
                try:
                    if CUL[2] is not None and CUL[4] is not None:
                        f.write(str(CUL[0])+"\t"+str(CUL[1])+"\t"+str(CUL[2].encode('gb2312'))\
                                +"\t"+str(CUL[3])+"\t"+str(CUL[4].encode('gb2312'))+"\n")
                    elif CUL[2] is None and CUL[4] is not None:
                        f.write(str(CUL[0])+"\t"+str(CUL[1])+"\t"+str(CUL[2])\
                                +"\t"+str(CUL[3])+"\t"+str(CUL[4].encode('gb2312'))+"\n")
                    elif CUL[2] is not None and CUL[4] is None:
                        f.write(str(CUL[0])+"\t"+str(CUL[1])+"\t"+str(CUL[2].encode('gb2312'))\
                                +"\t"+str(CUL[3])+"\t"+str(CUL[4])+"\n")
                except:
                    print CUL[0],CUL[1],CUL[2],CUL[3],CUL[4],"采集单位不匹配"
                    pass
                continue
        #if len(IDErrorList)!=0:
         #   print featureClassAliasDictionary[feature],feature, "中存在录入时间与管段录入时间不匹配的情况："
          #  for IEL in IDErrorList:
           #     print IEL
    f.close()
def facilityDiameterTest(feature):
    #设定允许的DN值列表
    DNValueList=[15,20,25,32,40,50,65,80,100,125,150,200,250,300,350,400,450,500,600]
    #所有管径值列表
    DiameterList=[14, 17, 17.2, 18, 20, 21.3, 22, 25, 26.9, 32, 33.7, 34, 38, 40, 42.4, \
                  45, 48, 48.4, 50, 57, 60, 60.3, 63, 73, 75, 76, 76.1, 88.9, 89, 90, \
                  108, 110, 114.3, 125, 133, 140, 159, 160, 168, 168.3, 180, 200, 219, \
                  219.1, 225, 250, 273, 280, 315, 323.9, 325, 355, 355.6, 377, 400, 406,406.4, \
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
                   "400.0":400,"406.0":400,"406.4":400,"426.0":400,"450.0":450,"457.0":450,"480.0":450,"500.0":500,\
                   "508.0":500,"530.0":500,"560.0":500,"610.0":600,"630.0":600,"710.0":700,"711.0":700,\
                   "720.0":700,"800.0":800,"813.0":800,"820.0":800,"900.0":900,"914.0":900,"920.0":900,\
                   "1000.0":1000,"1016.0":1000,"1020.0":1000,"1200.0":1000}
    twoDiameterFeatureList=["T_PN_REDUCER_GEO","T_PN_SPE_GEO","T_PN_VALVE_GEO",\
                            "T_PN_ELBOW_GEO","T_PN_IJOINT_GEO"]
    diaFieldNameDict={"INDIAMETER":"入口直径","OUTDIAMETER":"出口直径","DIAMETER":"直径",\
                   "MAINPIPEDIAMETER":"主管道外径","MAINDIAMETER":"主管直径","MINORDIAMETER":"支管直径"}

    DNErrorList=[]
    PipeSegmentDataList=[]
    with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("CODE","DIAMETER")) as PPcursor:
        for PC in PPcursor:
            try:
                if (PC[0] is not None) and (str(PC[0]).strip()!="") and \
                   (PC[1] is not None) and (PC[1] in DiameterList):
                    PipeSegmentDataList.append([PC[0],PC[1]])
            except:
                print PC[0],PC[1]
                pass
            continue
    #如果输入为异径管/刚塑转换接头/阀门/弯头/绝缘接头
    if feature in twoDiameterFeatureList:
        with arcpy.da.SearchCursor(feature,("OBJECTID","CODE","INDIAMETER","OUTDIAMETER","PSCODE"))\
             as REcursor:
            for RProw in REcursor:
                for PLS in PipeSegmentDataList:
                    try:
                        if RProw[4]==PLS[0] and RProw[2]!=DiameterDNDic[str(round(PLS[1],1))]:
                            DNErrorList.append([RProw[0],PLS[0],PLS[1],RProw[1],"INDIAMETER",RProw[2]])
                        if RProw[4]==PLS[0] and RProw[3] not in DNValueList:
                            DNErrorList.append([RProw[0],PLS[0],PLS[1],RProw[1],"OUTDIAMETER",RProw[3]])
                    except:
                        print RProw[0],PLS[0],PLS[1],RProw[1],RProw[2],RProw[3],"入口/出口直径异常"
                        pass
                    continue

    #如果输入为立管
    if feature =="T_PN_PIPERISER_GEO":
        with arcpy.da.SearchCursor(feature,("OBJECTID","CODE","DIAMETER","PSCODE"))\
             as REcursor:
            for RProw in REcursor:
                for PLS in PipeSegmentDataList:
                    try:
                        if RProw[3]==PLS[0] and RProw[2]!=DiameterDNDic[str(round(PLS[1],1))]:
                            DNErrorList.append([RProw[0],PLS[0],PLS[1],RProw[1],"DIAMETER",RProw[2]])
                    except:
                        print RProw[0],PLS[0],PLS[1],RProw[1],"DIAMETER",RProw[2]
                        pass
                    continue
    #如果输入为开孔
    if feature =="T_PN_TAPPING_GEO":
        with arcpy.da.SearchCursor(feature,("OBJECTID","CODE","MAINPIPEDIAMETER","PSCODE"))\
             as REcursor:
            for RProw in REcursor:
                for PLS in PipeSegmentDataList:
                    try:
                        if RProw[3]==PLS[0] and RProw[2]!=DiameterDNDic[str(round(PLS[1],1))]:
                            DNErrorList.append([RProw[0],PLS[0],PLS[1],RProw[1],"MAINPIPEDIAMETER",RProw[2]])
                    except:
                        print RProw[0],PLS[0],PLS[1],RProw[1],"MAINPIPEDIAMETER",RProw[2]
                        pass
                    continue

    #如果输入为三通四通
    if feature=="T_PN_THREEORFOUR_GEO":
        with arcpy.da.SearchCursor(feature,("OBJECTID","CODE","MAINDIAMETER","MINORDIAMETER","PSCODE"))\
             as REcursor:
            for RProw in REcursor:
                for PLS in PipeSegmentDataList:
                    try:
                        if RProw[4]==PLS[0] and RProw[2]!=DiameterDNDic[str(round(PLS[1],1))]:
                            DNErrorList.append([RProw[0],PLS[0],PLS[1],RProw[1],"MAINDIAMETER",RProw[2]])
                        if RProw[4]==PLS[0] and RProw[3] is not None and RProw[3] not in DNValueList:
                            DNErrorList.append([RProw[0],PLS[0],PLS[1],RProw[1],"MINORDIAMETER",RProw[3]])
                    except:
                        print RProw[0],PLS[0],PLS[1],RProw[1],RProw[2],RProw[3],"主管/支管管径异常"
    with open("result.txt","a+") as f:                    
        if len(DNErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"存在管径填写异常情况：\n")
            for DNEL in DNErrorList:
                try:
                    f.write(str(DNEL[0])+"\t"+str(DNEL[1])+"\t"+\
                            str(DNEL[2])+"\t"+str(DNEL[3])+"\t"+str(diaFieldNameDict[DNEL[4]])+"\t"+str(DNEL[5])+"\n")
                except:
                    print DNEL[0],DNEL[1],DNEL[2],DNEL[3],diaFieldNameDict[DNEL[4]],DNEL[5],"设备直径与管段直径不匹配"
                    pass
                continue
                    
