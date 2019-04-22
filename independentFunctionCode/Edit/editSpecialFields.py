# -*- coding: cp936 -*-
import os
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
#����һ�������ֶ����ĺ���
def fieldsFill(feature):
    '''
    ��������������ɵĹܶα���Ϣ���ڶ�Ҫ�ؽ��йܶ�ƥ��֮�󣬽������Ե���䣬��Щ���԰�����Ͷ�����ڡ���Ƶ�λ��
      ʩ����λ������λ����ⵥλ������ͼֽ����š��ɼ����ڡ��ɼ���λ��¼�����ڡ��������ơ��ܶ����ơ��ܾ���
    ���Ȼ�ȡ�ܶα����ԣ�
    Ȼ���ȡҪ�ر������б������Ҫ�����ֶ��������б��У������ݹܶα�����������ֶ�
    �ر�ע����ǹܾ���Ҫ���ùܶιܾ���DNֵ�����ֱ����ֻ��Ҫ������ֱ���ͱں�
    '''
    #�趨ֱ����DNֵ֮��Ľ�-ֵ��ϵ
    DiameterDNDic={"14.0":10,"15.0":10,"17.0":10,"17.2":10,"18.0":15,"20.0":15,"21.3":15,"22.0":15,"25.0":20,"26.9":20,\
                   "32.0":25,"33.7":25,"34.0":25,"38.0":32,"40.0":32,"42":32,"42.4":32,"45.0":40,"48.0":40,\
                   "48.4":40,"50.0":40,"57.0":50,"60.0":50,"60.3":50,"63.0":50,"73.0":65,"75.0":65,"76.0":65,\
                   "76.1":65,"88.9":80,"89.0":80,"90.0":80,"108.0":100,"110.0":100,"114.0":100,"114.3":100,\
                   "125.0":125,"133.0":125,"140.0":125,"159.0":150,"160.0":150,"168.0":150,"168.3":150,"174.0":150,\
                   "180.0":150,"200.0":200,"219.0":200,"219.1":200,"225.0":200,"250.0":250,"273.0":250,\
                   "280.0":250,"315.0":300,"323.9":300,"325.0":300,"355.0":350,"355.6":350,"377.0":350,\
                   "400.0":400,"406.4":400,"426.0":400,"450.0":450,"457.0":450,"480.0":450,"500.0":500,\
                   "508.0":500,"530.0":500,"560.0":500,"610.0":600,"630.0":600,"710.0":700,"711.0":700,\
                   "720.0":700,"800.0":800,"813.0":800,"820.0":800,"900.0":900,"914.0":900,"920.0":900,\
                   "1000.0":1000,"1016.0":1000,"1020.0":1000,"1200.0":1000}
    #����һ��������Ҫ�����Ԫ��
    #doNotFillTableTuple=("T_PN_PIPESEGMENT_GEO","T_PN_STATION_GEO","T_PN_SOURCE_GEO")
    doNotFillTableTuple=("T_LP_GASCROSS_GEO","T_LP_CASING_GEO")
    #����һ��ͨ�õ���������ֶ�Ԫ��
    fillGeneralFieldTuple=("PIPENAME","PIPESEGNAME","PIPESEGNO","USEDDATE","DESIGNDEPNAME","CONSTRUNIT",\
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
    if feature in doNotFillTableTuple:
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
                
        #���ܾ�����Ҫ˼·��һ��Ҫ�����һ�£�ֻ�������ʱ��Ҫ�صĹܾ����ùܶιܾ���DNֵ�������쾶�ܺ͸���ת����ͷ������ֱ�����
        for FDT in fillDiameterTuple:
            if FDT in fieldNameList:
                try:
                    with arcpy.da.UpdateCursor(feature,("PSCODE",FDT)) as cursor:
                        for row in cursor:
                            if row[0] is not None:
                                for PLS in PipeSegmentDataList:
                                    if FDT!="OUTDIAMETER":
                                        #if row[0]==PLS[1] and PLS[fieldsSequenceDic["DIAMETER"]] is not None
                                        if row[0]==PLS[1]:
                                            row[1]=float(DiameterDNDic[str(round(float(PLS[fieldsSequenceDic\
                                                                                           ["DIAMETER"]]),1))])
                                            cursor.updateRow(row)
                                    else:
                                        if feature!="T_PN_REDUCER_GEO" and  feature!="T_PN_SPE_GEO":
                                            #if row[0]==PLS[1] and PLS[fieldsSequenceDic["DIAMETER"]] is not None
                                            if row[0]==PLS[1]:
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
                                        #if row[0]==PLS[1] and PLS[fieldsSequenceDic["THICKNESS"]] is not None and row[1] is None
                                        if row[0]==PLS[1]:
                                            row[1]=PLS[fieldsSequenceDic["THICKNESS"]]
                                            cursor.updateRow(row)
                                    else:
                                        if feature!="T_PN_REDUCER_GEO" and  feature!="T_PN_SPE_GEO":
                                            #if row[0]==PLS[1] and PLS[fieldsSequenceDic["THICKNESS"]] is not None and row[1] is None:
                                            if row[0]==PLS[1]:
                                                row[1]=PLS[fieldsSequenceDic["THICKNESS"]]
                                                cursor.updateRow(row)
                except Exception, e:
                    print "������Ϣ��",e.message,
                    pass
                continue

            

for fc in featureClassList:
    print featureClassAliasDictionary[fc]
    fieldsFill(fc)
print "FillFinished"


    

