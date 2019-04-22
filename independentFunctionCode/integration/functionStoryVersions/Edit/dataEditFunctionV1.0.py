# -*- coding: cp936 -*-
import arcpy
import re

#����һ��Ҫ���ļ����ͱ�Ƶ��ֵ�
featureClassAliasDictionary={"T_BS_ELECMARK_GEO":"���ӱ�ʶ��","T_BS_GROUNDMARK_GEO":"�����ʾ��","T_CP_ANODEBED_GEO":"�����ش�",\
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
                             "T_PN_PIPESEGMENT_GEO":"�ܶ�"}
#����ÿһ��ͼ���Ŀ���ַ��ֵ�
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
#�ܶα�����д����
def PPCodeFill(feature):
    """
    �˺������ÿռ����ӵķ�ʽ�����豸��ʩ���еĹܶα����ֶν�����д��
    ���У��ܶα�վ������Դ��Ϊ����������д��
    ����Խ����׹ܱ�һ���ڹܶλ�����ɺ�ֱ�ӽ�����Խ�ܶν��и��ƣ���˲���Ҫ��䣻
    ����˼·��
    ���ȣ�����Ҫ���ܶα����Ҫ����OBJECTID�ֶν��и��Ƴ��������пռ���������Թ�����֤Ҫ�صĶ�Ӧ�ԣ���
    Ȼ�����ÿռ����ӣ��ҵ���Ҫ������ĹܶΣ�
    Ȼ�����ò����OBJECTID���ռ����Ӻ�ı���Ҫ�ر�����������ӣ�
    Ȼ�󣬽��ܶα����ֶμ��㵽Ŀ��Ҫ�ر��У�
    ���ɾ�������м䴫�����ݵ����ݱ�
    """
    #������ЩҪ�ز���Ҫ�Զ����ܶα���
    notFillPSCODEFeatureTuple=("T_PN_PIPESEGMENT_GEO","T_PN_STATION_GEO","T_PN_SOURCE_GEO",\
                               "T_LP_GASCROSS_GEO","T_LP_CASING_GEO")
    if feature not in notFillPSCODEFeatureTuple:
        try:
            arcpy.Delete_management("{}SpatialJoinClass".format(feature))
            if int(arcpy.GetCount_management(feature).getOutput(0))!=0:
                #���һ���ֶ����ڸ���Ҫ�ص�OBJECTID
                arcpy.AddField_management(feature,"OBJECTIDCOPY","TEXT")
                # ��Ŀ����е�OBJECTID�ֶμ��㵽�豸�����
                arcpy.CalculateField_management(feature,"OBJECTIDCOPY","!OBJECTID!","PYTHON")
                # ��Ҫ����ܶα���пռ����ӣ����ӷ�ʽ�����
                arcpy.SpatialJoin_analysis(feature,"T_PN_PIPESEGMENT_GEO","{}SpatialJoinClass".format(feature),\
                                            "","","","CLOSEST","","")
                # ��Ҫ�ر���ռ����Ӻ���м�����ͨ��OBJECTID�����������ӣ�
                arcpy.JoinField_management(feature,"OBJECTIDCOPY","{}SpatialJoinClass".format(feature),"OBJECTIDCOPY","CODE_1")
                # ���������Ӻ���ֶμ����Ҫ�صĹܶα���
                arcpy.CalculateField_management(feature,"PSCODE","!CODE_1!","PYTHON")
                # ɾ�������Ƕ������ʱ�ֶ�
                arcpy.DeleteField_management(feature,["CODE_1","OBJECTIDCOPY"])
                # ɾ���м��ļ�
                arcpy.Delete_management("{}SpatialJoinClass".format(feature))
        except Exception,e:
            print e.message
            pass

