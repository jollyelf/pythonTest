# -*- coding: cp936 -*-
import arcpy
import re

#定义一个要素文件名和别称的字典
featureClassAliasDictionary={"T_BS_ELECMARK_GEO":"电子标识器","T_BS_GROUNDMARK_GEO":"地面标示物","T_CP_ANODEBED_GEO":"阳极地床",\
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
                             "T_PN_PIPESEGMENT_GEO":"管段"}
#罗列每一个图层的目标字符字典
featureClassCodeDictionary={"T_BS_ELECMARK_GEO":"DBA","T_BS_GROUNDMARK_GEO":"BSA",\
                            "T_CP_ANODEBED_GEO":"YDA","T_CP_CPPOWER_GEO":"YBD",\
                            "T_CP_DRNGDEVICE_GEO":"PLA","T_CP_FLEXANODE_GEO":"RYA",\
                            "T_CP_RSANODE_GEO":"XYA","T_CP_SANODE_GEO":"XYA",\
                            "T_CP_TESTTRUNK_GEO":"CSA","T_GE_BUILDING_GEO":"GEJ",\
                            "T_GE_EMI_GEO":"GEG","T_GE_GEOHAZARD_GEO":"GEZ",\
                            "T_GE_HLINE_GEO":"GEH","T_GE_HPOLYGON_GEO":"",\
                            "T_GE_OTHPIPEPNT_GEO":"GES","T_GE_RAILWAY_GEO":"GET",\
                            "T_GE_ROAD_GEO":"GED","T_GE_UNDROBSTACLE_GEO":"GEA",\
                            "T_LP_ADDTLYR_GEO":"FSH","T_LP_APPENDANT_GEO":"XXX",\
                            "T_LP_CASING_GEO":"TGA","T_LP_CONDENSER_GEO":"FSJ",\
                            "T_LP_GASCROSS_GEO":"PTA","T_LP_HYDRPROTECT_GEO":"HPA",\
                            "T_LP_OPTICALHOLE_GEO":"GKA","T_LP_TUNNEL_GEO":"FSI",\
                            "T_PN_BELLOW_GEO":"BWA","T_PN_BLOCK_GEO":"FDA",\
                            "T_PN_ELBOW_GEO":"WGA","T_PN_IJOINT_GEO":"JTB",\
                            "T_PN_PEPIPEWELD_GEO":"HKA","T_PN_PIPERISER_GEO":"GDA",\
                            "T_PN_PRYCABINET_GEO":"TYG","T_PN_REDUCER_GEO":"YGA",\
                            "T_PN_REGULATOR_GEO":"TYX","T_PN_SEAMCUT_GEO":"HFA",\
                            "T_PN_SOURCE_GEO":"Z","T_PN_SPE_GEO":"JTC","T_PN_STATION_GEO":"Z",\
                            "T_PN_TAPPING_GEO":"KKA","T_PN_THREEORFOUR_GEO":"STA",\
                            "T_PN_VALVE_GEO":"FMB","T_PN_VALVEPIT_GEO":"FJA",\
                            "T_PN_PIPESEGMENT_GEO":"GB"}
#管段编码填写函数
def PPCodeFill(feature):
    """
    此函数利用空间连接的方式，给设备设施表中的管段编码字段进行填写；
    其中，管段表，站场表，气源表为特殊表格不用填写；
    穿跨越表和套管表一般在管段划分完成后直接将穿跨越管段进行复制，因此不需要填充；
    基本思路：
    首先，将需要填充管段编码的要素中OBJECTID字段进行复制出来（进行空间关联和属性关联保证要素的对应性）；
    然后，利用空间连接，找到与要素最近的管段；
    然后，利用不变的OBJECTID将空间连接后的表与要素表进行属性连接；
    然后，将管段编码字段计算到目标要素表中；
    最后，删除用于中间传递数据的数据表。
    """
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

