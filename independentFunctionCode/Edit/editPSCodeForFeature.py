# -*- coding: cp936 -*-
import arcpy

# ���ù����ռ�
workSpace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"
arcpy.env.workspace=workSpace

#��ȡ���ߵ���Ҫ�ؼ��е�����Ҫ����
featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")

#����һ��Ҫ���ļ����ͱ�Ƶ��ֵ�
featureClassAliasDictionary={
"T_BS_ELECMARK_GEO":"���ӱ�ʶ��","T_BS_GROUNDMARK_GEO":"�����ʾ��","T_CP_ANODEBED_GEO":"�����ش�",\
"T_CP_CPPOWER_GEO":"����վ��������Դ��","T_CP_DRNGDEVICE_GEO":"����װ��","T_CP_FLEXANODE_GEO":"��������",\
"T_CP_RSANODE_GEO":"��״��������","T_CP_SANODE_GEO":"��������","T_CP_TESTTRUNK_GEO":"����׮",\
"T_GE_BUILDING_GEO":"������","T_GE_EMI_GEO":"��������","T_GE_GEOHAZARD_GEO":"�����ֺ�","T_GE_HLINE_GEO":"��״ˮϵ",\
"T_GE_HPOLYGON_GEO":"��״ˮϵ","T_GE_OTHPIPEPNT_GEO":"����������λ��","T_GE_RAILWAY_GEO":"��·","T_GE_ROAD_GEO":"��·",\
"T_GE_UNDROBSTACLE_GEO":"�����ϰ���","T_LP_ADDTLYR_GEO":"���ӱ�����","T_LP_APPENDANT_GEO":"������",\
"T_LP_CASING_GEO":"�׹�","T_LP_CONDENSER_GEO":"��ˮ��","T_LP_GASCROSS_GEO":"����Խ","T_LP_HYDRPROTECT_GEO":"ˮ������",\
"T_LP_OPTICALHOLE_GEO":"�������ֿ�","T_LP_TUNNEL_GEO":"���","T_PN_BELLOW_GEO":"���ƹ�","T_PN_BLOCK_GEO":"�����",\
"T_PN_ELBOW_GEO":"��ͷ","T_PN_IJOINT_GEO":"��Ե��ͷ","T_PN_PEPIPEWELD_GEO":"PE�ܺ���","T_PN_PIPERISER_GEO":"����",\
"T_PN_PRYCABINET_GEO":"��װ��","T_PN_REDUCER_GEO":"�쾶��","T_PN_REGULATOR_GEO":"��ѹ��",\
"T_PN_SEAMCUT_GEO":"��������Ͳ���","T_PN_SOURCE_GEO":"��Դ","T_PN_SPE_GEO":"����ת����ͷ","T_PN_STATION_GEO":"��վ",\
"T_PN_TAPPING_GEO":"����","T_PN_THREEORFOUR_GEO":"��ͨ��ͨ","T_PN_VALVE_GEO":"����","T_PN_VALVEPIT_GEO":"��������",
"T_PN_PIPESEGMENT_GEO":"�ܶ�"
}

def fieldisIn(fc,fd):
    #�ж��ֶ��Ƿ���Ҫ�ر���
    fieldList = []
    for f in arcpy.ListFields(fc):
        fieldList.append(str(f.name))
    if fd in fieldList:
        return True
    else:
        return False

        

