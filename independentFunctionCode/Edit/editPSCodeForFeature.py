# -*- coding: cp936 -*-
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

def fieldisIn(fc,fd):
    #判断字段是否在要素表中
    fieldList = []
    for f in arcpy.ListFields(fc):
        fieldList.append(str(f.name))
    if fd in fieldList:
        return True
    else:
        return False

        

def PPCodeFill(feature):
    #下面这些要素不需要自动填充管段编码
    notFillPSCODEFeatureTuple=("T_PN_PIPESEGMENT_GEO","T_PN_STATION_GEO","T_PN_SOURCE_GEO",\
                               "T_LP_GASCROSS_GEO","T_LP_CASING_GEO","T_PN_THREEORFOUR_GEO")
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
        #定义一个需要填充的管径字段列表
    fillDiameterTuple=("INDIAMETER","OUTDIAMETER")

    fillThicknessTuple=("INTHICKNESS","OUTTHICKNESS")
    
    if feature not in notFillPSCODEFeatureTuple:
        try:
            if arcpy.Exists("{}SpatialJoinClass".format(feature)):
                arcpy.Delete_management("{}SpatialJoinClass".format(feature))
            if arcpy.Exists("{}SpatialJoinOTOClass".format(feature)):
                arcpy.Delete_management("{}SpatialJoinOTOClass".format(feature))
                
            if int(arcpy.GetCount_management(feature).getOutput(0))!=0:
                #删除重复要素
                arcpy.DeleteIdentical_management(feature,"Shape")
                if not fieldisIn(feature,"OBJECTIDCOPY"):
                    #添加一个字段用于复制要素的OBJECTID
                    arcpy.AddField_management(feature,"OBJECTIDCOPY","TEXT")
                # 将目标表中的OBJECTID字段计算到设备编号中
                arcpy.CalculateField_management(feature,"OBJECTIDCOPY","!OBJECTID!","PYTHON")

                # 将要素与管段表进行空间连接，连接方式用交叉一对一
                arcpy.SpatialJoin_analysis(feature,"T_PN_PIPESEGMENT_GEO","{}SpatialJoinOTOClass".format(feature),\
                                            "JOIN_ONE_TO_ONE","","","INTERSECT","","")
                # 将要素与管段表进行空间连接，连接方式用交叉一对多
                arcpy.SpatialJoin_analysis(feature,"T_PN_PIPESEGMENT_GEO","{}SpatialJoinClass".format(feature),\
                                            "JOIN_ONE_TO_MANY","","","INTERSECT","","")
                #将带有管段信息的数据  #Join_Count
                FPPDatalist=[]
                with arcpy.da.SearchCursor("{}SpatialJoinOTOClass".format(feature),("OBJECTIDCOPY","Join_Count")) as TFCuosor:
                    for TOFrow in TFCuosor:
                        with arcpy.da.SearchCursor("{}SpatialJoinClass".format(feature),("OBJECTIDCOPY","JOIN_FID","CODE_1","DIAMETER","THICKNESS")) as TFCuosor:
                            for TFrow in TFCuosor:
                                if TOFrow[0]==TFrow[0]:
                                    FPPDatalist.append([TFrow[0],TFrow[1],TFrow[2],TFrow[3],TFrow[4],TOFrow[1]])
                #获取管段信息至列表
                PPDataList=[]
                with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("OBJECTID","SHAPE@")) as Pcursor:
                    for Prow in Pcursor:
                        PPDataList.append([Prow[0],Prow[1]])

                #编辑有管径要素的管段编码和管径信息       
                if fieldisIn(feature,"INDIAMETER") and fieldisIn(feature,"INTHICKNESS") and \
                   fieldisIn(feature,"OUTDIAMETER") and fieldisIn(feature,"OUTTHICKNESS"): 
                    with arcpy.da.UpdateCursor(feature,\
                                   ("OBJECTIDCOPY","PSCODE","SHAPE@X","SHAPE@Y",\
                                    "INDIAMETER","INTHICKNESS","OUTDIAMETER","OUTTHICKNESS")) as Fcursor:
                        for Frow in Fcursor:
                            try:
                                for PPD in PPDataList:
                                    for FPPD in FPPDatalist:
                                        #设备的OBJECT与关联表的OBJECT相同，并且管段的OBJECT与关联表中的连接设备OBJECT相同时，进行设备设施归属的判断
                                        if Frow[0]==FPPD[0] and PPD[0]==FPPD[1]:
                                            #如果只有一条线与设备设施关联
                                            if FPPD[5]==1:
                                                #如果设备的坐标与管段的终点坐标一致，那么设备的管段编码就是管段的编码，入口直径和壁厚就通过管段信息录入
                                                if abs(Frow[2]-PPD[1].lastPoint.X)<1e-10 and abs(Frow[3]-PPD[1].lastPoint.Y)<1e-10:
                                                    Frow[1]=FPPD[2]
                                                    if FPPD[3] is not None:
                                                        Frow[4]=DiameterDNDic[str(FPPD[3])]
                                                    if FPPD[4] is not None:
                                                        Frow[5]=FPPD[4]      
                                                #如果设备的坐标与管段的起点一致，那么设备的出口直径和壁厚，依据管段信息填写
                                                if abs(Frow[2]-PPD[1].firstPoint.X)<1e-10 and abs(Frow[3]-PPD[1].firstPoint.Y)<1e-10:
                                                    if FPPD[3] is not None:
                                                        Frow[6]=DiameterDNDic[str(FPPD[3])]
                                                    if FPPD[4] is not None:
                                                        Frow[7]=FPPD[4]
                                                #如果设备位于管段的中间，那么设备的管段编码就是管段的编码，设备的入口/出口直径和壁厚，依据管段信息填写
                                                else:
                                                    Frow[1]=FPPD[2]
                                                    if FPPD[3] is not None:
                                                        Frow[4]=DiameterDNDic[str(FPPD[3])]
                                                        Frow[6]=DiameterDNDic[str(FPPD[3])]
                                                    if FPPD[4] is not None:
                                                        Frow[5]=FPPD[4]
                                                        Frow[7]=FPPD[4]
                                            elif FPPD[5]==2:
                                                if abs(Frow[2]-PPD[1].lastPoint.X)<1e-10 and abs(Frow[3]-PPD[1].lastPoint.Y)<1e-10:
                                                    Frow[1]=FPPD[2] 
                                                    if FPPD[3] is not None:
                                                        Frow[4]=DiameterDNDic[str(FPPD[3])]
                                                    if FPPD[4] is not None:
                                                        Frow[5]=FPPD[4]
                                                if abs(Frow[2]-PPD[1].firstPoint.X)<1e-10 and abs(Frow[3]-PPD[1].firstPoint.Y)<1e-10:
                                                    if FPPD[3] is not None:
                                                        Frow[6]=DiameterDNDic[str(FPPD[3])]
                                                    if FPPD[4] is not None:
                                                        Frow[7]=FPPD[4]
                                                if (not (abs(Frow[2]-PPD[1].lastPoint.X)<1e-10 and abs(Frow[3]-PPD[1].lastPoint.Y)<1e-10)) and \
                                                   (not (abs(Frow[2]-PPD[1].firstPoint.X)<1e-10 and abs(Frow[3]-PPD[1].firstPoint.Y)<1e-10)):
                                                    Frow[1]=FPPD[2]
                                                    if FPPD[3] is not None:
                                                        Frow[4]=DiameterDNDic[str(FPPD[3])]
                                                        Frow[6]=DiameterDNDic[str(FPPD[3])]
                                                    if FPPD[4] is not None:
                                                        Frow[5]=FPPD[4]
                                                        Frow[7]=FPPD[4]
                                            elif FPPD[5]==3:
                                                if abs(Frow[2]-PPD[1].lastPoint.X)<1e-10 and abs(Frow[3]-PPD[1].lastPoint.Y)<1e-10:
                                                    Frow[1]=FPPD[2]
                                                    if FPPD[3] is not None:
                                                        Frow[4]=DiameterDNDic[str(FPPD[3])]
                                                    if FPPD[4] is not None:
                                                        Frow[5]=FPPD[4]
                                            else:
                                                pass
                                            Fcursor.updateRow(Frow)
                            except Exception,e:
                                print e.message
                                pass
                            continue
                #专门针对阀井阀室进行判断        
                elif feature == "T_PN_VALVEPIT_GEO":
                    with arcpy.da.UpdateCursor(feature,("OBJECTIDCOPY","PSCODE","SHAPE@X","SHAPE@Y")) as Fcursor:
                        for Frow in Fcursor:
                            try:
                                for PPD in PPDataList:
                                    for FPPD in FPPDatalist:
                                        #设备的OBJECT与关联表的OBJECT相同，并且管段的OBJECT与关联表中的连接设备OBJECT相同时，进行设备设施归属的判断
                                        if Frow[0]==FPPD[0] and PPD[0]==FPPD[1]:
                                            #如果设备的坐标与管段的终点坐标一致，那么设备的管段编码就是管段的编码，入口直径和壁厚就通过管段信息录入
                                            if abs(Frow[2]-PPD[1].lastPoint.X)<1e-10 and abs(Frow[3]-PPD[1].lastPoint.Y)<1e-10:
                                                Frow[1]=FPPD[2]
                                            #如果设备位于管段的中间，那么设备的管段编码就是管段的编码，设备的入口/出口直径和壁厚，依据管段信息填写
                                            if not (abs(Frow[2]-PPD[1].lastPoint.X)<1e-10 and abs(Frow[3]-PPD[1].lastPoint.Y)<1e-10) \
                                               and \
                                               not (abs(Frow[2]-PPD[1].firstPoint.X)<1e-10 and abs(Frow[3]-PPD[1].firstPoint.Y)<1e-10):
                                                Frow[1]=FPPD[2]
                                            if abs(Frow[2]-PPD[1].firstPoint.X)<1e-10 and abs(Frow[3]-PPD[1].firstPoint.Y)<1e-10:
                                                pass
                                            Fcursor.updateRow(Frow)
                            except Exception,e:
                                print e.message
                                pass
                            continue
                #对于无出入口直径，同时不为阀井阀室的要素，直接用空间连接，然后用属性连接最近管段的编码作为管段编码
                else:
                    # 将要素表与空间连接后的中间标格按照通过OBJECTID进行属性连接，
                    arcpy.JoinField_management(feature,"OBJECTIDCOPY","{}SpatialJoinClass".format(feature),"OBJECTIDCOPY","CODE_1")
                    # 将属性连接后的字段计算成要素的管段编码
                    arcpy.CalculateField_management(feature,"PSCODE","!CODE_1!","PYTHON")
                    # 删除连接是多出的临时字段
                    arcpy.DeleteField_management(feature,["CODE_1"])
                #删除多出的临时字段
                arcpy.DeleteField_management(feature,["OBJECTIDCOPY"])
                # 删除中间文件
                arcpy.Delete_management("{}SpatialJoinClass".format(feature))
                arcpy.Delete_management("{}SpatialJoinOTOClass".format(feature))
        except Exception,e:
            print e.message
            pass
#for FC in featureClassList:
    #print featureClassAliasDictionary[FC]
PPCodeFill("T_PN_VALVEPIT_GEO")



    
        
    