#坐标填充函数
def coordinateFill(feature):
    '''
    本函数用于对要素的坐标值进行填写。
    在管段编码填写完成并正确的情况下，填写该要素的坐标值；
    填写要素坐标值之前必须确定数据坐标系为大地2000坐标系;
    
    对于点状要素填写其XY;
    对于现状要素填写其起止点的XY，填写之前一定确保线型的方向正确;
    对于站场、气源、管段不计算其XY坐标；
    对于第三方管道，地址灾害和电流干扰，库中为点状要素，但字段中为线状类型，不计算；

    基本思路：
    填写之前需要判断待处理的要素是点状要素还是线状要素；
        如果是点状要素：
        则采用其"SHAPE@X","SHAPE@Y"几何属性值直接赋值给要素的XY属性
        如果是线状要素：
        这利用其几何属性的第一个点的几何属性赋值给起点，第二个点的几何属性赋值给终点
    '''
    notFillTuple=("T_PN_PIPESEGMENT_GEO","T_PN_SOURCE_GEO","T_PN_STATION_GEO",\
                  "T_GE_OTHPIPEPNT_GEO","T_GE_EMI_GEO","T_GE_GEOHAZARD_GEO")
    if feature not in notFillTuple:
        if arcpy.Describe(feature).spatialReference.name=="GCS_China_Geodetic_Coordinate_System_2000":
            if arcpy.Describe(feature).shapeType=="Point":
                with arcpy.da.UpdateCursor(feature,("PSCODE","X","Y","SHAPE@X","SHAPE@Y")) \
                     as cursor:
                    for row in cursor:
                        try:
                           if row[0] is not None and len(row[0])==14 and\
                              re.search(r'\d{6}GB\d{6}',row[0]):
                               row[1]=row[3]
                               row[2]=row[4]
                               cursor.updateRow(row)
                        except Exception, e:
                            print e.message
                            pass
                        continue
            elif arcpy.Describe(feature).shapeType=="Polyline":
                with arcpy.da.UpdateCursor(feature,("PSCODE","XSTART","YSTART","XEND","YEND",\
                                                    "SHAPE@")) as cursor:
                    for row in cursor:
                        try:
                           if row[0] is not None and len(row[0])==14 and\
                              re.search(r'\d{6}GB\d{6}',row[0]):
                               row[1]=row[5].firstPoint.X
                               row[2]=row[5].firstPoint.Y
                               row[3]=row[5].lastPoint.X
                               row[4]=row[5].lastPoint.Y
                               cursor.updateRow(row)
                        except Exception, e:
                            print e.message
                            pass
                        continue 
        else:
            print arcpy.Describe(feature).spatialReference.name

#定义一个要素编码的函数
def featureCoding(feature):
    '''
    本函数用于对已进行管段匹配的设备设施进行自动编码（编码保证不重复，但不按照空间顺序来排序）。
    每一个要素类中都给定一个默认的特征编码如下(其中气源、站场和管段不编码，附属物和面状水系编码未定，用XXX表示)：
    T_PN_VALVEPIT_GEO 	    阀井阀室 	FJA     T_PN_VALVE_GEO 	    阀门 	FMB
    T_PN_THREEORFOUR_GEO    三通四通 	STA     T_PN_TAPPING_GEO    开孔 	KKA
    T_PN_STATION_GEO 	    场站 	Z       T_PN_SPE_GEO 	    钢塑转换接头 	JTC
    T_PN_SOURCE_GEO 	    气源 	Z       T_PN_SEAMCUT_GEO    金属焊缝和补口 HFA
    T_PN_REGULATOR_GEO     调压箱 	TYX     T_PN_REDUCER_GEO    异径管 	YGA
    T_PN_PRYCABINET_GEO     撬装柜 	TYG     T_PN_PIPESEGMENT_GEO管段 	GB
    T_PN_PIPERISER_GEO 	    立管 	GDA     T_PN_PEPIPEWELD_GEO PE管焊接 	HKA
    T_PN_IJOINT_GEO 	    绝缘接头 	JTB     T_PN_ELBOW_GEO 	    弯头 	WGA
    T_PN_BLOCK_GEO 	    封堵物 	FDA     T_PN_BELLOW_GEO     波纹管 	BWA
    T_LP_TUNNEL_GEO 	    隧道 	FSI     T_LP_OPTICALHOLE_GEO光缆人手孔 	GKA
    T_LP_HYDRPROTECT_GEO    水工保护 	HPA     T_LP_GASCROSS_GEO   穿跨越 	PTA
    T_LP_CONDENSER_GEO 	    凝水缸 	FSJ     T_LP_CASING_GEO     套管 	TGA
    T_LP_APPENDANT_GEO 	    附属物 	XXX     T_LP_ADDTLYR_GEO    附加保护层 	FSH
    T_GE_UNDROBSTACLE_GEO   地下障碍物 	GEA     T_GE_ROAD_GEO 	    公路 	GED
    T_GE_RAILWAY_GEO 	    铁路 	GET     T_GE_OTHPIPEPNT_GEO 第三方管线位置 GES
    T_GE_HPOLYGON_GEO 	    面状水系 	XXX     T_GE_HLINE_GEO 	    线状水系 	GEH
    T_GE_GEOHAZARD_GEO 	    地质灾害 	GEZ     T_GE_EMI_GEO 	    电流干扰 	GEG
    T_GE_BUILDING_GEO 	    建筑物 	GEJ     T_CP_TESTTRUNK_GEO  测试桩 	CSA
    T_CP_SANODE_GEO 	    牺牲阳极 	XYA     T_CP_RSANODE_GEO    带状牺牲阳极 	XYA
    T_CP_FLEXANODE_GEO 	    柔性阳极 	RYA     T_CP_DRNGDEVICE_GEO 排流装置 	PLA
    T_CP_CPPOWER_GEO  阴保站（阴保电源） 	YBD     T_CP_ANODEBED_GEO   阳极地床 	YDA
    T_BS_GROUNDMARK_GEO     地面标示物 	BSA     T_BS_ELECMARK_GEO   电子标识器 	DBA

    当前数据处理时，需要依据查询到的资料对特征编码值不正确的编码进行修改，待后期对自动编码功能进行完善
    
    基本思路：
    首先判断管段编码是否正确，如果出错则不填写；
    然后利用字典的健与值的关系来保证编码不重复；
    '''
    notCodingTuple=("T_PN_SOURCE_GEO","T_PN_STATION_GEO","T_PN_PIPESEGMENT_GEO")
    tempDictionary={}
    if feature not in notCodingTuple:
        with arcpy.da.UpdateCursor(feature,("PSCODE","CODE")) as cursor:
            for row in cursor:
                try:
                    tempValue=0
                    if row[0] is not None and len(row[0])==14 and re.search(r'\d{6}GB\d{6}',row[0]):
                            key=row[0]+featureClassCodeDictionary[feature]
                            if tempDictionary.has_key(key):
                                tempValue=tempDictionary[key]
                                row[1]=key + str(tempValue+1).zfill(3)
                                tempDictionary[key]=tempValue+1
                                cursor.updateRow(row)
                            else:
                                tempDictionary[key]=1
                                row[1]=key + str(tempValue+1).zfill(3)
                                cursor.updateRow(row)
                except Exception, e:
                    print e.message
                    pass
                continue
            
