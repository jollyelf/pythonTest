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
                # ɾ������ʱ�������ʱ�ֶ�
                arcpy.DeleteField_management(feature,["CODE_1","OBJECTIDCOPY"])
                # ɾ���м��ļ�
                arcpy.Delete_management("{}SpatialJoinClass".format(feature))
        except Exception,e:
            print featureClassCodeDictionary[feature],"�༭�ܶα���ʱ����������Ϣ��",e.message
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
                  "T_GE_OTHPIPEPNT_GEO","T_GE_EMI_GEO","T_GE_GEOHAZARD_GEO",\
                  "T_LP_GASCROSS_GEO","T_LP_CASING_GEO")
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
                            print featureClassCodeDictionary[feature],"�༭����ʱ����������Ϣ��",e.message
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
                            print featureClassCodeDictionary[feature],"�༭����ʱ����������Ϣ��",e.message
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
                    print featureClassCodeDictionary[feature],"�༭��������ʱ����������Ϣ��",e.message
                    pass
                continue
            
#����һ�������ֶ����ĺ���
def fieldsFill(feature):
    '''
    ��������������ɵĹܶα���Ϣ���ڶ�Ҫ�ؽ��йܶ�ƥ��֮�󣬽������Ե���䣬��Щ���԰�����Ͷ�����ڡ���Ƶ�λ��
      ʩ����λ������λ����ⵥλ������ͼֽ����š��ɼ����ڡ��ɼ���λ��¼�����ڡ��������ơ��ܶ����ơ��ܾ���
    ���Ȼ�ȡ�ܶα����ԣ�
    Ȼ���ȡҪ�ر������б������Ҫ�����ֶ��������б��У������ݹܶα�����������ֶ�
    �ر�ע����ǹܾ���Ҫ���ùܶιܾ���DNֵ�����ֱ����ֻ��Ҫ������ֱ���ͱں�
    '''
    doNotFillTableTuple=("T_PN_PIPESEGMENT_GEO","T_PN_STATION_GEO","T_PN_SOURCE_GEO","T_LP_GASCROSS_GEO","T_LP_CASING_GEO","T_PN_THREEORFOUR_GEO")
    #����һ��ͨ�õ���������ֶ�Ԫ��
    fillGeneralFieldTuple=("PIPENAME","PIPESEGNAME","PIPESEGNO","USEDDATE","DESIGNDEPNAME","CONSTRUNIT",\
                          "SUPERVISORUNIT","TESTUNIT","FDNAME","COLLECTDATE","COLLECTUNIT","INPUTDATETIME")
    
    pipeSegmentdataFieldTuple=("OBJECTID","CODE","PIPENAME","NAME","USEDDATE","DESIGNDEPNAME",\
                              "CONSTRUNIT","SUPERVISORUNIT","TESTUNIT","FDNAME","COLLECTDATE",\
                              "COLLECTUNIT","INPUTDATETIME")
    
    fieldsSequenceDic={"OBJECTID":0,"CODE":1,"PIPENAME":2,"NAME":3,"USEDDATE":4,"DESIGNDEPNAME":5,\
                              "CONSTRUNIT":6,"SUPERVISORUNIT":7,"TESTUNIT":8,"FDNAME":9,"COLLECTDATE":10,\
                              "COLLECTUNIT":11,"INPUTDATETIME":12}
    #��ȡ�ܶιܾ���������
    PipeSegmentDataList=[]
    with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",pipeSegmentdataFieldTuple) as PPcursor:
        for PC in PPcursor:
            if PC[0] is not None and str(PC[0]).strip()!="":
                PipeSegmentDataList.append([PC[0],PC[1],PC[2],PC[3],PC[4],PC[5],PC[6],\
                                            PC[7],PC[8],PC[9],PC[10],PC[11],PC[12]])

    
    fieldList=[]
    fieldNameList=[]
    if feature not in doNotFillTableTuple and int(arcpy.GetCount_management(feature).getOutput(0))!=0:
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
                                        #if row[0]==PLS[1] and PLS[fieldsSequenceDic[FGFT]] is not None
                                        if row[0]==PLS[1]:
                                            row[1]=PLS[fieldsSequenceDic[FGFT]]
                                            cursor.updateRow(row)
                                    else:
                                        #if row[0]==PLS[1] and PLS[fieldsSequenceDic["NAME"]] is not None
                                        if row[0]==PLS[1]:
                                            row[1]=PLS[fieldsSequenceDic["NAME"]]
                                            cursor.updateRow(row)
                                    
                except Exception, e:
                    print e.message
                    pass
                continue
#����ɾ���ظ�Ҫ�غ���
def deleteIdentical(feature):
    """
    ����һ��ɾ��Ҫ�������ظ�Ҫ�صĺ���,
    ����˼·��
    ����arcgis��DeleteIdentical_management����ɾ�������ظ���Ҫ�أ���Ҫ�����ͷ����ͨ������Ҫ��
    """
    arcpy.DeleteIdentical_management(feature,"Shape")
