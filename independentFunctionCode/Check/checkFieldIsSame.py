# -*- coding: cp936 -*-
import arcpy

# ���ù����ռ�
arcpy.env.workspace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"

#��ȡ���ߵ���Ҫ�ؼ��е�����Ҫ����

featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")

#����һ��Ҫ���ļ����ͱ�Ƶ��ֵ�
featureClassAliasDictionary={
"T_BS_ELECMARK_GEO":"���ӱ�ʶ��",
"T_BS_GROUNDMARK_GEO":"�����ʾ��",
"T_CP_ANODEBED_GEO":"�����ش�",
"T_CP_CPPOWER_GEO":"����վ��������Դ��",
"T_CP_DRNGDEVICE_GEO":"����װ��",
"T_CP_FLEXANODE_GEO":"��������",
"T_CP_RSANODE_GEO":"��״��������",
"T_CP_SANODE_GEO":"��������",
"T_CP_TESTTRUNK_GEO":"����׮",
"T_GE_BUILDING_GEO":"������",
"T_GE_EMI_GEO":"��������",
"T_GE_GEOHAZARD_GEO":"�����ֺ�",
"T_GE_HLINE_GEO":"��״ˮϵ",
"T_GE_HPOLYGON_GEO":"��״ˮϵ",
"T_GE_OTHPIPEPNT_GEO":"����������λ��",
"T_GE_RAILWAY_GEO":"��·",
"T_GE_ROAD_GEO":"��·",
"T_GE_UNDROBSTACLE_GEO":"�����ϰ���",
"T_LP_ADDTLYR_GEO":"���ӱ�����",
"T_LP_APPENDANT_GEO":"������",
"T_LP_CASING_GEO":"�׹�",
"T_LP_CONDENSER_GEO":"��ˮ��",
"T_LP_GASCROSS_GEO":"����Խ",
"T_LP_HYDRPROTECT_GEO":"ˮ������",
"T_LP_OPTICALHOLE_GEO":"�������ֿ�",
"T_LP_TUNNEL_GEO":"���",
"T_PN_BELLOW_GEO":"���ƹ�",
"T_PN_BLOCK_GEO":"�����",
"T_PN_ELBOW_GEO":"��ͷ",
"T_PN_IJOINT_GEO":"��Ե��ͷ",
"T_PN_PEPIPEWELD_GEO":"PE�ܺ���",
"T_PN_PIPERISER_GEO":"����",
"T_PN_PRYCABINET_GEO":"��װ��",
"T_PN_REDUCER_GEO":"�쾶��",
"T_PN_REGULATOR_GEO":"��ѹ��",
"T_PN_SEAMCUT_GEO":"��������Ͳ���",
"T_PN_SOURCE_GEO":"��Դ",
"T_PN_SPE_GEO":"����ת����ͷ",
"T_PN_STATION_GEO":"��վ",
"T_PN_TAPPING_GEO":"����",
"T_PN_THREEORFOUR_GEO":"��ͨ��ͨ",
"T_PN_VALVE_GEO":"����",
"T_PN_VALVEPIT_GEO":"��������",
"T_PN_PIPESEGMENT_GEO":"�ܶ�"
}