def PPCodeFill(feature):
    #������ЩҪ�ز���Ҫ�Զ����ܶα���
    notFillPSCODEFeatureTuple=("T_PN_PIPESEGMENT_GEO","T_PN_STATION_GEO","T_PN_SOURCE_GEO",\
                               "T_LP_GASCROSS_GEO","T_LP_CASING_GEO","T_PN_THREEORFOUR_GEO")
    #����ֱ���͹���ֱ���Ķ�Ӧ��ϵ
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
        #����һ����Ҫ���Ĺܾ��ֶ��б�
    fillDiameterTuple=("INDIAMETER","OUTDIAMETER")

    fillThicknessTuple=("INTHICKNESS","OUTTHICKNESS")
    
    if feature not in notFillPSCODEFeatureTuple:
        try:
            if arcpy.Exists("{}SpatialJoinClass".format(feature)):
                arcpy.Delete_management("{}SpatialJoinClass".format(feature))
            if arcpy.Exists("{}SpatialJoinOTOClass".format(feature)):
                arcpy.Delete_management("{}SpatialJoinOTOClass".format(feature))
                
            if int(arcpy.GetCount_management(feature).getOutput(0))!=0:
                #ɾ���ظ�Ҫ��
                arcpy.DeleteIdentical_management(feature,"Shape")
                if not fieldisIn(feature,"OBJECTIDCOPY"):
                    #���һ���ֶ����ڸ���Ҫ�ص�OBJECTID
                    arcpy.AddField_management(feature,"OBJECTIDCOPY","TEXT")
                # ��Ŀ����е�OBJECTID�ֶμ��㵽�豸�����
                arcpy.CalculateField_management(feature,"OBJECTIDCOPY","!OBJECTID!","PYTHON")

                # ��Ҫ����ܶα���пռ����ӣ����ӷ�ʽ�ý���һ��һ
                arcpy.SpatialJoin_analysis(feature,"T_PN_PIPESEGMENT_GEO","{}SpatialJoinOTOClass".format(feature),\
                                            "JOIN_ONE_TO_ONE","","","INTERSECT","","")
                # ��Ҫ����ܶα���пռ����ӣ����ӷ�ʽ�ý���һ�Զ�
                arcpy.SpatialJoin_analysis(feature,"T_PN_PIPESEGMENT_GEO","{}SpatialJoinClass".format(feature),\
                                            "JOIN_ONE_TO_MANY","","","INTERSECT","","")
                #�����йܶ���Ϣ������  #Join_Count
                FPPDatalist=[]
                with arcpy.da.SearchCursor("{}SpatialJoinOTOClass".format(feature),("OBJECTIDCOPY","Join_Count")) as TFCuosor:
                    for TOFrow in TFCuosor:
                        with arcpy.da.SearchCursor("{}SpatialJoinClass".format(feature),("OBJECTIDCOPY","JOIN_FID","CODE_1","DIAMETER","THICKNESS")) as TFCuosor:
                            for TFrow in TFCuosor:
                                if TOFrow[0]==TFrow[0]:
                                    FPPDatalist.append([TFrow[0],TFrow[1],TFrow[2],TFrow[3],TFrow[4],TOFrow[1]])
                #��ȡ�ܶ���Ϣ���б�
                PPDataList=[]
                with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("OBJECTID","SHAPE@")) as Pcursor:
                    for Prow in Pcursor:
                        PPDataList.append([Prow[0],Prow[1]])

                #�༭�йܾ�Ҫ�صĹܶα���͹ܾ���Ϣ       
                if fieldisIn(feature,"INDIAMETER") and fieldisIn(feature,"INTHICKNESS") and \
                   fieldisIn(feature,"OUTDIAMETER") and fieldisIn(feature,"OUTTHICKNESS"): 
                    with arcpy.da.UpdateCursor(feature,\
                                   ("OBJECTIDCOPY","PSCODE","SHAPE@X","SHAPE@Y",\
                                    "INDIAMETER","INTHICKNESS","OUTDIAMETER","OUTTHICKNESS")) as Fcursor:
                        for Frow in Fcursor:
                            try:
                                for PPD in PPDataList:
                                    for FPPD in FPPDatalist:
                                        #�豸��OBJECT��������OBJECT��ͬ�����ҹܶε�OBJECT��������е������豸OBJECT��ͬʱ�������豸��ʩ�������ж�
                                        if Frow[0]==FPPD[0] and PPD[0]==FPPD[1]:
                                            #���ֻ��һ�������豸��ʩ����
                                            if FPPD[5]==1:
                                                #����豸��������ܶε��յ�����һ�£���ô�豸�Ĺܶα�����ǹܶεı��룬���ֱ���ͱں��ͨ���ܶ���Ϣ¼��
                                                if abs(Frow[2]-PPD[1].lastPoint.X)<1e-10 and abs(Frow[3]-PPD[1].lastPoint.Y)<1e-10:
                                                    Frow[1]=FPPD[2]
                                                    if FPPD[3] is not None:
                                                        Frow[4]=DiameterDNDic[str(FPPD[3])]
                                                    if FPPD[4] is not None:
                                                        Frow[5]=FPPD[4]      
                                                #����豸��������ܶε����һ�£���ô�豸�ĳ���ֱ���ͱں����ݹܶ���Ϣ��д
                                                if abs(Frow[2]-PPD[1].firstPoint.X)<1e-10 and abs(Frow[3]-PPD[1].firstPoint.Y)<1e-10:
                                                    if FPPD[3] is not None:
                                                        Frow[6]=DiameterDNDic[str(FPPD[3])]
                                                    if FPPD[4] is not None:
                                                        Frow[7]=FPPD[4]
                                                #����豸λ�ڹܶε��м䣬��ô�豸�Ĺܶα�����ǹܶεı��룬�豸�����/����ֱ���ͱں����ݹܶ���Ϣ��д
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
                #ר����Է������ҽ����ж�        
                elif feature == "T_PN_VALVEPIT_GEO":
                    with arcpy.da.UpdateCursor(feature,("OBJECTIDCOPY","PSCODE","SHAPE@X","SHAPE@Y")) as Fcursor:
                        for Frow in Fcursor:
                            try:
                                for PPD in PPDataList:
                                    for FPPD in FPPDatalist:
                                        #�豸��OBJECT��������OBJECT��ͬ�����ҹܶε�OBJECT��������е������豸OBJECT��ͬʱ�������豸��ʩ�������ж�
                                        if Frow[0]==FPPD[0] and PPD[0]==FPPD[1]:
                                            #����豸��������ܶε��յ�����һ�£���ô�豸�Ĺܶα�����ǹܶεı��룬���ֱ���ͱں��ͨ���ܶ���Ϣ¼��
                                            if abs(Frow[2]-PPD[1].lastPoint.X)<1e-10 and abs(Frow[3]-PPD[1].lastPoint.Y)<1e-10:
                                                Frow[1]=FPPD[2]
                                            #����豸λ�ڹܶε��м䣬��ô�豸�Ĺܶα�����ǹܶεı��룬�豸�����/����ֱ���ͱں����ݹܶ���Ϣ��д
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
                #�����޳����ֱ����ͬʱ��Ϊ�������ҵ�Ҫ�أ�ֱ���ÿռ����ӣ�Ȼ����������������ܶεı�����Ϊ�ܶα���
                else:
                    # ��Ҫ�ر���ռ����Ӻ���м�����ͨ��OBJECTID�����������ӣ�
                    arcpy.JoinField_management(feature,"OBJECTIDCOPY","{}SpatialJoinClass".format(feature),"OBJECTIDCOPY","CODE_1")
                    # ���������Ӻ���ֶμ����Ҫ�صĹܶα���
                    arcpy.CalculateField_management(feature,"PSCODE","!CODE_1!","PYTHON")
                    # ɾ�������Ƕ������ʱ�ֶ�
                    arcpy.DeleteField_management(feature,["CODE_1"])
                #ɾ���������ʱ�ֶ�
                arcpy.DeleteField_management(feature,["OBJECTIDCOPY"])
                # ɾ���м��ļ�
                arcpy.Delete_management("{}SpatialJoinClass".format(feature))
                arcpy.Delete_management("{}SpatialJoinOTOClass".format(feature))
        except Exception,e:
            print e.message
            pass
#for FC in featureClassList:
    #print featureClassAliasDictionary[FC]
PPCodeFill("T_PN_VALVEPIT_GEO")



    
        
    