#�༭����Խ��
def copyPipesegmenttoGascross():
    """
    ������Ϊ���ܶα��еĴ���Խ����ͬ���������д�뵽����Խ����
    ����˼·��
    ���ȴӹܶα���ѡ�����跽ʽΪ����Խ��Ҫ�أ����Ҫ����д�ܶα�ʱ��
        ������ȷ��д����跽ʽ�����Ϊ����Խ���뽫����跽ʽ����Ϊ��Խ���Խ��
    Ȼ����ЩҪ����ͬ��������ӵ�����Խ����
    """

    if arcpy.Exists("ForCross"):
        arcpy.Delete_management("ForCross")
    #�ӹܶα���ѡ����跽ʽΪ��Խ/��Խ��Ҫ��
    arcpy.Select_analysis("T_PN_PIPESEGMENT_GEO","ForCross","LAYMODE = 4 OR LAYMODE = 5")

    #�½��ֶ�ӳ���б����
    fieldMappings = arcpy.FieldMappings()     #�����ֶ�ӳ�����
    fieldTuple=("PIPENAME","PSCODE","PIPESEGNO","MSTART","MEND","USEDDATE","REFOBJSTART",\
                "OFFSETSTART","XSTART","YSTART","ZSTART","REFOBJEND","OFFSETEND",\
                "XEND","YEND","ZEND","CONSTRUNIT","SUPERVISORUNIT","TESTUNIT",\
                "FDNAME","INPUTDATETIME","COLLECTUNIT","COLLECTDATE","NAME")
    for FT in fieldTuple:
        if FT!="PSCODE" and FT!="PIPESEGNO":
            #�½��ֶ�ӳ�����
            fm=arcpy.FieldMap()        
            #��Դ�ֶ�������ֶ�ӳ����
            fm.addInputField("ForCross",FT)
            #����Ŀ���ֶ�ӳ��
            fm_name=fm.outputField
            fm_name.name = FT
            fm.outputField = fm_name
            #���ֶ�ӳ������ֶ�ӳ���б���
            fieldMappings.addFieldMap(fm)
        elif FT=="PSCODE":
            #�½��ֶ�ӳ�����
            fm=arcpy.FieldMap()        
            #��Դ�ֶ�������ֶ�ӳ����
            fm.addInputField("ForCross","CODE")
            #����Ŀ���ֶ�ӳ��
            fm_name=fm.outputField
            fm_name.name = FT
            fm.outputField = fm_name
            #���ֶ�ӳ������ֶ�ӳ���б���
            fieldMappings.addFieldMap(fm)
        elif FT=="PIPESEGNO":
            #�½��ֶ�ӳ�����
            fm=arcpy.FieldMap()        
            #��Դ�ֶ�������ֶ�ӳ����
            fm.addInputField("ForCross","NAME")
            #����Ŀ���ֶ�ӳ��
            fm_name=fm.outputField
            fm_name.name = FT
            fm.outputField = fm_name
            #���ֶ�ӳ������ֶ�ӳ���б���
            fieldMappings.addFieldMap(fm)
            
    #��ɸѡ���Ĵ���Խ�ܶ�,��ӵ�����Խ����
    arcpy.Append_management("ForCross","T_LP_GASCROSS_GEO","NO_TEST",fieldMappings,"")
    #ɾ���м��ļ�
    arcpy.Delete_management("ForCross")
    
def editGascrossFields():
    """
    ���ݹܶ���������������Խ���в����ֶε���д����˱��뱣֤����Խ�ܶε����Ƹ�ʽΪ��
    ***XX�����磩Խ�Σ�**����������ݴʣ�XX�����������ݴʣ�����ٹ�·����·��**�ӣ�**���ȡ�
    1�������ȼ�Ĭ��Ϊ�����������Ƿ����¶�Ӱ��Ĭ��Ϊ���Ƿ�����ɢ����Ӱ��Ĭ��Ϊ���Ƿ����׹�Ĭ��Ϊ��
    2����Խ����ΪPTA����Խ����ΪACA����·�ȼ�Ĭ��Ϊһ����·���Ǹ���·�Ĵ�Խ��·�ȼ�Ĭ��Ϊ�ֵ�
    """
    if int(arcpy.GetCount_management("T_LP_GASCROSS_GEO").getOutput(0))!=0:
        with arcpy.da.UpdateCursor("T_LP_GASCROSS_GEO",("PSCODE","CODE","PIPESEGNO","DOH","AREALEVEL","CROSSOBJ",\
                                                        "RAILLEVEL","ROADLEVEL","MINDEPTH","HASCASING","ISTEMPAFFECT",\
                                                        "HASCURRENT","HYDRLEVEL","NAME")) as cursor:
            for row in cursor:
                try:
                    if row[0] is not None and len(row[0])==14 and re.search(r'\d{6}GB\d{6}',row[0]):
                        #����ܶ������а�����Խ�������ΪPTA001����Խ���=1.2�������ȼ�=����������
                        #����ܶ������а�����·���򴩿�Խ����=��·��Խ����Խ��·�ȼ�=һ����·����������Խ����=��·��Խ����Խ
                        #����ܶ������а������٣���Խ��·�ȼ�=���ٹ�·�������Ĵ�Խ��·�ȼ�=����������
                        #�Ƿ����¶�Ӱ��=���Ƿ�����ɢ����Ӱ��=���Ƿ����׹�=��
                        row[4]=3
                        row[9]=1
                        row[10]=0
                        row[11]=0
                        if "��Խ".decode("gb2312") in row[2]:
                            row[1]=row[0]+"PTA001"
                            row[3]=1.2
                            row[8]=1.2
                            if "��·".decode("gb2312") in row[2]:
                                row[6]=1
                                row[5]=5
                            else:
                                row[5]=3
                                if "����".decode("gb2312") in row[2]:
                                    row[7]=1
                                else:
                                    row[7]=4
                        else:
                            row[1]=row[0]+"ACA001"
                            row[12]=3
                            if "��".decode("gb2312") in row[2]:
                                row[5]=14
                            else:
                                row[5]=2
                    row[13]=row[13][:-1]
                    cursor.updateRow(row)
                except Exception,e:
                    print "�༭����Խ�ֶ�ʱ����������Ϣ��",e.message
                    pass
                continue
