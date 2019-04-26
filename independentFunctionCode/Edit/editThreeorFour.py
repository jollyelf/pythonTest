# -*- coding: cp936 -*-
import os
import arcpy
import re

# 设置工作空间
workSpace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"
arcpy.env.workspace=workSpace

def editThreeorFourPipeSegmentCode():
    '''
    利用空间连接，找到三通的主管和支管，填写三通的管段编码和主管直径、主管壁厚、支管直径和支管壁厚
    基本思路：
    首先删除重复要素
    然后利用空间连接，找到与三通交叉的管线
    如果管线的起点不和三通重合，这条管线大概率是主线，则将该管线的相关信息写入三通表中
    如果起点与三通的坐标重合，则该线大概率为支线，则将该管线的信息写入三通表中
    '''
    #删除重复要素
    arcpy.DeleteIdentical_management("T_PN_THREEORFOUR_GEO","Shape")
    #定义直径和公称直径的对应关系
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

    #如果已经存在临时文件"TFSpatialJoinClass"，则删除
    if arcpy.Exists("TFSpatialJoinClass"):
        arcpy.Delete_management("TFSpatialJoinClass")
    #如果已经存在临时文件"TFSpatialJoinOTOClass"，则删除
    if arcpy.Exists("TFSpatialJoinOTOClass"):
        arcpy.Delete_management("TFSpatialJoinOTOClass")
    #判断"OBJECTIDCOPY"是否存在三通表中
    fieldList = []
    for f in arcpy.ListFields("T_PN_THREEORFOUR_GEO"):
        fieldList.append(str(f.name))
    if "OBJECTIDCOPY" not in fieldList:
        #首先给三通添加一个用于复制OBJECTID的字段
        arcpy.AddField_management("T_PN_THREEORFOUR_GEO","OBJECTIDCOPY","TEXT")
        # 将目标表中的OBJECTID字段计算到设备编号中
        arcpy.CalculateField_management("T_PN_THREEORFOUR_GEO","OBJECTIDCOPY","!OBJECTID!","PYTHON")
    # 将要素与管段表进行空间连接，连接方式用交叉1对多
    arcpy.SpatialJoin_analysis("T_PN_THREEORFOUR_GEO","T_PN_PIPESEGMENT_GEO","TFSpatialJoinClass","JOIN_ONE_TO_MANY","","","INTERSECT","","")
    # 将要素与管段表进行空间连接，连接方式用交叉1对多
    arcpy.SpatialJoin_analysis("T_PN_THREEORFOUR_GEO","T_PN_PIPESEGMENT_GEO","TFSpatialJoinOTOClass","JOIN_ONE_TO_ONE","","","INTERSECT","","")
    
    TFMPPCodelist=[]
    with arcpy.da.SearchCursor("TFSpatialJoinClass",("OBJECTIDCOPY","JOIN_FID","CODE_1","DIAMETER","THICKNESS")) as TFCuosor:
        for TFrow in TFCuosor:
            with arcpy.da.SearchCursor("TFSpatialJoinOTOClass",("OBJECTIDCOPY","Join_Count")) as TOFCuosor:
                for TOFrow in TOFCuosor:
                    if TFrow[0]==TOFrow[0]:
                        TFMPPCodelist.append([TFrow[0],TFrow[1],TFrow[2],TFrow[3],TFrow[4],TOFrow[1]])
    #获取管段信息至列表
    PPDataList=[]
    with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("OBJECTID","SHAPE@")) as Pcursor:
        for Prow in Pcursor:
            PPDataList.append([Prow[0],Prow[1]])

    #更新三通表
    with arcpy.da.UpdateCursor("T_PN_THREEORFOUR_GEO",\
                               ("OBJECTIDCOPY","PSCODE","SHAPE@X","SHAPE@Y",\
                                "MAINDIAMETER","MAINTHICKNESS","MINORDIAMETER","MINORTHICKNESS")) as TFUcursor:
        for TFUrow in TFUcursor:
            try:
                for PPD in PPDataList:
                    for TFMPPL in TFMPPCodelist:
                        if TFUrow[0]==TFMPPL[0] and PPD[0]==TFMPPL[1]:
                            #如果只有一条线与三通点交汇，那么直接略过这个三通
                            if TFMPPL[5]==1:
                                pass
                            #如果靠近三通点的有两根管线，那么终点和起点均不是三通点的线为主管，起点为三通点的线为支管
                            elif TFMPPL[5]==2:
                                if not (abs(TFUrow[2]-PPD[1].firstPoint.X)<1e-5 and abs(TFUrow[3]-PPD[1].firstPoint.Y)<1e-5) \
                                   and \
                                   not (abs(TFUrow[2]-PPD[1].lastPoint.X)<1e-5 and abs(TFUrow[3]-PPD[1].lastPoint.Y)<1e-5):
                                    TFUrow[1]=TFMPPL[2]
                                    if TFMPPL[3] is not None:
                                        TFUrow[4]=DiameterDNDic[str(TFMPPL[3])]
                                        TFUrow[5]=TFMPPL[4]
                                if abs(TFUrow[2]-PPD[1].firstPoint.X)<1e-5 and abs(TFUrow[3]-PPD[1].firstPoint.Y)<1e-5:
                                    if TFMPPL[3] is not None:
                                        TFUrow[6]=DiameterDNDic[str(TFMPPL[3])]
                                        TFUrow[7]=TFMPPL[4]
                            #如果靠近该三通点有三根线，那么起止点均不是三通点的线为主管，或者终点为三通点的线为主管
                            elif TFMPPL[5]==3:
                                if abs(TFUrow[2]-PPD[1].lastPoint.X)<1e-5 and abs(TFUrow[3]-PPD[1].lastPoint.Y)<1e-5:
                                    TFUrow[1]=TFMPPL[2]
                                    if TFMPPL[3] is not None:
                                        TFUrow[4]=DiameterDNDic[str(TFMPPL[3])]
                                        TFUrow[5]=TFMPPL[4]
                                        TFUrow[6]=TFMPPL[5]
                                if not (abs(TFUrow[2]-PPD[1].firstPoint.X)<1e-5 and abs(TFUrow[3]-PPD[1].firstPoint.Y)<1e-5)\
                                   and \
                                   not (abs(TFUrow[2]-PPD[1].lastPoint.X)<1e-5 and abs(TFUrow[3]-PPD[1].lastPoint.Y)<1e-5):
                                    TFUrow[1]=TFMPPL[2]
                                    if TFMPPL[3] is not None:
                                        TFUrow[4]=DiameterDNDic[str(TFMPPL[3])]
                                        TFUrow[5]=TFMPPL[4]
                                        TFUrow[6]=TFMPPL[5]  
                            else:
                                TFUrow[6]=TFMPPL[5]
                            TFUcursor.updateRow(TFUrow)
            except Exception,e:
                print e.message
                pass
            continue
    # 删除连接是多出的临时字段
    arcpy.DeleteField_management("T_PN_THREEORFOUR_GEO",["OBJECTIDCOPY"])
    # 删除中间文件
    arcpy.Delete_management("TFSpatialJoinClass")
    arcpy.Delete_management("TFSpatialJoinOTOClass")

