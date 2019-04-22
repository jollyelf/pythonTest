# -*- coding: cp936 -*-
import arcpy
import re

# 设置工作空间
arcpy.env.workspace="C:\Users\lenovo\Desktop\PyTest\geodb.gdb"

#获取管线地理要素集中的所有要素类

featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")



#定义一个检测管段和设备设施表内部数据逻辑性检查的函数
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
    
    steelDiameterList=[14,17,17.2,18,21.3,22,25,26.9,32,33.7,34,38,42.4,45,48,48.4,57,60,60.3,73,76,76.1,88.9,\
                       89,108,114.3,133,140,159,168,168.3,219,219.1,273,323.9,325,355.6,377,406.4,426,\
                       457,480,508,530,610,630,711,720,813,820,914,920,1016,1020] #定义常用钢管管径列表
    PEDiameterList=[20,25,32,40,50,63,75,90,110,125,160,180,200,225,250,280,315,\
                    355,400,450,500,560,630,710,800,900,1000,1200]#定义PE管直径列表
    steelThicknessList=[1.2,1.6,2.0,2.8,3.0,3.5,4.0,4.5,5.0,6.0,6.5,7.0,8.0,9.5,11.0,13.0,14.0,15.0,\
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
                    if (PC[15] is not None) and (PC[7] is not None)\
                       and (str(PC[7]).strip()!=""):
                        if "-" in PC[7]:
                            if float(re.search(r'[^-]+$',PC[7]).group())>PC[15]:
                                PRLDPErrorList.append([PC[0],PC[1],PC[7],PC[15]])
                        elif "~" in PC[7]:
                            if float(re.search(r'[^~]+$',PC[7]).group())>PC[15]:
                                PRLDPErrorList.append([PC[0],PC[1],PC[7],PC[15]])                        
                        elif re.search(r'[0-0].[0-9]',PC[7]):
                            if float(PC[7])>PC[15]:
                                PRLDPErrorList.append([PC[0],PC[1],PC[7],PC[15]])
                        else:
                            continue

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
                        
                    
                
                
                
    if len(TRANSAMOUNTErrorList) !=0:
        print "管段表中存在实际输送量大于设计输送量的情况：\n"
        for TMEL in TRANSAMOUNTErrorList:
            print TMEL[0],TMEL[1],TMEL[2],TMEL[3]
    if len(PNPErrorList) !=0:
        print "管段表中存在上一管段和下一管段未填写的情况：\n"
        for PNPEL in PNPErrorList:
            print PNPEL[0],PNPEL[1]
    if len(PLDPErrorList) !=0:
        print "管段表中存在压力级别与设计压力填写的不匹配的情况：\n"
        for PLDPEL in PLDPErrorList:
            print PLDPEL[0],PLDPEL[1],PLDPEL[2],PLDPEL[3]
    if len(ANMErrorList) !=0:
        print "管段表中存在PE管有防腐方式的情况：\n"
        for ANMEL in ANMErrorList:
            print ANMEL[0],ANMEL[1],ANMEL[2],ANMEL[3]
    if len(PRLDPErrorList) !=0:
        print "管段表中存在运行压力大于设计压力的情况：\n"
        for PRLDPEL in PRLDPErrorList:
            print PRLDPEL[0],PRLDPEL[1],PRLDPEL[2],PRLDPEL[3]
    if len(DiameterErrorList)!=0:
        print "管段表中存在管径异常的情况：\n"
        for DEL in DiameterErrorList:
            print DEL[0],DEL[1],DEL[2]
    if len(ThicknessErrorList)!=0:
        print "管段表中存在壁厚异常的情况：\n"
        for TEL in ThicknessErrorList:
            print TEL[0],TEL[1],TEL[2]
    if len(MileageErrorList)!=0:
        print "管段表中存在里程异常的情况：\n"
        for MLE in MileageErrorList:
            print MLE[0],MLE[1],MLE[2],MLE[3],MLE[4]

            
            
    #检查管段名称重复情况
    if len(NameAndPLList)!=len(set(NameAndPLList)):
        print "管段表中存在同一管线下管段名称重复的情况：\n"
        duNameList=[]
        for NL in NameAndPLList:
            if NameAndPLList.count(NL)>1:
                duNameList.append(NL)
        for dc in set(duNameList):
            for NAO in NameAndOtherList:
                if NAO[3] in dc:
                    print NAO[0],NAO[1],NAO[2],NAO[3]


pipeSegmentLogicTest("T_PN_PIPESEGMENT_GEO")
                    
                