def editGascross():
    copyPipesegmenttoGascross()
    editGascrossFields()


#������Խ�����׹ܵ�Ҫ��д���׹�   
def copyGascrosstoCasing():
    """
    ������Ϊ������Խ�б�ʶ���׹ܵ�Ҫ����ͬ��������Ը��Ƶ��׹ܱ���
    ����˼·��
    ���ȴӴ���Խ����ѡ�����׹ܵĴ���ԽҪ�أ����Ҫ����д����Խ��ʱ��
        ������ȷ��д�Ƿ����׹��ֶ�
    Ȼ����ЩҪ����ͬ��������ӵ��׹ܱ���
    """
    #�Ӵ���Խ����ѡ���Ƿ����׹�Ϊ���Ҫ��
    arcpy.Select_analysis("T_LP_GASCROSS_GEO","ForCasing","HASCASING=1")       
    #��ɸѡ���Ĵ���Խ�ܶ�,��ӵ�����Խ����
    arcpy.Append_management("ForCasing","T_LP_CASING_GEO","NO_TEST","","")
    #ɾ���м��ļ�
    arcpy.Delete_management("ForCasing")
    #���׹ܽ������±���
    featureCoding("T_LP_CASING_GEO")
#���ܶηǼ�����Ϣд����߱�
def editPipeTableNonGeometricalProperties():
    '''
    ����һ�����ܶα��зǿռ����Ե����ݻ��ܵ����߱�ĺ�����
    �������һ�������е�ĳ���������ж��ֵ�������������������Ϊ�������ߵ���һ����None
    ����׷����й���ȷ��ʱ���뽫��������д��ܶα��еĹ��������ֶ���
    ����������Ϣ�ֶ����ֶ����
    �������ֶ�Ĭ��Ϊ0���յ����Ĭ��Ϊ���߳��ȣ��������ռ���������ڴ˺����н��б༭��
    ����˼·��
    ���Ȼ�ȡ���йܶε���Ϣ
    ��ν�ͬһ�����µ���Ϣ���л��ܣ���ȡ��������ֵ����ͬһ������ĳһ���Դ��ڶ�ֵ����������ΪNone��
    ������еĹ�����Ϣ������߱���
    '''

    #�༭���߷Ǽ�������
    pipeCodeList=[]         #������߱����б�
    pipeSegmentDataList=[]  #����ܶ������б�
    pipeEndDataList=[]      #����һ���б������յĹ�������  
    #��ȡ�ܶ���Ϣ���б�
    with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("OBJECTID","PIPENAME","PLCODE","LENGTH","DESIGNDEPNAME",\
                                                       "CONSTRUNIT","SUPERVISORUNIT","TESTUNIT","USEDDATE",\
                                                       "FDNAME","SEGTYPE","TRANSMEDIUM","SEGMATERIAL2",\
                                                       "TRANSAMOUNTDESIGN","TRANSAMOUNTREAL","DIAMETER",\
                                                       "THICKNESS","DESIGNPRESURE","PRESSURELEVEL",\
                                                       "RUNPRESSURE","MAXPRESSURE","ANTISEPTICMODE",\
                                                       "ANTISEPTICLEVEL","REPAIRHOLEMODE","REPAIRHOLLEVEL",\
                                                       "CPMODE","COLLECTDATE","COLLECTUNIT","INPUTDATETIME"\
                                                       )) as PPcursor:
        for PC in PPcursor:
            try:
                if PC[2] is not None:
                    pipeCodeList.append(PC[2])
                    pipeSegmentDataList.append([PC[1],PC[2],PC[3],PC[4],PC[5],PC[6],PC[7],PC[8],PC[9],PC[10],PC[11],PC[12],PC[13],\
                                                PC[14],PC[15],PC[16],PC[17],PC[18],PC[19],PC[20],PC[21],PC[22],PC[23],PC[24],PC[25],\
                                                PC[26],PC[27],PC[28]])
            except Exception,e:
                print "�༭���߱�Ǽ������Գ���������Ϣ��",e.message
                print PC[0],PC[1]
                pass
            continue
    #��ÿ�����ߵ����ݽ��л��ܼ���            
    for P in set(pipeCodeList):
        #����һ���б�����ʱ�Ĺ�������
        pipeALLDataList=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],\
                         [],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        pipeSingleDataList=[]
        for PPD in pipeSegmentDataList:
            if P==PPD[1]:
                for i in range(0,28):
                    pipeALLDataList[i].append(PPD[i])
        for i in range(0,28):
            if i!=2:
                if len(set(pipeALLDataList[i]))==1:
                   pipeSingleDataList.append(list(set(pipeALLDataList[i]))[0])
                else :
                    pipeSingleDataList.append(None)
            else:
                Sum=0
                for Len in pipeALLDataList[i]:
                    Sum+=Len
                pipeSingleDataList.append(Sum)      
        pipeEndDataList.append(pipeSingleDataList)

    #������д����߱���
    rows=arcpy.InsertCursor("T_PN_PIPELINE")
    for PED in pipeEndDataList:
        row=rows.newRow()
        row.setValue("NAME",PED[0])
        row.setValue("CODE",PED[1])
        row.setValue("LENGTH",PED[2])
        row.setValue("DESIGNDEPNAME",PED[3])
        row.setValue("CONSTRUNIT",PED[4])
        row.setValue("SUPERVISORUNIT",PED[5])
        row.setValue("TESTUNIT",PED[6])
        row.setValue("USEDDATE",PED[7])
        row.setValue("FNNAME",PED[8])
        row.setValue("SEGTYPE",PED[9])
        row.setValue("TRANSMEDIUM",PED[10])
        row.setValue("SEGMATERIAL2",PED[11])
        row.setValue("TRANSAMOUNTDESIGN",PED[12])
        row.setValue("TRANSAMOUNTREAL",PED[13])
        row.setValue("DIAMETER",PED[14])
        row.setValue("THICKNESS",PED[15])
        row.setValue("DESIGNPRESURE",PED[16])
        row.setValue("PRESSURELEVEL",PED[17])
        row.setValue("RUNPRESSURE",PED[18])
        row.setValue("MAXPRESSURE",PED[19])
        row.setValue("ANTISEPTICMODE",PED[20])
        row.setValue("ANTISEPTICLEVEL",PED[21])
        row.setValue("REPAIRHOLEMODE",PED[22])
        row.setValue("REPAIRHOLLEVEL",PED[23])
        row.setValue("CPMODE",PED[24])
        row.setValue("COLLECTDATE",PED[25])
        row.setValue("COLLECTUNIT",PED[26])
        row.setValue("INPUTDATETIME",PED[27])
        row.setValue("RUNSTATE",3)
        row.setValue("LAYMODE",1)
        row.setValue("MSTART",0)
        row.setValue("MEND",PED[2])
        rows.insertRow(row)  