#定义一个特殊字段填充的函数
def fieldsFill(feature):
    '''
    本方法利用已完成的管段表信息，在对要素进行管段匹配之后，进行属性的填充，这些属性包括：投用日期、设计单位、
      施工单位、监理单位、检测单位，竣工图纸及编号、采集日期、采集单位、录入日期、管线名称、管段名称、管径等
    基本思路：
    首先获取管段表属性；
    然后获取要素表属性列表，如果需要填充的字段在属性列表中，则依据管段表的数据填充该字段
    特别注意的是管径需要采用管段管径的DN值，部分表格中只需要填充入口直径和壁厚
    '''
    #设定直径与DN值之间的健-值关系
    DiameterDNDic={"14.0":10,"17.0":10,"17.2":10,"18.0":15,"20.0":15,"21.3":15,"22.0":15,"25.0":20,"26.9":20,\
                   "32.0":25,"33.7":25,"34.0":25,"38.0":32,"40.0":32,"42":32,"42.4":32,"45.0":40,"48.0":40,\
                   "48.4":40,"50.0":40,"57.0":50,"60.0":50,"60.3":50,"63.0":50,"73.0":65,"75.0":65,"76.0":65,\
                   "76.1":65,"88.9":80,"89.0":80,"90.0":80,"108.0":100,"110.0":100,"114.0":100,"114.3":100,\
                   "125.0":125,"133.0":125,"140.0":125,"159.0":150,"160.0":150,"168.0":150,"168.3":150,\
                   "180.0":150,"200.0":200,"219.0":200,"219.1":200,"225.0":200,"250.0":250,"273.0":250,\
                   "280.0":250,"315.0":300,"323.9":300,"325.0":300,"355.0":350,"355.6":350,"377.0":350,\
                   "400.0":400,"406.4":400,"426.0":400,"450.0":450,"457.0":450,"480.0":450,"500.0":500,\
                   "508.0":500,"530.0":500,"560.0":500,"610.0":600,"630.0":600,"710.0":700,"711.0":700,\
                   "720.0":700,"800.0":800,"813.0":800,"820.0":800,"900.0":900,"914.0":900,"920.0":900,\
                   "1000.0":1000,"1016.0":1000,"1020.0":1000,"1200.0":1000}
    #定义一个不填充的要素类的元组
    doNotFillTableTuple=("T_PN_PIPESEGMENT_GEO","T_PN_STATION_GEO","T_PN_SOURCE_GEO")
    #定义一个通用的填充属性字段元组
    fillGeneralFieldTuple=("CODE","PIPENAME","PIPESEGNAME","PIPESEGNO","USEDDATE","DESIGNDEPNAME","CONSTRUNIT",\
                          "SUPERVISORUNIT","TESTUNIT","FDNAME","COLLECTDATE","COLLECTUNIT","INPUTDATETIME")
    #定义一个需要填充的管径字段列表
    fillDiameterTuple=("INDIAMETER","OUTDIAMETER","DIAMETER","MAINPIPEDIAMETER","MAINDIAMETER")

    fillThicknessTuple=("INTHICKNESS","OUTTHICKNESS","THICKNESS","MAINTHICKNESS")
    
    pipeSegmentdataFieldTuple=("OBJECTID","CODE","PIPENAME","NAME","USEDDATE","DESIGNDEPNAME",\
                              "CONSTRUNIT","SUPERVISORUNIT","TESTUNIT","FDNAME","COLLECTDATE",\
                              "COLLECTUNIT","INPUTDATETIME","DIAMETER","THICKNESS")
    
    fieldsSequenceDic={"OBJECTID":0,"CODE":1,"PIPENAME":2,"NAME":3,"USEDDATE":4,"DESIGNDEPNAME":5,\
                              "CONSTRUNIT":6,"SUPERVISORUNIT":7,"TESTUNIT":8,"FDNAME":9,"COLLECTDATE":10,\
                              "COLLECTUNIT":11,"INPUTDATETIME":12,"DIAMETER":13,"THICKNESS":14}
    #获取管段管径数据数据
    PipeSegmentDataList=[]
    with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",pipeSegmentdataFieldTuple) as PPcursor:
        for PC in PPcursor:
            if PC[0] is not None and str(PC[0]).strip()!="":
                PipeSegmentDataList.append([PC[0],PC[1],PC[2],PC[3],PC[4],PC[5],PC[6],\
                                            PC[7],PC[8],PC[9],PC[10],PC[11],PC[12],PC[13],PC[14]])

    
    fieldList=[]
    fieldNameList=[]
    if feature not in doNotFillTableTuple:
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
                                        if row[0]==PLS[1] and PLS[fieldsSequenceDic[FGFT]] is not None and row[1] is None:
                                            row[1]=PLS[fieldsSequenceDic[FGFT]]
                                            cursor.updateRow(row)
                                    else:
                                        if row[0]==PLS[1] and PLS[fieldsSequenceDic["NAME"]] is not None and row[1] is None:
                                            row[1]=PLS[fieldsSequenceDic["NAME"]]
                                            cursor.updateRow(row)
                                    
                except Exception, e:
                    print e.message
                    pass
                continue
                
        #填充管径，主要思路与一般要素填充一致，只是在填充时各要素的管径采用管段管径的DN值（对于异径管和刚塑转换接头，出口直径不填）
        for FDT in fillDiameterTuple:
            if FDT in fieldNameList:
                try:
                    with arcpy.da.UpdateCursor(feature,("PSCODE",FDT)) as cursor:
                        for row in cursor:
                            if row[0] is not None:
                                for PLS in PipeSegmentDataList:
                                    if FDT!="OUTDIAMETER":
                                        if row[0]==PLS[1] and PLS[fieldsSequenceDic["DIAMETER"]] is not None\
                                           and row[1] is None:
                                            row[1]=float(DiameterDNDic[str(round(float(PLS[fieldsSequenceDic\
                                                                                           ["DIAMETER"]]),1))])
                                            cursor.updateRow(row)
                                    else:
                                        if feature!="T_PN_REDUCER_GEO" and  feature!="T_PN_SPE_GEO":
                                            if row[0]==PLS[1] and PLS[fieldsSequenceDic["DIAMETER"]] is not None\
                                               and row[1] is None:
                                                row[1]=float(DiameterDNDic[str(round(float(PLS[fieldsSequenceDic\
                                                                                               ["DIAMETER"]]),1))])
                                                cursor.updateRow(row)
                                        
                except Exception, e:
                    print "错误信息：",e.message,
                    pass
                continue
        #填充壁厚，思路与管径填写一致（对于异径管和刚塑转换接头，出口壁厚不填）
        for FTT in fillThicknessTuple:
            if FTT in fieldNameList:
                try:
                    with arcpy.da.UpdateCursor(feature,("PSCODE",FTT)) as cursor:
                        for row in cursor:
                            if row[0] is not None:
                                for PLS in PipeSegmentDataList:
                                    if FDT!="OUTTHICKNESS":
                                        if row[0]==PLS[1] and PLS[fieldsSequenceDic["THICKNESS"]] is not None\
                                           and row[1] is None:
                                            row[1]=PLS[fieldsSequenceDic["THICKNESS"]]
                                            cursor.updateRow(row)
                                    else:
                                        if feature!="T_PN_REDUCER_GEO" and  feature!="T_PN_SPE_GEO":
                                            if row[0]==PLS[1] and PLS[fieldsSequenceDic["THICKNESS"]] is not None\
                                               and row[1] is None:
                                                row[1]=PLS[fieldsSequenceDic["THICKNESS"]]
                                                cursor.updateRow(row)
                except Exception, e:
                    print "错误信息：",e.message,
                    pass
                continue
def deleteIdentical(feature):
    """
    定义一个删除要素类中重复要素的函数,
    基本思路：
    利用arcgis的DeleteIdentical_management函数删除几何重复的要素，主要针对弯头，三通这样的要素
    """
    arcpy.DeleteIdentical_management(feature,"Shape")
