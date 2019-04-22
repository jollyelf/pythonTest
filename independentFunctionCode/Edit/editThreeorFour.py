# -*- coding: cp936 -*-
import os
import arcpy
import re

# 设置工作空间
workSpace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"
arcpy.env.workspace=workSpace

def editThreeorFourPipeSegmentCode():
    #利用三通表与管段进行空间连接

    
    #首先给三通添加一个用于复制OBJECTID的字段
    arcpy.AddField_management("T_PN_THREEORFOUR_GEO","OBJECTIDCOPY","TEXT")
    # 将目标表中的OBJECTID字段计算到设备编号中
    arcpy.CalculateField_management("T_PN_THREEORFOUR_GEO","OBJECTIDCOPY","!OBJECTID!","PYTHON")
    # 将要素与管段表进行空间连接，连接方式用最近
    arcpy.SpatialJoin_analysis("T_PN_THREEORFOUR_GEO","T_PN_PIPESEGMENT_GEO","TFSpatialJoinClass","","","","INTERSECT","0.01 Kilometers","")
    TFMPPCodelist=[]
    with arcpy.da.SearchCursor("TFSpatialJoinClass",("OBJECTIDCOPY","JOIN_FID","CODE_1")) as TFCuosor:
        for TFrow in TFCuosor:
            TFMPPCodelist.append([TFrow[0],TFrow[1],TFrow[2]])
    with arcpy.da.UpdateCursor("T_PN_THREEORFOUR_GEO",\
                               ("OBJECTIDCOPY","PSCODE","SHAPE@X","SHAPE@Y")) as TFUcursor:
        for TFUrow in TFUcursor:
            with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("OBJECTID","SHAPE@")) as Pcursor:
                for Prow in Pcursor:
                    for TFMPPL in TFMPPCodelist:
                        if TFUrow[0]==TFMPPL[0] and Prow[0]==TFMPPL[1]:
                            if not (abs(TFUrow[2]-Prow[1].firstPoint.X)<1e-10\
                               and abs(TFUrow[3]-Prow[1].firstPoint.Y)<1e-10):
                                TFUrow[1]=TFMPPL[2]
    # 删除连接是多出的临时字段
    arcpy.DeleteField_management("T_PN_THREEORFOUR_GEO",["OBJECTIDCOPY"])
    # 删除中间文件
    arcpy.Delete_management("TFSpatialJoinClass")
    
def editThreeorFourField():
    #设定直径与DN值之间的健-值关系
    DiameterDNDic={"14.0":10,"15.0":10,"17.0":10,"17.2":10,"18.0":15,"20.0":15,"21.3":15,"22.0":15,"25.0":20,"26.9":20,\
                   "32.0":25,"33.7":25,"34.0":25,"38.0":32,"40.0":32,"42":32,"42.4":32,"45.0":40,"48.0":40,\
                   "48.4":40,"50.0":40,"57.0":50,"60.0":50,"60.3":50,"63.0":50,"73.0":65,"75.0":65,"76.0":65,\
                   "76.1":65,"88.9":80,"89.0":80,"90.0":80,"108.0":100,"110.0":100,"114.0":100,"114.3":100,\
                   "125.0":125,"133.0":125,"140.0":125,"159.0":150,"160.0":150,"168.0":150,"168.3":150,"174.0":150,\
                   "180.0":150,"188.0":150,"200.0":200,"219.0":200,"219.1":200,"225.0":200,"250.0":250,"273.0":250,\
                   "280.0":250,"315.0":300,"323.9":300,"325.0":300,"355.0":350,"355.6":350,"377.0":350,\
                   "400.0":400,"406.4":400,"426.0":400,"450.0":450,"457.0":450,"480.0":450,"500.0":500,\
                   "508.0":500,"530.0":500,"560.0":500,"610.0":600,"630.0":600,"710.0":700,"711.0":700,\
                   "720.0":700,"800.0":800,"813.0":800,"820.0":800,"900.0":900,"914.0":900,"920.0":900,\
                   "1000.0":1000,"1016.0":1000,"1020.0":1000,"1200.0":1000}
    #获取管段数据
    PipeSegmentDataList=[]
    with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("CODE","DIAMETER","THICKNESS","USEDDATE",\
                                                       "CONSTRUNIT","SUPERVISORUNIT","TESTUNIT","FDNAME","COLLECTDATE",\
                                                       "COLLECTUNIT","INPUTDATETIME","DESIGNPRESURE","NAME","SEGMATERIAL2")) as PPcursor:
        for PC in PPcursor:
            if PC[0] is not None and str(PC[0]).strip()!="":
                PipeSegmentDataList.append([PC[0],PC[1],PC[2],PC[3],PC[4],PC[5],PC[6],PC[7],PC[8],PC[9],PC[10],PC[11],PC[12],PC[13]])
    #更新三通数据
    tempDictionary={}       
    with arcpy.da.UpdateCursor("T_PN_THREEORFOUR_GEO",\
                               ("PSCODE","MAINDIAMETER","MAINTHICKNESS","INCONNECTMODE","MINORCONNECTMODE",\
                                "OUTCONNECTMODE","TXMATERIAL","USEDDATE","PRESSURELEVEL","CONSTRUNIT",\
                                "SUPERVISORUNIT","TESTUNIT","FDNAME","COLLECTDATE","COLLECTUNIT",\
                                "INPUTDATETIME","TXTYPE","MINORDIAMETER","PIPESEGNAME","CODE",\
                                "SHAPE@X","SHAPE@Y","X","Y")) as cursor:
        for row in cursor:
            try:
                #填写基本属性
                for PSD in PipeSegmentDataList:
                    if row[0]==PSD[0]:
                        if PSD[1] is not None:
                            row[1]=DiameterDNDic[str(PSD[1])]
                        if PSD[13] is not None:
                            if PSD[13]!=22 and PSD[13]!=23 and PSD[13]!=24 and PSD[13]!=25:
                                row[3]=1
                                row[4]=1
                                row[5]=1
                            else:
                                row[3]=7
                                row[4]=7
                                row[5]=7
                        row[2]=PSD[2]
                        row[7]=PSD[3]
                        row[8]=PSD[11]
                        row[9]=PSD[4]
                        row[10]=PSD[5]
                        row[11]=PSD[6]
                        row[12]=PSD[7]
                        row[13]=PSD[8]
                        row[14]=PSD[9]
                        row[15]=PSD[10]
                        row[18]=PSD[12]
                        cursor.updateRow(row)
                if row[0] is not None:
                    row[6]=1
                    row[22]=row[20]
                    row[23]=row[21]
                    cursor.updateRow(row)
                if row[0] is not None and row[1] is not None and row[17] is not None:
                    if row[1]==row[17]:
                        row[16]=1
                    else:
                        row[16]=2
                    cursor.updateRow(row)
                #进行编码
                tempValue=0
                if row[0] is not None and len(row[0])==14 and re.search(r'\d{6}GB\d{6}',row[0]):
                    key=row[0]+"STA"
                    if tempDictionary.has_key(key):
                        tempValue=tempDictionary[key]
                        row[19]=key + str(tempValue+1).zfill(3)
                        tempDictionary[key]=tempValue+1
                        cursor.updateRow(row)
                    else:
                        tempDictionary[key]=1
                        row[19]=key + str(tempValue+1).zfill(3)
                        cursor.updateRow(row)
            except Exception,e:
                print "编辑三通四通时出错，错误信息：",e.message
                pass
            continue
def editThreeorFour():
    editThreeorFourPipeSegmentCode()
editThreeorFour()

                    
    