#������亯��
def coordinateFill(feature):
    '''
    ���������ڶ�Ҫ�ص�����ֵ������д��
    �ڹܶα�����д��ɲ���ȷ������£���д��Ҫ�ص�����ֵ��
    ��дҪ������ֵ֮ǰ����ȷ����������ϵΪ���2000����ϵ;
    
    ���ڵ�״Ҫ����д��XY;
    ������״Ҫ����д����ֹ���XY����д֮ǰһ��ȷ�����͵ķ�����ȷ;
    ����վ������Դ���ܶβ�������XY���ꣻ
    ���ڵ������ܵ�����ַ�ֺ��͵������ţ�����Ϊ��״Ҫ�أ����ֶ���Ϊ��״���ͣ������㣻

    ����˼·��
    ��д֮ǰ��Ҫ�жϴ������Ҫ���ǵ�״Ҫ�ػ�����״Ҫ�أ�
        ����ǵ�״Ҫ�أ�
        �������"SHAPE@X","SHAPE@Y"��������ֱֵ�Ӹ�ֵ��Ҫ�ص�XY����
        �������״Ҫ�أ�
        �������伸�����Եĵ�һ����ļ������Ը�ֵ����㣬�ڶ�����ļ������Ը�ֵ���յ�
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

#����һ��Ҫ�ر���ĺ���
def featureCoding(feature):
    '''
    ���������ڶ��ѽ��йܶ�ƥ����豸��ʩ�����Զ����루���뱣֤���ظ����������տռ�˳�������򣩡�
    ÿһ��Ҫ�����ж�����һ��Ĭ�ϵ�������������(������Դ��վ���͹ܶβ����룬���������״ˮϵ����δ������XXX��ʾ)��
    T_PN_VALVEPIT_GEO 	    �������� 	FJA     T_PN_VALVE_GEO 	    ���� 	FMB
    T_PN_THREEORFOUR_GEO    ��ͨ��ͨ 	STA     T_PN_TAPPING_GEO    ���� 	KKA
    T_PN_STATION_GEO 	    ��վ 	Z       T_PN_SPE_GEO 	    ����ת����ͷ 	JTC
    T_PN_SOURCE_GEO 	    ��Դ 	Z       T_PN_SEAMCUT_GEO    ��������Ͳ��� HFA
    T_PN_REGULATOR_GEO     ��ѹ�� 	TYX     T_PN_REDUCER_GEO    �쾶�� 	YGA
    T_PN_PRYCABINET_GEO     ��װ�� 	TYG     T_PN_PIPESEGMENT_GEO�ܶ� 	GB
    T_PN_PIPERISER_GEO 	    ���� 	GDA     T_PN_PEPIPEWELD_GEO PE�ܺ��� 	HKA
    T_PN_IJOINT_GEO 	    ��Ե��ͷ 	JTB     T_PN_ELBOW_GEO 	    ��ͷ 	WGA
    T_PN_BLOCK_GEO 	    ����� 	FDA     T_PN_BELLOW_GEO     ���ƹ� 	BWA
    T_LP_TUNNEL_GEO 	    ��� 	FSI     T_LP_OPTICALHOLE_GEO�������ֿ� 	GKA
    T_LP_HYDRPROTECT_GEO    ˮ������ 	HPA     T_LP_GASCROSS_GEO   ����Խ 	PTA
    T_LP_CONDENSER_GEO 	    ��ˮ�� 	FSJ     T_LP_CASING_GEO     �׹� 	TGA
    T_LP_APPENDANT_GEO 	    ������ 	XXX     T_LP_ADDTLYR_GEO    ���ӱ����� 	FSH
    T_GE_UNDROBSTACLE_GEO   �����ϰ��� 	GEA     T_GE_ROAD_GEO 	    ��· 	GED
    T_GE_RAILWAY_GEO 	    ��· 	GET     T_GE_OTHPIPEPNT_GEO ����������λ�� GES
    T_GE_HPOLYGON_GEO 	    ��״ˮϵ 	XXX     T_GE_HLINE_GEO 	    ��״ˮϵ 	GEH
    T_GE_GEOHAZARD_GEO 	    �����ֺ� 	GEZ     T_GE_EMI_GEO 	    �������� 	GEG
    T_GE_BUILDING_GEO 	    ������ 	GEJ     T_CP_TESTTRUNK_GEO  ����׮ 	CSA
    T_CP_SANODE_GEO 	    �������� 	XYA     T_CP_RSANODE_GEO    ��״�������� 	XYA
    T_CP_FLEXANODE_GEO 	    �������� 	RYA     T_CP_DRNGDEVICE_GEO ����װ�� 	PLA
    T_CP_CPPOWER_GEO  ����վ��������Դ�� 	YBD     T_CP_ANODEBED_GEO   �����ش� 	YDA
    T_BS_GROUNDMARK_GEO     �����ʾ�� 	BSA     T_BS_ELECMARK_GEO   ���ӱ�ʶ�� 	DBA

    ��ǰ���ݴ���ʱ����Ҫ���ݲ�ѯ�������϶���������ֵ����ȷ�ı�������޸ģ������ڶ��Զ����빦�ܽ�������
    
    ����˼·��
    �����жϹܶα����Ƿ���ȷ�������������д��
    Ȼ�������ֵ�Ľ���ֵ�Ĺ�ϵ����֤���벻�ظ���
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
            