#���ܶμ�����Ϣд����߱�
def editPipeTableGeometricalProperties():
    '''
    ����һ�����ڱ༭���߱��м�����Ϣ�ĺ�������������������꣩
    �༭���йܶα���ʱ��Ҫ��ĳһ���ߵĿ�ʼһ���ܶα���Ϊ001�����һ������Ϊ���Źܶ�
    �����л�ȡĳһ�����¹ܶ���Сֵ����㼸����Ϣ��Ϊ���ߵ���㼸����Ϣ���ܶ����ֵ���յ㼸����Ϣ��Ϊ�����յ㼸����Ϣ
    ����˼·��
    ���Ȼ�ȡ�ܶε����м�����Ϣ
    Ȼ�󽫹��ߵ���С�ܶα������㼸����Ϣ�����ܶε��յ㼸����Ϣ���Ի㼯
    ��󽫻㼯�����Ϣ���������߱�
    ***�༭���ߵļ�����Ϣ��Ҫ������������Ϣ�༭��ɺ����***
    '''
    #�༭���߼������ԣ����������ȣ�
    pipeCodeGList=[]         #������߱����б�
    pipeSegmentDataGList=[]  #����ܶ������б�
    pipeEndDataGList=[]      #����һ���б������յĹ�������   
    #��ȡ�ܶι��߼�����Ϣ
    with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("OBJECTID","PLCODE","CODE","ADDRSTART","REFOBJSTART",\
                                                       "OFFSETSTART","XSTART","YSTART","ZSTART","ADDREND",\
                                                       "REFOBJEND","OFFSETEND","XEND","YEND","ZEND")) as PPAcursor:
        for PCA in PPAcursor:
            try:
                if PCA[1] is not None:
                    pipeCodeGList.append(PCA[1])
                    pipeSegmentDataGList.append([PCA[1],PCA[2],PCA[3],PCA[4],PCA[5],PCA[6],PCA[7],\
                                                 PCA[8],PCA[9],PCA[10],PCA[11],PCA[12],PCA[13],PCA[14],])
                    
            except Exception,e:
                print "�༭���߱������Գ���������Ϣ��",e.message
                print PCA[0],PCA[1],PCA[2]
                pass
            continue
    #��ȡͬһ�����µ����йܶοռ���Ϣ
    for PG in set(pipeCodeGList):
        #����һ����ȡȫ���ܶε��б�
        pipeSegCodeALLDataList=[]
        for PPDG in pipeSegmentDataGList:
            if PG==PPDG[0]:
                pipeSegCodeALLDataList.append(PPDG[1])
        pipeSingleADataGList=[]
        pipeSingleBDataGList=[]
        for PPDGT in pipeSegmentDataGList:
            if PPDGT[1]==min(pipeSegCodeALLDataList):
                pipeSingleADataGList.append(PG)
                pipeSingleADataGList.append(PPDGT[2])
                pipeSingleADataGList.append(PPDGT[3])
                pipeSingleADataGList.append(PPDGT[4])
                pipeSingleADataGList.append(PPDGT[5])
                pipeSingleADataGList.append(PPDGT[6])
                pipeSingleADataGList.append(PPDGT[7])
            if PPDGT[1]==max(pipeSegCodeALLDataList):
                pipeSingleBDataGList.append(PPDGT[8])
                pipeSingleBDataGList.append(PPDGT[9])
                pipeSingleBDataGList.append(PPDGT[10])
                pipeSingleBDataGList.append(PPDGT[11])
                pipeSingleBDataGList.append(PPDGT[12])
                pipeSingleBDataGList.append(PPDGT[13])
        for PSB in pipeSingleBDataGList:
            pipeSingleADataGList.append(PSB)
        pipeEndDataGList.append(pipeSingleADataGList)
    #�����ռ��Ĺ������ݸ��������߱�
    with arcpy.da.UpdateCursor("T_PN_PIPELINE",("CODE","ADDRSTART","REFOBJSTART",\
                                                "OFFSETSTART","XSTART","YSTART","ZSTART","ADDREND",\
                                                "REFOBJEND","OFFSETEND","XEND","YEND","ZEND")) as PUcursor:
        for PURow in PUcursor:
            for PEDG in pipeEndDataGList:
                if PEDG[0]==PURow[0]:
                    PURow[1]=PEDG[1]
                    PURow[2]=PEDG[2]
                    PURow[3]=PEDG[3]
                    PURow[4]=PEDG[4]
                    PURow[5]=PEDG[5]
                    PURow[6]=PEDG[6]
                    PURow[7]=PEDG[7]
                    PURow[8]=PEDG[8]
                    PURow[9]=PEDG[9]
                    PURow[10]=PEDG[10]
                    PURow[11]=PEDG[11]
                    PURow[12]=PEDG[12]
                    PUcursor.updateRow(PURow)