def editThreeorFourField():
    '''
    利用管段信息将管段相关信息写入三通表中
    基本思路：
    首先获取管段信息
    然后找到三通管段编码与管段编码一致的记录，将该三通记录的值由管线信息填充
    最后对三通进行编码
    '''
    
    #获取管段数据
    PipeSegmentDataList=[]
    with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("CODE","DIAMETER","THICKNESS","USEDDATE",\
                                                       "CONSTRUNIT","SUPERVISORUNIT","TESTUNIT","FDNAME","COLLECTDATE",\
                                                       "COLLECTUNIT","INPUTDATETIME","DESIGNPRESURE","NAME","SEGMATERIAL2","PIPENAME")) as PPcursor:
        for PC in PPcursor:
            if PC[0] is not None and str(PC[0]).strip()!="":
                PipeSegmentDataList.append([PC[0],PC[1],PC[2],PC[3],PC[4],PC[5],PC[6],PC[7],PC[8],PC[9],PC[10],PC[11],PC[12],PC[13],PC[14]])
    #更新三通数据
    tempDictionary={}       
    with arcpy.da.UpdateCursor("T_PN_THREEORFOUR_GEO",\
                               ("PSCODE","MAINDIAMETER","MAINTHICKNESS","INCONNECTMODE","MINORCONNECTMODE",\
                                "OUTCONNECTMODE","TXMATERIAL","USEDDATE","PRESSURELEVEL","CONSTRUNIT",\
                                "SUPERVISORUNIT","TESTUNIT","FDNAME","COLLECTDATE","COLLECTUNIT",\
                                "INPUTDATETIME","TXTYPE","MINORDIAMETER","PIPESEGNAME","CODE",\
                                "SHAPE@X","SHAPE@Y","X","Y","SPECIFICATIONS","PIPENAME")) as cursor:
        for row in cursor:
            try:
                #填写基本属性
                for PSD in PipeSegmentDataList:
                    if row[0]==PSD[0]:
                        #if PSD[1] is not None:
                            #row[1]=DiameterDNDic[str(PSD[1])]
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
                        row[25]=PSD[14]
                        cursor.updateRow(row)
                if row[0] is not None:
                    row[6]=1
                    row[22]=row[20]
                    row[23]=row[21]
                    cursor.updateRow(row)
                if row[0] is not None and row[1] is not None and row[17]>10:
                    if row[1]==row[17]:
                        row[16]=1
                    else:
                        row[16]=2
                    row[24]="DN"+str(int(row[1]))+"*"+str(int(row[1]))+"*"+str(int(row[17]))
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
    editThreeorFourField()
editThreeorFour()

                    
    