#����һ�������ֶ����ĺ���
def fieldsFill(feature):
    '''
    ��������������ɵĹܶα���Ϣ���ڶ�Ҫ�ؽ��йܶ�ƥ��֮�󣬽������Ե���䣬��Щ���԰�����Ͷ�����ڡ���Ƶ�λ��
      ʩ����λ������λ����ⵥλ������ͼֽ����š��ɼ����ڡ��ɼ���λ��¼�����ڡ��������ơ��ܶ����ơ��ܾ���
    ����˼·��
    ���Ȼ�ȡ�ܶα����ԣ�
    Ȼ���ȡҪ�ر������б������Ҫ�����ֶ��������б��У������ݹܶα�����������ֶ�
    �ر�ע����ǹܾ���Ҫ���ùܶιܾ���DNֵ�����ֱ����ֻ��Ҫ������ֱ���ͱں�
    '''
    #�趨ֱ����DNֵ֮��Ľ�-ֵ��ϵ
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
    #����һ��������Ҫ�����Ԫ��
    doNotFillTableTuple=("T_PN_PIPESEGMENT_GEO","T_PN_STATION_GEO","T_PN_SOURCE_GEO")
    #����һ��ͨ�õ���������ֶ�Ԫ��
    fillGeneralFieldTuple=("CODE","PIPENAME","PIPESEGNAME","PIPESEGNO","USEDDATE","DESIGNDEPNAME","CONSTRUNIT",\
                          "SUPERVISORUNIT","TESTUNIT","FDNAME","COLLECTDATE","COLLECTUNIT","INPUTDATETIME")
    #����һ����Ҫ���Ĺܾ��ֶ��б�
    fillDiameterTuple=("INDIAMETER","OUTDIAMETER","DIAMETER","MAINPIPEDIAMETER","MAINDIAMETER")

    fillThicknessTuple=("INTHICKNESS","OUTTHICKNESS","THICKNESS","MAINTHICKNESS")
    
    pipeSegmentdataFieldTuple=("OBJECTID","CODE","PIPENAME","NAME","USEDDATE","DESIGNDEPNAME",\
                              "CONSTRUNIT","SUPERVISORUNIT","TESTUNIT","FDNAME","COLLECTDATE",\
                              "COLLECTUNIT","INPUTDATETIME","DIAMETER","THICKNESS")
    
    fieldsSequenceDic={"OBJECTID":0,"CODE":1,"PIPENAME":2,"NAME":3,"USEDDATE":4,"DESIGNDEPNAME":5,\
                              "CONSTRUNIT":6,"SUPERVISORUNIT":7,"TESTUNIT":8,"FDNAME":9,"COLLECTDATE":10,\
                              "COLLECTUNIT":11,"INPUTDATETIME":12,"DIAMETER":13,"THICKNESS":14}
    #��ȡ�ܶιܾ���������
    PipeSegmentDataList=[]
    with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",pipeSegmentdataFieldTuple) as PPcursor:
        for PC in PPcursor:
            if PC[0] is not None and str(PC[0]).strip()!="":
                PipeSegmentDataList.append([PC[0],PC[1],PC[2],PC[3],PC[4],PC[5],PC[6],\
                                            PC[7],PC[8],PC[9],PC[10],PC[11],PC[12],PC[13],PC[14]])

    
    fieldList=[]
    fieldNameList=[]
    if feature not in doNotFillTableTuple:
        fieldList=arcpy.ListFields(feature)  #��ȡ�����ֶ��б�
        for FL in fieldList: #��ȡÿһ����������ֶ�����
            fieldNameList.append(FL.name)

        #����б���һ��Ҫ��,�����ֵ���е�ÿһ���ֶΣ�������ֶ���ĳһ��Ҫ�ر��У����ֶε�ֵΪ��ʱ�����ܶα�����д���Ӧ��Ҫ�ر���
        #    ���и�Ҫ����Ĺܶ������ֶβ�ͳһ���������֣�PIPESEGNAME��PIPESEGNO��
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
                
        #���ܾ�����Ҫ˼·��һ��Ҫ�����һ�£�ֻ�������ʱ��Ҫ�صĹܾ����ùܶιܾ���DNֵ�������쾶�ܺ͸���ת����ͷ������ֱ�����
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
                    print "������Ϣ��",e.message,
                    pass
                continue
        #���ں�˼·��ܾ���дһ�£������쾶�ܺ͸���ת����ͷ�����ڱں��
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
                    print "������Ϣ��",e.message,
                    pass
                continue
def deleteIdentical(feature):
    """
    ����һ��ɾ��Ҫ�������ظ�Ҫ�صĺ���,
    ����˼·��
    ����arcgis��DeleteIdentical_management����ɾ�������ظ���Ҫ�أ���Ҫ�����ͷ����ͨ������Ҫ��
    """
    arcpy.DeleteIdentical_management(feature,"Shape")