#����༭�ܶα�
def editPipeTable():
    editPipeTableNonGeometricalProperties()
    editPipeTableGeometricalProperties()
#�༭����״Ҫ�ص����
def editMileage():
    '''
    ����һ�������豸��ʩ����̵ĺ�����
    ����֮ǰȷ���ܶα��������̺��յ�����Ѿ���ȷ��д��
    
    ����˼·��
    �������ô���·�����߹����������й��ߵ�·��
    Ȼ���豸��ʩ��·��ͨ����λҪ�ع��߼��������̣��������̺��յ���̣�
    ������ֵд��ÿһ��Ҫ�صĶ�Ӧ����ֶ���

    ��ͨ�������������Ҫ���飨�ر��Ƕ��ڹܶα���Žϴ����ֵΪ0�Ļ��߹ܶα���ֵ��С�����ֵ�ϴ�������Ҫ�ص��飩��
    '''
    #���ùܶ������̺��յ�����ֶδ������ߵ�·��
    arcpy.CreateRoutes_lr("T_PN_PIPESEGMENT_GEO","PLCODE","routes", "TWO_FIELDS", "MSTART","MEND")

    #��ȡ���ߵ���Ҫ�ؼ��е�����Ҫ����
    featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")
    for FC in featureClassList:
        if FC!="T_PN_THREEORFOUR_GEO":
            try:
                #�����в�Ϊ�յĵ�״Ҫ�ؽ�����̼���
                if arcpy.Describe(FC).shapeType=="Point" and\
                   int(arcpy.GetCount_management(FC).getOutput(0))!=0:
                    
                    #��ȡ����Ҫ�ص������ֶ�����
                    fieldList=[]
                    fieldNameList=[]
                    fieldList=arcpy.ListFields(FC)  #��ȡ�����ֶ��б�
                    for FL in fieldList: #��ȡÿһ����������ֶ�����
                        fieldNameList.append(FL.name)
                    if "MILEAGE" in fieldNameList:
                        #���һ���ֶ����ڸ���Ҫ�ص�OBJECTID
                        arcpy.AddField_management(FC,"OBJECTIDCOPY","TEXT")
                        # ��Ŀ����е�OBJECTID�ֶμ��㵽�豸�����
                        arcpy.CalculateField_management(FC,"OBJECTIDCOPY","!OBJECTID!","PYTHON")
                        #����Ŀ��Ҫ�ر���������
                        arcpy.LocateFeaturesAlongRoutes_lr(FC,"routes","PLCODE","0.01 Kilometers","out")
                        #�����������ӽ��������������ݵı���Ŀ��Ҫ�ر�����
                        arcpy.JoinField_management(FC,"OBJECTIDCOPY","out","OBJECTIDCOPY","MEAS")
                        # ���������Ӻ���ֶμ����Ҫ�صĹܶα���
                        arcpy.CalculateField_management(FC,"MILEAGE","!MEAS!","PYTHON")
                        # ɾ������ʱ�������ʱ�ֶ�
                        arcpy.DeleteField_management(FC,["MEAS","OBJECTIDCOPY"])
                        # ɾ���м��ļ�
                        arcpy.Delete_management("out")     
            except Exception,e:
                print featureClassCodeDictionary[feature],"�༭���ʱ����������Ϣ��",e.message
                pass
            continue
    #ɾ�������Ĺ켣ͼ��
    arcpy.Delete_management("routes")

