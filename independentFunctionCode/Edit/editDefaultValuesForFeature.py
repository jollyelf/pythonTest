# -*- coding: cp936 -*-
import os
import arcpy
import re

# 设置工作空间
workSpace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"
arcpy.env.workspace=workSpace

def editDefaultValuesForFeature():
    #获取管段数据
    PipeSegmentDataList=[]
    with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("CODE","DESIGNPRESURE","RUNPRESSURE","SEGMATERIAL2",\
                                                       "ANTISEPTICMODE")) as PPcursor:
        for PC in PPcursor:
            if PC[0] is not None and str(PC[0]).strip()!="":
                PipeSegmentDataList.append([PC[0],PC[1],PC[2],PC[3],PC[4]])
    #编辑阀井阀室表，设计运行压力=管段设计压力，实际运行压力=管段实际压力
    if int(arcpy.GetCount_management("T_PN_VALVEPIT_GEO").getOutput(0))!=0:
        with arcpy.da.UpdateCursor("T_PN_VALVEPIT_GEO",("PSCODE","DESIGNPRESSURE","RUNPRESSURE")) as VPcursor:
            for VProw in VPcursor:
                try:
                    for PSD in PipeSegmentDataList:
                        if VProw[0]==PSD[0]:
                            VProw[1]=str(PSD[1])
                            if "-" in PSD[2]:
                                VProw[2]=float(re.search(r'[^-]+$',PSD[2]).group())
                            if "~" in PSD[2]:
                                VProw[2]=float(re.search(r'[^~]+$',PSD[2]).group())
                            else:
                                VProw[2]=float(PSD[2])
                            VPcursor.updateRow(VProw)
                except Exception,e:
                    print "编辑阀井阀室默认值时出错，错误信息：",e.message
                    pass
                continue
    #编辑阀门表，压力等级=管段设计压力，阀门构造类型=球阀，驱动类型=手动，进口/出口连接方式=焊接（管段为钢管）=热熔连接（管段为PE），正常/当前阀门状态=常开，阀门功能=调节，是否可远程控制=否
    if int(arcpy.GetCount_management("T_PN_VALVE_GEO").getOutput(0))!=0:
        with arcpy.da.UpdateCursor("T_PN_VALVE_GEO",("PSCODE","PRESSURELEVEL","VALVETYPE","DRIVETYPE","INCONNECTMODE",\
                                                     "NORMALSTATE","CURRENTSTATE","OUTCONNECTMODE","VALVEFUNC","ISREMOTECONTROL"\
                                                     )) as Vcursor:
            for Vrow in Vcursor:
                try:
                    for PSD in PipeSegmentDataList:
                        if Vrow[0]==PSD[0]:
                            Vrow[1]=PSD[1]
                            #如果管段为PE则连接方式默认为热熔连接，如果为钢管则默认为焊接
                            if PSD[3] is not None:
                                if PSD[3]!=22 and PSD[3]!=23 and PSD[3]!=24 and PSD[3]!=25:
                                    Vrow[4]=1
                                    Vrow[7]=1
                                else:
                                    Vrow[4]=7
                                    Vrow[7]=7
                    if Vrow[0] is not None:
                        Vrow[2]=2
                        Vrow[3]=3
                        Vrow[5]=1
                        Vrow[6]=1
                        Vrow[8]=1
                        Vrow[9]=0
                    Vcursor.updateRow(Vrow)
                except Exception,e:
                    print "编辑阀门默认值时出错，错误信息：",e.message
                    pass
                continue
    #编辑刚塑转换接头表，压力等级=管段设计压力
    if int(arcpy.GetCount_management("T_PN_SPE_GEO").getOutput(0))!=0:
        with arcpy.da.UpdateCursor("T_PN_SPE_GEO",("PSCODE","PRESSURELEVEL")) as SPcursor:
            for SProw in SPcursor:
                try:
                    for PSD in PipeSegmentDataList:
                        if SProw[0]==PSD[0]:
                            SProw[1]=PSD[1]
                            SPcursor.updateRow(SProw)
                except Exception,e:
                    print "编辑刚塑转换接头默认值时出错，错误信息：",e.message
                    pass
                continue
    #编辑调压箱表，进口压力=管段设计压力，运行压力=管段运行压力
    if int(arcpy.GetCount_management("T_PN_REGULATOR_GEO").getOutput(0))!=0:
        with arcpy.da.UpdateCursor("T_PN_REGULATOR_GEO",("PSCODE","INPRESSURE","RUNPRESSURE")) as REcursor:
            for RErow in REcursor:
                try:
                    for PSD in PipeSegmentDataList:
                        if RErow[0]==PSD[0]:
                            RErow[1]=PSD[1]
                            RErow[2]=PSD[2]
                    REcursor.updateRow(RErow)
                except Exception,e:
                    print "编辑调压箱默认值时出错，错误信息：",e.message
                    pass
                continue
    #编辑异径管表，压力等级=管段设计压力，进口/出口连接方式=焊接（管段为钢管）=热熔连接（管段为PE）
    if int(arcpy.GetCount_management("T_PN_REDUCER_GEO").getOutput(0))!=0:
        with arcpy.da.UpdateCursor("T_PN_REDUCER_GEO",("PSCODE","PRESSURELEVEL","INCONNECTMODE","OUTCONNECTMODE")) as REDcursor:
            for REDrow in REDcursor:
                try:
                    for PSD in PipeSegmentDataList:
                        if REDrow[0]==PSD[0]:
                            REDrow[1]=PSD[1]
                    if REDrow[0] is not None:
                        if PSD[3] is not None:
                            if PSD[3]!=22 and PSD[3]!=23 and PSD[3]!=24 and PSD[3]!=25:
                                REDrow[2]=1
                                REDrow[3]=1
                            else:
                                REDrow[2]=7
                                REDrow[3]=7
                    REDcursor.updateRow(REDrow)
                except Exception,e:
                    print "编辑异径管默认值时出错，错误信息：",e.message
                    pass
                continue
    #编辑绝缘接头表，压力等级=管段设计压力，进口/出口连接方式=焊接
    if int(arcpy.GetCount_management("T_PN_IJOINT_GEO").getOutput(0))!=0:
        with arcpy.da.UpdateCursor("T_PN_IJOINT_GEO",("PSCODE","PRESSURELEVEL","INCONNECTMODE","OUTCONNECTMODE")) as IJcursor:
            for IJrow in IJcursor:
                try:
                    for PSD in PipeSegmentDataList:
                        if IJrow[0]==PSD[0]:
                            IJrow[1]=PSD[1]
                    if IJrow[0] is not None:
                        IJrow[2]=1
                        IJrow[3]=1
                    IJcursor.updateRow(IJrow)
                except Exception,e:
                    print "编辑聚缘接头默认值时出错，错误信息：",e.message
                    pass
                continue
    #编辑弯头表，压力等级=管段设计压力，弯管类型=正常弯头，进口/出口连接方式=焊接（管段为钢管）=热熔连接（管段为PE）,材料=碳钢（如果管段材料不是PE）
    if int(arcpy.GetCount_management("T_PN_ELBOW_GEO").getOutput(0))!=0:
        with arcpy.da.UpdateCursor("T_PN_ELBOW_GEO",("PSCODE","PRESSURELEVEL","ELBOWTYPE","INCONNECTMODE",\
                                                     "OUTCONNECTMODE","ELBOWMATERIAL","ANTISEPTICMATERIAL")) as ELcursor:
            for ELrow in ELcursor:
                try:
                    for PSD in PipeSegmentDataList:
                        if ELrow[0]==PSD[0]:
                            ELrow[1]=PSD[1]
                            if PSD[3] is not None:
                                if PSD[3]!=22 and PSD[3]!=23 and PSD[3]!=24 and PSD[3]!=25:
                                    ELrow[5]=1
                                    ELrow[3]=1
                                    ELrow[4]=1
                                else:
                                    ELrow[3]=7
                                    ELrow[4]=7
                    if ELrow[0] is not None:
                        ELrow[2]=1
                        ELrow[3]=1
                        ELrow[4]=1
                    ELcursor.updateRow(ELrow)
                except Exception,e:
                    print "编辑弯头默认值时出错，错误信息：",e.message
                    pass
                continue
editDefaultValuesForFeature()
            