#����һ�����ڼ���豸��ʩ�����Ƿ���ܶ����Ա���һ�µĺ���
def fieldIsSameTest(feature):
    PipeSegmentList=[]
    with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("CODE","USEDDATE","DESIGNDEPNAME",\
                                                    "CONSTRUNIT","SUPERVISORUNIT","TESTUNIT",\
                                                    "FDNAME","COLLECTDATE","COLLECTUNIT",\
                                                    "INPUTDATETIME")) as PPcursor:
        for PC in PPcursor:
            if (PC[0] is not None) and (PC[0]!=""):
                PipeSegmentList.append([PC[0],PC[1],PC[2],PC[3],PC[4],PC[5],PC[6],PC[7],PC[8],PC[9]])

    
    #���б����Ҫ����ļ������
    checkZeroFieldsList=["T_PN_SOURCE_GEO","T_PN_STATION_GEO","T_PN_PIPESEGMENT_GEO"]
    checkThreeFieldsList=["T_GE_BUILDING_GEO","T_GE_EMI_GEO","T_GE_GEOHAZARD_GEO",\
                      "T_GE_HLINE_GEO","T_GE_HPOLYGON_GEO","T_GE_OTHPIPEPNT_GEO",\
                      "T_GE_RAILWAY_GEO","T_GE_ROAD_GEO","T_GE_UNDROBSTACLE_GEO"]
    checkSevenFieldsList=["T_BS_ELECMARK_GEO","T_BS_GROUNDMARK_GEO","T_CP_CPPOWER_GEO",\
                      "T_CP_TESTTRUNK_GEO","T_LP_ADDTLYR_GEO","T_LP_APPENDANT_GEO",\
                      "T_LP_CONDENSER_GEO","T_LP_OPTICALHOLE_GEO","T_PN_BELLOW_GEO",\
                      "T_PN_BLOCK_GEO","T_PN_IJOINT_GEO","T_PN_PRYCABINET_GEO",\
                      "T_PN_REDUCER_GEO","T_PN_REGULATOR_GEO","T_PN_SPE_GEO",\
                      "T_PN_TAPPING_GEO","T_PN_VALVEPIT_GEO"]
    checkEightFieldsList=["T_CP_ANODEBED_GEO","T_CP_DRNGDEVICE_GEO","T_CP_FLEXANODE_GEO",\
                      "T_CP_RSANODE_GEO","T_CP_SANODE_GEO","T_LP_CASING_GEO",\
                      "T_LP_GASCROSS_GEO","T_LP_HYDRPROTECT_GEO","T_LP_TUNNEL_GEO",\
                      "T_PN_ELBOW_GEO","T_PN_PEPIPEWELD_GEO","T_PN_SEAMCUT_GEO",\
                      "T_PN_THREEORFOUR_GEO","T_PN_VALVE_GEO"]
    checkNineFieldsList=["T_PN_PIPERISER_GEO"]
    #���Ÿ������н��ܼ������������Ҫ��
    if feature in checkThreeFieldsList:
        CDErrorList=[]
        CUErrorList=[]
        #IDErrorList=[]
        with arcpy.da.SearchCursor(feature,("OBJECTID","PSCODE","COLLECTDATE","COLLECTUNIT",\
                                            "INPUTDATETIME","CODE")) as Tcousor:
            for TC in Tcousor:
                for PSL in PipeSegmentList:
                    if TC[1] is not None and TC[1]==PSL[0]:
                        if TC[2]!=PSL[7]:
                            CDErrorList.append([TC[0],TC[5],TC[2],TC[1],PSL[7]])
                        if TC[3]!=PSL[8]:
                            CUErrorList.append([TC[0],TC[5],TC[3],TC[1],PSL[8]])
                        #if TC[4]!=PSL[9]:
                            #IDErrorList.append([TC[0],TC[1]])
        if len(CDErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"�д��ڲɼ�ʱ����ܶβɼ�ʱ�䲻ƥ��������\n"
            for CEL in CDErrorList:
                print CEL[0],CEL[1],CEL[2],CEL[3],CEL[4]
        if len(CUErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"�д��ڲɼ���λ��ܶβɼ���λ��ƥ��������\n"
            for CUL in CUErrorList:
                print CUL[0],CUL[1],CUL[2],CUL[3],CUL[4]
        #if len(IDErrorList)!=0:
            #print featureClassAliasDictionary[feature],feature, "�д���¼��ʱ����ܶ�¼��ʱ�䲻ƥ��������"
            #for IEL in IDErrorList:
                #print IEL

    #���Ÿ������н��ܼ���߸�������Ҫ��            
    if feature in checkSevenFieldsList:
        UDErrorList=[]
        COUErrorList=[]
        SUErrorList=[]
        FDErrorList=[]
        CDErrorList=[]
        CUErrorList=[]
        #IDErrorList=[]
        with arcpy.da.SearchCursor(feature,("OBJECTID","PSCODE","USEDDATE",\
                                            "CONSTRUNIT","SUPERVISORUNIT",\
                                            "FDNAME","COLLECTDATE","COLLECTUNIT",\
                                            "INPUTDATETIME","CODE")) as Tcousor:
            for TC in Tcousor:
                for PSL in PipeSegmentList:
                    if TC[1] is not None and TC[1]==PSL[0]:
                        if TC[2]!=PSL[1]:
                            UDErrorList.append([TC[0],TC[9],TC[2],TC[1],PSL[1]])
                        if TC[3]!=PSL[3]:
                            COUErrorList.append([TC[0],TC[9],TC[3],TC[1],PSL[3]])
                        if TC[4]!=PSL[4]:
                            SUErrorList.append([TC[0],TC[9],TC[4],TC[1],PSL[4]])
                        if TC[5]!=PSL[6]:
                            FDErrorList.append([TC[0],TC[9],TC[5],TC[1],PSL[6]])
                        if TC[6]!=PSL[7]:
                            CDErrorList.append([TC[0],TC[9],TC[6],TC[1],PSL[7]])
                        if TC[7]!=PSL[8]:
                            CUErrorList.append([TC[0],TC[9],TC[7],TC[1],PSL[8]])
                        #if TC[8]!=PSL[9]:
                            #IDErrorList.append([TC[0],TC[1]])
        if len(UDErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"�д���Ͷ��������ܶ�Ͷ�����ڲ�ƥ��������\n"
            for UDL in UDErrorList:
                print UDL[0],UDL[1],UDL[2],UDL[3],UDL[4]
        if len(COUErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"�д���ʩ����λ��ܶ�ʩ����λ��ƥ��������\n"
            for COL in COUErrorList:
                print COL[0],COL[1],COL[2],COL[3],COL[4]
        if len(SUErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"�д��ڼ���λ��ܶμ���λ��ƥ��������\n"
            for SUL in SUErrorList:
                print SUL[0],SUL[1],SUL[2],SUL[3],SUL[4]
        if len(FDErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"�д��ڿ���ͼֽ�������ܶο���ͼֽ����Ų�ƥ��������\n"
            for FDL in FDErrorList:
                print FDL[0],FDL[1],FDL[2],FDL[3],FDL[4]
        if len(CDErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"�д��ڲɼ�ʱ����ܶβɼ�ʱ�䲻ƥ��������\n"
            for CEL in CDErrorList:
                print CEL[0],CEL[1],CEL[2],CEL[3],CEL[4]
        if len(CUErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"�д��ڲɼ���λ��ܶβɼ���λ��ƥ��������\n"
            for CUL in CUErrorList:
                print CUL[0],CUL[1],CUL[2],CUL[3],CUL[4]
        #if len(IDErrorList)!=0:
            #print featureClassAliasDictionary[feature],feature, "�д���¼��ʱ����ܶ�¼��ʱ�䲻ƥ��������"
            #for IEL in IDErrorList:
                #print IEL

    #���Ÿ������н��ܼ��˸�������Ҫ��            
    if feature in checkEightFieldsList:
        UDErrorList=[]
        COUErrorList=[]
        SUErrorList=[]
        FDErrorList=[]
        TUErrorList=[]
        CDErrorList=[]
        CUErrorList=[]
        #IDErrorList=[]
        with arcpy.da.SearchCursor(feature,("OBJECTID","PSCODE","USEDDATE",\
                                            "CONSTRUNIT","SUPERVISORUNIT","TESTUNIT",\
                                            "FDNAME","COLLECTDATE","COLLECTUNIT",\
                                            "INPUTDATETIME","CODE")) as Tcousor:
            for TC in Tcousor:
                for PSL in PipeSegmentList:
                    if TC[1] is not None and TC[1]==PSL[0]:
                        if TC[2]!=PSL[1]:
                            UDErrorList.append([TC[0],TC[10],TC[2],TC[1],PSL[1]])
                        if TC[3]!=PSL[3]:
                            COUErrorList.append([TC[0],TC[10],TC[3],TC[1],PSL[3]])
                        if TC[4]!=PSL[4]:
                            SUErrorList.append([TC[0],TC[10],TC[4],TC[1],PSL[4]])
                        if TC[5]!=PSL[5]:
                           TUErrorList.append([TC[0],TC[10],TC[5],TC[1],PSL[5]]) 
                        if TC[6]!=PSL[6]:
                            FDErrorList.append([TC[0],TC[10],TC[6],TC[1],PSL[6]])
                        if TC[7]!=PSL[7]:
                            CDErrorList.append([TC[0],TC[10],TC[7],TC[1],PSL[7]])
                        if TC[8]!=PSL[8]:
                            CUErrorList.append([TC[0],TC[10],TC[8],TC[1],PSL[8]])
                        #if TC[9]!=PSL[9]:
                            #IDErrorList.append([TC[0],TC[1]])

        if len(UDErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"�д���Ͷ��������ܶ�Ͷ�����ڲ�ƥ��������\n"
            for UDL in UDErrorList:
                print UDL[0],UDL[1],UDL[2],UDL[3],UDL[4]
        if len(COUErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"�д���ʩ����λ��ܶ�ʩ����λ��ƥ��������\n"
            for COL in COUErrorList:
                print COL[0],COL[1],COL[2],COL[3],COL[4]
        if len(SUErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"�д��ڼ���λ��ܶμ���λ��ƥ��������\n"
            for SUL in SUErrorList:
                print SUL[0],SUL[1],SUL[2],SUL[3],SUL[4]
        if len(TUErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"�д��ڼ�ⵥλ��ܶμ�ⵥλ��ƥ��������\n"
            for TUL in TUErrorList:
                print TUL[0],TUL[1],TUL[2],TUL[3],TUL[4]
        if len(FDErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"�д��ڿ���ͼֽ�������ܶο���ͼֽ����Ų�ƥ��������\n"
            for FDL in FDErrorList:
                print FDL[0],FDL[1],FDL[2],FDL[3],FDL[4]
        if len(CDErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"�д��ڲɼ�ʱ����ܶβɼ�ʱ�䲻ƥ��������\n"
            for CEL in CDErrorList:
                print CEL[0],CEL[1],CEL[2],CEL[3],CEL[4]
        if len(CUErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"�д��ڲɼ���λ��ܶβɼ���λ��ƥ��������\n"
            for CUL in CUErrorList:
                print CUL[0],CUL[1],CUL[2],CUL[3],CUL[4]
        #if len(IDErrorList)!=0:
         #   print featureClassAliasDictionary[feature],feature, "�д���¼��ʱ����ܶ�¼��ʱ�䲻ƥ��������"
          #  for IEL in IDErrorList:
           #     print IEL


    #���Ÿ��������ܼ��Ÿ�������Ҫ�� ������ȱ����ͼֽ�ֶ�           
    if feature in checkNineFieldsList:
        UDErrorList=[]
        DUErrorList=[]
        COUErrorList=[]
        SUErrorList=[]
        TUErrorList=[]
        CDErrorList=[]
        CUErrorList=[]
        #IDErrorList=[]
        with arcpy.da.SearchCursor(feature,("OBJECTID","PSCODE","USEDDATE","DESIGNDEPNAME",\
                                            "CONSTRUNIT","SUPERVISORUNIT","TESTUNIT",\
                                            "COLLECTDATE","COLLECTUNIT","INPUTDATETIME",\
                                            "CODE")) as Tcousor:
            for TC in Tcousor:
                for PSL in PipeSegmentList:
                    if TC[1] is not None and TC[1]==PSL[0]:
                        if TC[2]!=PSL[1]:
                            UDErrorList.append([TC[0],TC[10],TC[2],TC[1],PSL[1]])
                        if TC[3]!=PSL[2]:
                            DUErrorList.append([TC[0],TC[10],TC[3],TC[1],PSL[2]])
                        if TC[4]!=PSL[3]:
                            COUErrorList.append([TC[0],TC[10],TC[4],TC[1],PSL[3]])
                        if TC[5]!=PSL[4]:
                            SUErrorList.append([TC[0],TC[10],TC[5],TC[1],PSL[4]])
                        if TC[6]!=PSL[5]:
                           TUErrorList.append([TC[0],TC[10],TC[6],TC[1],PSL[5]]) 
                        if TC[7]!=PSL[7]:
                            CDErrorList.append([TC[0],TC[10],TC[7],TC[1],PSL[7]])
                        if TC[8]!=PSL[8]:
                            CUErrorList.append([TC[0],TC[10],TC[8],TC[1],PSL[8]])
                        #if TC[9]!=PSL[9]:
                         #   IDErrorList.append([TC[0],TC[1]])
        if len(UDErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"�д���Ͷ��������ܶ�Ͷ�����ڲ�ƥ��������\n"
            for UDL in UDErrorList:
                print UDL[0],UDL[1],UDL[2],UDL[3],UDL[4]
        if len(DUErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"�д�����Ƶ�λ��ܶ���Ƶ�λ��ƥ��������\n"
            for DUL in DUErrorList:
                print DUL[0],DUL[1],DUL[2],DUL[3],DUL[4]
        if len(COUErrorList)!=0:
            print featureClassAliasDictionary[feature]+feature,"�д���ʩ����λ��ܶ�ʩ����λ��ƥ��������\n"
            for COL in COUErrorList:
                print COL[0],COL[1],COL[2],COL[3],COL[4]
        if len(SUErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"�д��ڼ���λ��ܶμ���λ��ƥ��������\n"
            for SUL in SUErrorList:
                print SUL[0],SUL[1],SUL[2],SUL[3],SUL[4]
        if len(TUErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"�д��ڼ�ⵥλ��ܶμ�ⵥλ��ƥ��������\n"
            for TUL in TUErrorList:
                print TUL[0],TUL[1],TUL[2],TUL[3],TUL[4]
        if len(CDErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"�д��ڲɼ�ʱ����ܶβɼ�ʱ�䲻ƥ��������\n"
            for CEL in CDErrorList:
                print CEL[0],CEL[1],CEL[2],CEL[3],CEL[4]
        if len(CUErrorList)!=0:
            print featureClassAliasDictionary[feature],feature,"�д��ڲɼ���λ��ܶβɼ���λ��ƥ��������\n"
            for CUL in CUErrorList:
                print CUL[0],CUL[1],CUL[2],CUL[3],CUL[4]
        #if len(IDErrorList)!=0:
         #   print featureClassAliasDictionary[feature],feature, "�д���¼��ʱ����ܶ�¼��ʱ�䲻ƥ��������"
          #  for IEL in IDErrorList:
           #     print IEL




for fc in featureClassList:
    fieldIsSameTest(fc)