#������������޸ĺ�����±���
def databaseReCoding():
    '''
    ����ѭ��������Ҫ�����±��뺯����ʵ�ֶ��������ݿⲻͬҪ�ص����±���
    '''
    #����һ��Ҫ�����±���ĺ���
    def featureReCoding(feature):
        '''
        ���Ѿ��޸ı�������ֵ��Ҫ����������±��룬�紩��Խ���ѽ�PTA�޸�ΪACAʱ�����Ҫ�ص��ر���
        ����˼·��
        ���Ȼ�ȡ�����ǰ17λ
        �������Ϊ�ֵ�Ľ�ֵ�����ݱ����˼·�������±���
        '''
        notCodingTuple=("T_PN_SOURCE_GEO","T_PN_STATION_GEO","T_PN_PIPESEGMENT_GEO")
        tempDictionary={}
        if feature not in notCodingTuple:
            with arcpy.da.UpdateCursor(feature,("CODE")) as cursor:
                for row in cursor:
                    try:
                        tempValue=0
                        if row[0] is not None and len(row[0])==20 \
                           and re.search(r'\d{6}GB\d{6}[A-Z]{3}\d{3}',row[0]):
                                key=row[0][:17]
                                if tempDictionary.has_key(key):
                                    tempValue=tempDictionary[key]
                                    row[0]=key + str(tempValue+1).zfill(3)
                                    tempDictionary[key]=tempValue+1
                                    cursor.updateRow(row)
                                else:
                                    tempDictionary[key]=1
                                    row[0]=key + str(tempValue+1).zfill(3)
                                    cursor.updateRow(row)
                    except Exception, e:
                        print featureClassCodeDictionary[feature],"���±༭����ʱ����������Ϣ��",e.message
                        pass
                    continue
    #��ȡ���ߵ���Ҫ�ؼ��е�����Ҫ����
    featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")            
    #���ú����޸ĸ�Ҫ�ر���
    for FC in featureClassList:
        if int(arcpy.GetCount_management(FC).getOutput(0))!=0:
            featureReCoding(FC)

#�༭��ͨ��
def editThreeorFourPipeSegmentCode():
    '''
    ���ÿռ����ӣ��ҵ���ͨ�����ܺ�֧�ܣ���д��ͨ�Ĺܶα��������ֱ�������ܱں�֧��ֱ����֧�ܱں�
    ����˼·��
    ����ɾ���ظ�Ҫ��
    Ȼ�����ÿռ����ӣ��ҵ�����ͨ����Ĺ���
    ������ߵ���㲻����ͨ�غϣ��������ߴ���������ߣ��򽫸ù��ߵ������Ϣд����ͨ����
    ����������ͨ�������غϣ�����ߴ����Ϊ֧�ߣ��򽫸ù��ߵ���Ϣд����ͨ����
    '''
    #ɾ���ظ�Ҫ��
    arcpy.DeleteIdentical_management("T_PN_THREEORFOUR_GEO","Shape")
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

    #����Ѿ�������ʱ�ļ�"TFSpatialJoinClass"����ɾ��
    if arcpy.Exists("TFSpatialJoinClass"):
        arcpy.Delete_management("TFSpatialJoinClass")
    #����Ѿ�������ʱ�ļ�"TFSpatialJoinOTOClass"����ɾ��
    if arcpy.Exists("TFSpatialJoinOTOClass"):
        arcpy.Delete_management("TFSpatialJoinOTOClass")
    #�ж�"OBJECTIDCOPY"�Ƿ������ͨ����
    fieldList = []
    for f in arcpy.ListFields("T_PN_THREEORFOUR_GEO"):
        fieldList.append(str(f.name))
    if "OBJECTIDCOPY" not in fieldList:
        #���ȸ���ͨ���һ�����ڸ���OBJECTID���ֶ�
        arcpy.AddField_management("T_PN_THREEORFOUR_GEO","OBJECTIDCOPY","TEXT")
        # ��Ŀ����е�OBJECTID�ֶμ��㵽�豸�����
        arcpy.CalculateField_management("T_PN_THREEORFOUR_GEO","OBJECTIDCOPY","!OBJECTID!","PYTHON")
    # ��Ҫ����ܶα���пռ����ӣ����ӷ�ʽ�ý���1�Զ�
    arcpy.SpatialJoin_analysis("T_PN_THREEORFOUR_GEO","T_PN_PIPESEGMENT_GEO","TFSpatialJoinClass","JOIN_ONE_TO_MANY","","","INTERSECT","","")
    # ��Ҫ����ܶα���пռ����ӣ����ӷ�ʽ�ý���1�Զ�
    arcpy.SpatialJoin_analysis("T_PN_THREEORFOUR_GEO","T_PN_PIPESEGMENT_GEO","TFSpatialJoinOTOClass","JOIN_ONE_TO_ONE","","","INTERSECT","","")
    
    TFMPPCodelist=[]
    with arcpy.da.SearchCursor("TFSpatialJoinClass",("OBJECTIDCOPY","JOIN_FID","CODE_1","DIAMETER","THICKNESS")) as TFCuosor:
        for TFrow in TFCuosor:
            with arcpy.da.SearchCursor("TFSpatialJoinOTOClass",("OBJECTIDCOPY","Join_Count")) as TOFCuosor:
                for TOFrow in TOFCuosor:
                    if TFrow[0]==TOFrow[0]:
                        TFMPPCodelist.append([TFrow[0],TFrow[1],TFrow[2],TFrow[3],TFrow[4],TOFrow[1]])
    #��ȡ�ܶ���Ϣ���б�
    PPDataList=[]
    with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("OBJECTID","SHAPE@")) as Pcursor:
        for Prow in Pcursor:
            PPDataList.append([Prow[0],Prow[1]])

    #������ͨ��
    with arcpy.da.UpdateCursor("T_PN_THREEORFOUR_GEO",\
                               ("OBJECTIDCOPY","PSCODE","SHAPE@X","SHAPE@Y",\
                                "MAINDIAMETER","MAINTHICKNESS","MINORDIAMETER","MINORTHICKNESS")) as TFUcursor:
        for TFUrow in TFUcursor:
            try:
                for PPD in PPDataList:
                    for TFMPPL in TFMPPCodelist:
                        if TFUrow[0]==TFMPPL[0] and PPD[0]==TFMPPL[1]:
                            #���ֻ��һ��������ͨ�㽻�㣬��ôֱ���Թ������ͨ
                            if TFMPPL[5]==1:
                                pass
                            #���������ͨ������������ߣ���ô�յ������������ͨ�����Ϊ���ܣ����Ϊ��ͨ�����Ϊ֧��
                            elif TFMPPL[5]==2:
                                if not (abs(TFUrow[2]-PPD[1].firstPoint.X)<1e-10 and abs(TFUrow[3]-PPD[1].firstPoint.Y)<1e-10) \
                                   and \
                                   not (abs(TFUrow[2]-PPD[1].lastPoint.X)<1e-10 and abs(TFUrow[3]-PPD[1].lastPoint.Y)<1e-10):
                                    TFUrow[1]=TFMPPL[2]
                                    if TFMPPL[3] is not None:
                                        TFUrow[4]=DiameterDNDic[str(TFMPPL[3])]
                                        TFUrow[5]=TFMPPL[4]
                                if abs(TFUrow[2]-PPD[1].firstPoint.X)<1e-10 and abs(TFUrow[3]-PPD[1].firstPoint.Y)<1e-10:
                                    if TFMPPL[3] is not None:
                                        TFUrow[6]=DiameterDNDic[str(TFMPPL[3])]
                                        TFUrow[7]=TFMPPL[4]
                            #�����������ͨ���������ߣ���ô��ֹ���������ͨ�����Ϊ���ܣ������յ�Ϊ��ͨ�����Ϊ����
                            elif TFMPPL[5]==3:
                                if abs(TFUrow[2]-PPD[1].lastPoint.X)<1e-10 and abs(TFUrow[3]-PPD[1].lastPoint.Y)<1e-10:
                                    TFUrow[1]=TFMPPL[2]
                                    if TFMPPL[3] is not None:
                                        TFUrow[4]=DiameterDNDic[str(TFMPPL[3])]
                                        TFUrow[5]=TFMPPL[4]
                                        TFUrow[6]=TFMPPL[5]
                                if not (abs(TFUrow[2]-PPD[1].firstPoint.X)<1e-10 and abs(TFUrow[3]-PPD[1].firstPoint.Y)<1e-10)\
                                   and \
                                   not (abs(TFUrow[2]-PPD[1].lastPoint.X)<1e-10 and abs(TFUrow[3]-PPD[1].lastPoint.Y)<1e-10):
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
    # ɾ�������Ƕ������ʱ�ֶ�
    arcpy.DeleteField_management("T_PN_THREEORFOUR_GEO",["OBJECTIDCOPY"])
    # ɾ���м��ļ�
    arcpy.Delete_management("TFSpatialJoinClass")
    arcpy.Delete_management("TFSpatialJoinOTOClass")

def editThreeorFourField():
    '''
    ���ùܶ���Ϣ���ܶ������Ϣд����ͨ����
    ����˼·��
    ���Ȼ�ȡ�ܶ���Ϣ
    Ȼ���ҵ���ͨ�ܶα�����ܶα���һ�µļ�¼��������ͨ��¼��ֵ�ɹ�����Ϣ���
    ������ͨ���б���
    '''
    
    #��ȡ�ܶ�����
    PipeSegmentDataList=[]
    with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("CODE","DIAMETER","THICKNESS","USEDDATE",\
                                                       "CONSTRUNIT","SUPERVISORUNIT","TESTUNIT","FDNAME","COLLECTDATE",\
                                                       "COLLECTUNIT","INPUTDATETIME","DESIGNPRESURE","NAME","SEGMATERIAL2")) as PPcursor:
        for PC in PPcursor:
            if PC[0] is not None and str(PC[0]).strip()!="":
                PipeSegmentDataList.append([PC[0],PC[1],PC[2],PC[3],PC[4],PC[5],PC[6],PC[7],PC[8],PC[9],PC[10],PC[11],PC[12],PC[13]])
    #������ͨ����
    tempDictionary={}       
    with arcpy.da.UpdateCursor("T_PN_THREEORFOUR_GEO",\
                               ("PSCODE","MAINDIAMETER","MAINTHICKNESS","INCONNECTMODE","MINORCONNECTMODE",\
                                "OUTCONNECTMODE","TXMATERIAL","USEDDATE","PRESSURELEVEL","CONSTRUNIT",\
                                "SUPERVISORUNIT","TESTUNIT","FDNAME","COLLECTDATE","COLLECTUNIT",\
                                "INPUTDATETIME","TXTYPE","MINORDIAMETER","PIPESEGNAME","CODE",\
                                "SHAPE@X","SHAPE@Y","X","Y","SPECIFICATIONS")) as cursor:
        for row in cursor:
            try:
                #��д��������
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
                #���б���
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
                print "�༭��ͨ��ͨʱ����������Ϣ��",e.message
                pass
            continue
def editThreeorFour():
    editThreeorFourPipeSegmentCode()
    editThreeorFourField()
            
#�༭�������ܶ��յ㼸����Ϣд������
def editBLOCK():
    #��ȡ�ܶ�����
    PipeSegmentDataList=[]
    with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("CODE","REFOBJEND","OFFSETEND","XEND","YEND","ZEND")) as PPcursor:
        for PC in PPcursor:
            if PC[0] is not None and str(PC[0]).strip()!="":
                PipeSegmentDataList.append([PC[0],PC[1],PC[2],PC[3],PC[4],PC[5]])
    #������ͨ����
    with arcpy.da.UpdateCursor("T_PN_BLOCK_GEO",("PSCODE","REFOBJ","OFFSET","X","Y","Z")) as cursor:
        for row in cursor:
            try:
                for PSD in PipeSegmentDataList:
                    if row[0]==PSD[0]:
                        row[1]=PSD[1]
                        row[2]=PSD[2]
                        row[3]=PSD[3]
                        row[4]=PSD[4]
                        row[5]=PSD[5]
                        cursor.updateRow(row)
            except Exception,e:
                print "�༭��������������Ϣ��",e.message
                pass
            continue
#�༭����Ҫ�ص�Ĭ��ֵ
def editDefaultValuesForFeature():
    #��ȡ�ܶ�����
    PipeSegmentDataList=[]
    with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("CODE","DESIGNPRESURE","RUNPRESSURE","SEGMATERIAL2",\
                                                       "ANTISEPTICMODE")) as PPcursor:
        for PC in PPcursor:
            if PC[0] is not None and str(PC[0]).strip()!="":
                PipeSegmentDataList.append([PC[0],PC[1],PC[2],PC[3],PC[4]])
    #�༭�������ұ��������ѹ��=�ܶ����ѹ����ʵ������ѹ��=�ܶ�ʵ��ѹ��
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
                    print "�༭��������Ĭ��ֵʱ����������Ϣ��",e.message
                    pass
                continue
    #�༭���ű�ѹ���ȼ�=�ܶ����ѹ�������Ź�������=�򷧣���������=�ֶ�������/�������ӷ�ʽ=���ӣ��ܶ�Ϊ�ֹܣ�=�������ӣ��ܶ�ΪPE��������/��ǰ����״̬=���������Ź���=���ڣ��Ƿ��Զ�̿���=��
    if int(arcpy.GetCount_management("T_PN_VALVE_GEO").getOutput(0))!=0:
        with arcpy.da.UpdateCursor("T_PN_VALVE_GEO",("PSCODE","PRESSURELEVEL","VALVETYPE","DRIVETYPE","INCONNECTMODE",\
                                                     "NORMALSTATE","CURRENTSTATE","OUTCONNECTMODE","VALVEFUNC","ISREMOTECONTROL"\
                                                     )) as Vcursor:
            for Vrow in Vcursor:
                try:
                    for PSD in PipeSegmentDataList:
                        if Vrow[0]==PSD[0]:
                            Vrow[1]=PSD[1]
                            #����ܶ�ΪPE�����ӷ�ʽĬ��Ϊ�������ӣ����Ϊ�ֹ���Ĭ��Ϊ����
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
                    print "�༭����Ĭ��ֵʱ����������Ϣ��",e.message
                    pass
                continue
    #�༭����ת����ͷ��ѹ���ȼ�=�ܶ����ѹ��
    if int(arcpy.GetCount_management("T_PN_SPE_GEO").getOutput(0))!=0:
        with arcpy.da.UpdateCursor("T_PN_SPE_GEO",("PSCODE","PRESSURELEVEL")) as SPcursor:
            for SProw in SPcursor:
                try:
                    for PSD in PipeSegmentDataList:
                        if SProw[0]==PSD[0]:
                            SProw[1]=PSD[1]
                            SPcursor.updateRow(SProw)
                except Exception,e:
                    print "�༭����ת����ͷĬ��ֵʱ����������Ϣ��",e.message
                    pass
                continue
    #�༭��ѹ�������ѹ��=�ܶ����ѹ��������ѹ��=�ܶ�����ѹ��
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
                    print "�༭��ѹ��Ĭ��ֵʱ����������Ϣ��",e.message
                    pass
                continue
    #�༭�쾶�ܱ�ѹ���ȼ�=�ܶ����ѹ��������/�������ӷ�ʽ=���ӣ��ܶ�Ϊ�ֹܣ�=�������ӣ��ܶ�ΪPE��
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
                    print "�༭�쾶��Ĭ��ֵʱ����������Ϣ��",e.message
                    pass
                continue
    #�༭��Ե��ͷ��ѹ���ȼ�=�ܶ����ѹ��������/�������ӷ�ʽ=����
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
                    print "�༭��Ե��ͷĬ��ֵʱ����������Ϣ��",e.message
                    pass
                continue
    #�༭��ͷ��ѹ���ȼ�=�ܶ����ѹ�����������=������ͷ������/�������ӷ�ʽ=���ӣ��ܶ�Ϊ�ֹܣ�=�������ӣ��ܶ�ΪPE��,����=̼�֣�����ܶβ��ϲ���PE��
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
                    print "�༭��ͷĬ��ֵʱ����������Ϣ��",e.message
                    pass
                continue

















