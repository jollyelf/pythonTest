# -*- coding: cp936 -*-
import os
import sys
import arcpy
import re



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

#����ÿһ��ͼ���Ŀ���ַ��ֵ�
featureClassCodeDictionary={
"T_BS_ELECMARK_GEO":"DBA",
"T_BS_GROUNDMARK_GEO":"BS",
"T_CP_ANODEBED_GEO":"YDA",
"T_CP_CPPOWER_GEO":"YBD",
"T_CP_DRNGDEVICE_GEO":"PLA",
"T_CP_FLEXANODE_GEO":"RYA",
"T_CP_RSANODE_GEO":"XYA",
"T_CP_SANODE_GEO":"XYA",
"T_CP_TESTTRUNK_GEO":"CSA",
"T_GE_BUILDING_GEO":"GEJ",
"T_GE_EMI_GEO":"GEG",
"T_GE_GEOHAZARD_GEO":"GEZ",
"T_GE_HLINE_GEO":"GEH",
"T_GE_HPOLYGON_GEO":"",
"T_GE_OTHPIPEPNT_GEO":"GES",
"T_GE_RAILWAY_GEO":"GET",
"T_GE_ROAD_GEO":"GED",
"T_GE_UNDROBSTACLE_GEO":"GEA",
"T_LP_ADDTLYR_GEO":"FSH",
"T_LP_APPENDANT_GEO":"",
"T_LP_CASING_GEO":"TGA",
"T_LP_CONDENSER_GEO":"FSJ",
"T_LP_GASCROSS_GEO":"A",
"T_LP_HYDRPROTECT_GEO":"HPA",
"T_LP_OPTICALHOLE_GEO":"GKA",
"T_LP_TUNNEL_GEO":"FSI",
"T_PN_BELLOW_GEO":"BWA",
"T_PN_BLOCK_GEO":"FDA",
"T_PN_ELBOW_GEO":"WGA",
"T_PN_IJOINT_GEO":"JTB",
"T_PN_PEPIPEWELD_GEO":"HKA",
"T_PN_PIPERISER_GEO":"GDA",
"T_PN_PRYCABINET_GEO":"QZ",
"T_PN_REDUCER_GEO":"YGA",
"T_PN_REGULATOR_GEO":"TY",
"T_PN_SEAMCUT_GEO":"HFA",
"T_PN_SOURCE_GEO":"Z",
"T_PN_SPE_GEO":"JTC",
"T_PN_STATION_GEO":"Z",
"T_PN_TAPPING_GEO":"KKA",
"T_PN_THREEORFOUR_GEO":"ST",
"T_PN_VALVE_GEO":"FM",
"T_PN_VALVEPIT_GEO":"FJ",
"T_PN_PIPESEGMENT_GEO":"GB"
}

#����һ�����ܶ������߼��Լ��ĺ���
def pipeSegmentLogicTest(feature):
    '''
    �ú������ڼ��ܶα��п��ܴ��ڵ��߼�����
    1��һ����Ϊʵ��������Ӧ��С����������������ʵ����������ֵ�����������������ֵ����Ϊ����
    2���涨��Դ���ߺ��������߱�����д�����ι��ߵı�������ƣ����δ��д������Ϊ����
    3���涨ѹ����������ѹ��֮������߼���ϵ����������ϸ��߼���ϵ������Ϊ����
    4��һ����ΪPE����û�з�����ʽ�ģ��������Ϊ����������ʽ����Ϊ����
    5��һ����Ϊ��д��ʵ������ѹ����ҪС�����ѹ����������ڣ���Ϊ����
    6���涨ͬһ�����µĹܶ����Ʋ����ظ�������ظ�����Ϊ����
    7�����øֹܵĵĹܾ��ͱں��й涨��ֵ������������ݷǲ�����һ��Χ�ڣ���Ϊ����
    '''
    #��ȡ���ڼ��Ĺ��߱�����
    TRANSAMOUNTErrorList=[] #����������������б�
    PNPErrorList=[]         #�����������ߺ���Դ������һ�ܶκ���һ�ܶ���д��Ϊ�յ��б�
    PLDPErrorList=[]        #����ѹ�����������ѹ����ƥ���������б�
    ANMErrorList=[]         #���PE�ܵķ�����ʽ�Ƿ���д��ȷ
    PRLDPErrorList=[]       #�������ѹ���Ƿ�С�����ѹ��
    MileageErrorList=[]     #���ܶ���̿��ܳ���ļ�¼
    NameAndOtherList=[]     #�ܶ����Ƽ�����ص��ֶ��б�
    NameAndPLList=[]        #�ܶ����ƺ͹��߱����б�
    
    steelDiameterList=[14,17,17.2,18,21.3,22,25,26.9,32,33.7,34,38,42.4,45,48,48.4,57,60,60.3,63,73,76,76.1,88.9,\
                       89,108,114,174,114.3,133,140,159,168,168.3,219,219.1,273,323.9,325,355.6,377,406.4,426,\
                       457,480,508,530,610,630,711,720,813,820,914,920,1016,1020] #���峣�øֹܹܾ��б�
    PEDiameterList=[20,25,32,40,50,63,75,90,110,125,160,180,200,225,250,280,315,\
                    355,400,450,500,560,630,710,800,900,1000,1200]#����PE��ֱ���б�
    steelThicknessList=[1.2,1.6,2.0,2.8,3.0,3.5,4.0,4.5,4.6,5.0,5.6,5.8,6.0,6.3,6.5,7.0,8.0,\
                        8.2,9.5,10.0,11.0,12.0,13.0,14.0,15.0,\
                        17.0,18.0,19.0,20.0,22.0,24.0,25.0,26.0,28.0,30.0,32.0,35.0,38.0,40.0,42.0,\
                        45.0,48.0,50.0,54.0] #����ֹܱں��б�
    DiameterErrorList=[]
    ThicknessErrorList=[]
    if feature=="T_PN_PIPESEGMENT_GEO":
        with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("OBJECTID","CODE","SEGTYPE",\
                                                           "SEGMATERIAL2","DIAMETER","THICKNESS",\
                                                           "PRESSURELEVEL","RUNPRESSURE","PPSNAME",\
                                                           "PPSCODE","NPSNAME","NPSCODE","ANTISEPTICMODE",\
                                                           "TRANSAMOUNTDESIGN","TRANSAMOUNTREAL",\
                                                           "DESIGNPRESURE","NAME","PLCODE",\
                                                           "COLLECTDATE","COLLECTUNIT","INPUTDATETIME",\
                                                           "LENGTH","MSTART","MEND")) as PPcursor:
            for PC in PPcursor:
                try:
                     #�趨�ܶα�������ɲŽ������м��
                    if (PC[1] is not None) and (str(PC[1]).strip()!=""):
                        #���ʵ���������Ƿ�С�����������
                        if (PC[13] is not None) and (PC[14] is not None):
                            if PC[13]< PC[14]:
                                TRANSAMOUNTErrorList.append([PC[0],PC[1],PC[13],PC[14]])

                        #����������ߺ���Դ���ߵ���һ����һ���Ƿ�����д
                        if (PC[2]==1 or PC[2]==2) and (PC[8] is None and PC[9] is None and \
                                                       PC[10] is None and PC[11] is None ):
                            PNPErrorList.append([PC[0],PC[1]])

                        #��鲻ͬѹ�������µ����ѹ���Ƿ�����
                        if (PC[6] is not None) and (PC[15] is not None):
                            if(PC[6]==1) and (PC[15]<=1.6 or PC[15]>4):    #��ѹ�ķ�ΧΪ(1.6,4]
                                PLDPErrorList.append([PC[0],PC[1],PC[6],PC[15]])
                            if(PC[6]==2) and (PC[15]<=0.4 or PC[15]>1.6):  #�θ�ѹ�ķ�ΧΪ(0.4,1.6]
                                PLDPErrorList.append([PC[0],PC[1],PC[6],PC[15]])
                            if(PC[6]==3) and (PC[15]<0.01 or PC[15]>0.4):  #��ѹ�ķ�ΧΪ[0.01,0.4]
                                PLDPErrorList.append([PC[0],PC[1],PC[6],PC[15]])
                            if(PC[6]==4) and (PC[15]<0 or PC[15]>0.01):    #��ѹ�ķ�ΧΪ(0,0.01)
                                PLDPErrorList.append([PC[0],PC[1],PC[6],PC[15]])

                        #���PE�ܵķ�����ʽӦ��Ϊ��
                        if (PC[3]==22 or PC[3]==23 or PC[3]==24 or PC[3]==25):
                            if PC[12]!=7 and PC[12] is not None:
                                ANMErrorList.append([PC[0],PC[1],PC[3],PC[12]])
                        
                        #�������ѹ���Ƿ���С�����ѹ��
                        if (PC[15] is not None) and (PC[7] is not None) and (str(PC[7]).strip()!=""):
                            if "-" in PC[7]:
                                if float(re.search(r'[^-]+$',PC[7]).group())>PC[15]:
                                    PRLDPErrorList.append([PC[0],PC[1],PC[7],PC[15]])
                            elif "~" in PC[7]:
                                if float(re.search(r'[^~]+$',PC[7]).group())>PC[15]:
                                    PRLDPErrorList.append([PC[0],PC[1],PC[7],PC[15]])                        
                            else:
                                if float(PC[7])>PC[15]:
                                    PRLDPErrorList.append([PC[0],PC[1],PC[7],PC[15]])

                        #�ܶ����Ƽ�������ֶ����ݼ����б�
                        if(PC[16] is not None):
                            NameAndPLList.append(PC[17]+PC[16])
                            NameAndOtherList.append([PC[0],PC[1],PC[17],PC[16]])

                            

                        #�ܾ����(�ֹܺ�PE��)
                        if(PC[3]!=22 and PC[3]!=23 and PC[3]!=24 and PC[3]!=25):
                            if (PC[4] is not None) and (PC[4] not in steelDiameterList):
                                DiameterErrorList.append([PC[0],PC[1],PC[4]])
                        elif (PC[4] is not None) and (PC[4] not in PEDiameterList):
                            DiameterErrorList.append([PC[0],PC[1],PC[4]])


                        #�ֹܱں���
                        if(PC[3]!=22 and PC[3]!=23 and PC[3]!=24 and PC[3]!=25):
                            if (PC[5] is not None) and (PC[5] not in steelThicknessList):
                                ThicknessErrorList.append([PC[0],PC[1],PC[5]])

                        #�ܶ���̼��
                        if PC[22]is not None and PC[23] is not None and \
                           re.search(r'\d{6}GB\d{3}001',PC[1]) and PC[22]!=0:
                            MileageErrorList.append([PC[0],PC[1],PC[21],PC[22],PC[23]])
                        if PC[22]is not None and PC[23] is not None and abs(abs(PC[23]-PC[22])-PC[21])>0.001:
                            MileageErrorList.append([PC[0],PC[1],PC[21],PC[22],PC[23]])
                            
                except:
                    print PC[0],PC[1],PC[2],PC[3],PC[4],PC[5],PC[6],PC[7],PC[8],PC[9],PC[10],\
                          PC[11],PC[12],PC[13],PC[14],PC[15],PC[16],PC[17],PC[18],PC[19],PC[20]
                    pass
                continue
                
    f=open("result.txt","a+")            
    if len(TRANSAMOUNTErrorList) !=0:
        f.write("�ܶα��д���ʵ����������������������������\n")
        for TMEL in TRANSAMOUNTErrorList:
            f.write(str(TMEL[0])+"\t"+str(TMEL[1])+"\t"+str(TMEL[2])+"\t"+str(TMEL[3])+"\n")
    if len(PNPErrorList) !=0:
        f.write("�ܶα�����Դ���߻��������ߴ�����һ�ܶκ���һ�ܶ�δ��д�������\n")
        for PNPEL in PNPErrorList:
            f.write(str(PNPEL[0])+"\t"+str(PNPEL[1])+"\n")
    if len(PLDPErrorList) !=0:
        f.write("�ܶα��д���ѹ�����������ѹ����д��ƥ��������\n")
        for PLDPEL in PLDPErrorList:
            f.write(str(PLDPEL[0])+"\t"+str(PLDPEL[1])+"\t"+str(PLDPEL[2])+"\t"+str(PLDPEL[3])+"\n")
    if len(ANMErrorList) !=0:
        f.write("�ܶα��д���PE���з�����ʽ�������\n")
        for ANMEL in ANMErrorList:
            f.write(str(ANMEL[0])+"\t"+str(ANMEL[1])+"\t"+str(ANMEL[2])+"\t"+str(ANMEL[3])+"\n")
    if len(PRLDPErrorList) !=0:
        f.write("�ܶα��д�������ѹ���������ѹ���������\n")
        for PRLDPEL in PRLDPErrorList:
            f.write(str(PRLDPEL[0])+"\t"+str(PRLDPEL[1])+"\t"+str(PRLDPEL[2])+"\t"+str(PRLDPEL[3])+"\n")
    if len(DiameterErrorList)!=0:
        f.write("�ܶα��д��ڹܾ��쳣�������\n")
        for DEL in DiameterErrorList:
            f.write(str(DEL[0])+"\t"+str(DEL[1])+"\t"+str(DEL[2])+"\n")
    if len(ThicknessErrorList)!=0:
        f.write("�ܶα��д��ڱں��쳣�������\n")
        for TEL in ThicknessErrorList:
            f.write(str(TEL[0])+"\t"+str(TEL[1])+"\t"+str(TEL[2])+"\n")
    if len(MileageErrorList)!=0:
        f.write("�ܶα��д�������쳣�������\n")
        for MLE in MileageErrorList:
            f.write(str(MLE[0])+"\t"+str(MLE[1])+"\t"+str(MLE[2])+"\t"+str(MLE[3])+"\t"+str(MLE[4])+"\n")
    

            
            
    #���ܶ������ظ����
    if len(NameAndPLList)!=len(set(NameAndPLList)):
        f.write("�ܶα��д���ͬһ�����¹ܶ������ظ��������\n")
        duNameList=[]
        for NL in NameAndPLList:
            if NameAndPLList.count(NL)>1:
                duNameList.append(NL)
        for dc in set(duNameList):
            for NAO in NameAndOtherList:
                try:
                    if NAO[3] in dc:
                        f.write(str(NAO[0])+"\t"+str(NAO[1])+"\t"+str(NAO[2])+"\t"\
                                +str(NAO[3].encode('gb2312'))+"\n")
                except UnicodeEncodeError:
                    print NAO[0],NAO[1],NAO[2],NAO[3],"�ܶ������ظ�"
                    pass
                continue
                    
    f.close()
                    


#����һ���������ֶ��Ƿ�Ϊ�յĺ���
def fieldIsNonetest(feature):
    '''
    �������Ҫ�ر��б�����д���ֶΣ��ڱ�������д������£��Ƿ��������¼��
    �г�������Ҫ�����ֶΣ�����Ƿ��ڱ���У�����ھͽ����ж�
    '''
    #����һ����Ҫ���������ֶε�Ԫ��
    testFieldTuple=("NAME","PSCODE","MSTART","REFOBJSTART","OFFSETSTART",\
                    "XSTART","YSTART","MEND","REFOBJEND","OFFSETEND","XEND","YEND",\
                    "LENGTH","ADDRSTART","CROSSWIDTH","AREALEVEL","PLCODE","TRANSMEDIUM",\
                    "ADDREND","X","Y","MILEAGE","REFOBJ","OFFSET","COLLECTDATE","COMPLETBY1",\
                    "COLLECTUNIT","INPUTDATETIME")#������ֻΪNone�����д���
    testFieldTuple2=("NAME","PSCODE","REFOBJSTART","REFOBJEND","ADDRSTART","PLCODE",\
                    "ADDREND","REFOBJ","COLLECTUNIT")#����ַ����ֶβ�ΪNone��Ϊ""�Ĵ���
    FieldNameDic={"NAME":"����","PSCODE":"�ܶα���","MSTART":"������","REFOBJSTART":"������λ�ò�����",\
                  "OFFSETSTART":"������λ��ƫ����","XSTART":"���X����","YSTART":"���Y����","MEND":"�յ����",\
                  "REFOBJEND":"�յ����λ�ò�����","OFFSETEND":"�յ����λ��ƫ����","XEND":"�յ�X����",\
                  "YEND":"�յ�Y����","LENGTH":"����","ADDRSTART":"���λ�õ���","CROSSWIDTH":"����Խ���",\
                  "AREALEVEL":"�����ȼ�","PLCODE":"���߱���","TRANSMEDIUM":"���ͽ���","ADDREND":"�յ�λ�õ���",\
                  "X":"X����","Y":"Y����","MILEAGE":"���","REFOBJ":"���λ�ò�����","OFFSET":"���λ��ƫ����",\
                  "COLLECTDATE":"�ɼ�����","COMPLETBY1":"�����","COLLECTUNIT":"�ɼ���λ","INPUTDATETIME":"¼��ʱ��"}
    
    fieldIsNoneList=[]   #��������ֶ�Ϊ�յ��б�
    fieldList=[]         #��������ֶε��б�
    fieldNameList=[]     #��������ֶ����Ƶ��б�
    fieldList=arcpy.ListFields(feature)  #��ȡ�����ֶ��б�
    for FL in fieldList: #��ȡÿһ����������ֶ�����
        fieldNameList.append(FL.name)
    for FT in testFieldTuple:
        if FT in fieldNameList:
            with arcpy.da.SearchCursor(feature,("OBJECTID","CODE",FT)) as cursor:
                for row in cursor:
                    try:
                        if (row[1] is not None) and (str(row[1]).strip()!=""):
                            if row[2] is None:
                                fieldIsNoneList.append([row[0],row[1],FT,row[2]])
                    except UnicodeEncodeError:
                        print row[0],row[1],FT,row[2]
                        pass
                    continue
    for FT2 in testFieldTuple2:
        if FT2 in fieldNameList:
            with arcpy.da.SearchCursor(feature,("OBJECTID","CODE",FT2)) as cursor:
                for row in cursor:
                    try:
                        if (row[1] is not None) and (str(row[1]).strip()!=""):
                            if row[2] is not None and row[2].strip()=="":
                                fieldIsNoneList.append([row[0],row[1],FT2,row[2]])
                    except:
                        print row[0],row[1],FT2,row[2]
                        pass
                    continue
    with open("result.txt","a+") as f:
        if len(fieldIsNoneList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"���д��ڱ����ֶ�δ��д�������\n")
            for FINL in fieldIsNoneList:
                try:
                    f.write(str(FINL[0])+"\t"+str(FINL[1])+"\t"+str(FieldNameDic[FINL[2]])+"\t"+str(FINL[3])+"\n")
                except:
                    print FINL[0],FINL[1],FieldNameDic[FINL[2]],FINL[3],"�����ֶ�Ϊ��"
                    pass
                continue

                        
#����һ���������Ƿ��ظ��ĺ���,���������ӡ���ļ�
def codeRepetitionTest(featureClass):
    codeList=[]
    codeAndObjList=[]
    with arcpy.da.SearchCursor(featureClass,("CODE","OBJECTID")) as cursor:
        for row in cursor:
            if row[0] is not None:
                codeAndObjList.append([row[1],row[0]])
                codeList.append(row[0])
    f=open("result.txt","a+")
    if len(codeList)!=len(set(codeList)):
        f.write(featureClassAliasDictionary[featureClass]+"("+str(featureClass)+")"+"���ڱ����ظ����ظ��ı���Ϊ��\n")
        #���ظ�����д�����ļ�
        ducodeList=[]
        for cd in codeList:
            if codeList.count(cd)>1:
                ducodeList.append(cd)
        for dc in set(ducodeList):
            for CAO in codeAndObjList:
                try:
                    if dc == CAO[1]:
                        f.write(str(CAO[0])+"\t"+str(CAO[1])+"\n")
                except:
                    print CAO[0],CAO[1],"�����ظ�"
                    pass
                continue
    f.close()


#����豸ʵʩ�Ƿ����丸�豸����ƥ��
def facilityAffiliationTest(feature):
    '''
    ��ԭ������豸��ʩ�͹ܶ��Ƿ�ƥ��Ļ����������Ż�����ǰ�ܶεı���ֱ��ͨ���豸ʵʩ��ܶοռ����Ӷ�����������ͨ���豸��ʩ���еĹܶα����ֶ�
    '''
    #������ЩҪ�ز���Ҫ�Զ����ܶα���
    notCheckFeatureTuple=("T_PN_PIPESEGMENT_GEO","T_PN_STATION_GEO","T_PN_SOURCE_GEO",\
                          "T_LP_GASCROSS_GEO","T_LP_CASING_GEO","T_PN_THREEORFOUR_GEO")
    FAErrorList=[]
    if feature not in notCheckFeatureTuple:
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
                #arcpy.JoinField_management(feature,"OBJECTIDCOPY","{}SpatialJoinClass".format(feature),"OBJECTIDCOPY","CODE_1")
                # ���������Ӻ���ֶμ����Ҫ�صĹܶα���
                with arcpy.da.SearchCursor("{}SpatialJoinClass".format(feature),\
                                           ("OBJECTIDCOPY","CODE","CODE_1")) as cursor:
                    for row in cursor:
                        if row[1] is not None and row[2] is not None and row[2] not in row[1]:
                            FAErrorList.append([row[0],row[1],row[2]])
                # ɾ����ӵ���ʱ�ֶ�
                arcpy.DeleteField_management(feature,"OBJECTIDCOPY")
                # ɾ���м��ļ�
                arcpy.Delete_management("{}SpatialJoinClass".format(feature))
                #��ӡ���ڴ������Ϣ���ļ�
                with open("result.txt","a+") as f:
                    if len(FAErrorList)!=0:
                        f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"�����豸��ʩ���벻ƥ��������\n")
                        for FAE in FAErrorList:
                            f.write(str(FAE[0])+"\t"+str(FAE[1])+"\t"+str(FAE[2])+"\n")
                    
        except Exception,e:
            print e.message
            pass
                
#�ж��ֶ��б����Ƿ����CODE��PSCODE�ֶ�
def checkFieldIsIn(feature,Code):
    fieldList=arcpy.ListFields(feature)
    fieldNameList=[]
    for f in fieldList:
        fieldNameList.append(f.name)
    if Code in fieldNameList:
        return True
    else:
        return False

#���ÿһ��Ҫ�ر����Ƿ񺬶�Ӧ�豸��ʩ��������
def facilityCodeTest(feature):
    #����һ�����ڵ�������Ҫ���б�
    checkAloneList=["T_PN_PIPESEGMENT_GEO","T_PN_SOURCE_GEO","T_PN_STATION_GEO",\
                "T_LP_GASCROSS_GEO","T_BS_GROUNDMARK_GEO","T_PN_THREEORFOUR_GEO"]
    codeList=[]
    if feature not in checkAloneList:
        with arcpy.da.SearchCursor(feature,("CODE","OBJECTID")) as cursor:
            for row in cursor:
                if row[0] is not None:
                    if len(row[0])!=20:
                        codeList.append([row[1],row[0]])
                    elif not re.search(r'\d{6}G[A-Z]\d{6}[A-Z]{3}\d{3}',row[0]):
                        codeList.append([row[1],row[0]])
                    elif(featureClassCodeDictionary[feature] not in row[0]):
                        codeList.append([row[1],row[0]])
    elif feature == "T_PN_PIPESEGMENT_GEO":
        with arcpy.da.SearchCursor(feature,("CODE","OBJECTID")) as cursor:
            for row in cursor:
                if row[0] is not None:
                    if (len(row[0])!=14):
                        codeList.append([row[1],row[0]])
                    elif not re.search(r'\d{6}G[A-Z]\d{6}',row[0]):
                        codeList.append([row[1],row[0]])
    elif feature =="T_PN_SOURCE_GEO":
        with arcpy.da.SearchCursor(feature,("CODE","OBJECTID")) as cursor:
            for row in cursor:
                if row[0] is not None:
                    if (len(row[0])!=11):
                        codeList.append([row[1],row[0]])
                    elif not re.search(r'\d{6}Z[A-Z]\d{3}',row[0]):
                        codeList.append([row[1],row[0]])
    elif feature =="T_PN_STATION_GEO":
        with arcpy.da.SearchCursor(feature,("CODE","OBJECTID")) as cursor:
            for row in cursor:
                if row[0] is not None:
                    if (len(row[0])!=11):
                        codeList.append([row[1],row[0]])
                    elif not re.search(r'\d{6}Z[A-Z]\d{3}',row[0]):
                        codeList.append([row[1],row[0]])                     
    elif feature == "T_LP_GASCROSS_GEO":
        with arcpy.da.SearchCursor(feature,("CODE","OBJECTID")) as cursor:
            for row in cursor:
                if row[0] is not None:
                    if (len(row[0])!=20):
                        codeList.append([row[1],row[0]])
                    elif not re.search(r'\d{6}G[A-Z]\d{6}[A-Z]{3}\d{3}',row[0]):
                        codeList.append([row[1],row[0]])
                    elif "PTA" not in row[0] and "ACA" not in row[0]:
                        codeList.append([row[1],row[0]])
    elif feature == "T_BS_GROUNDMARK_GEO":
        with arcpy.da.SearchCursor(feature,("CODE","OBJECTID")) as cursor:
            for row in cursor:
                if row[0] is not None:
                    if (len(row[0])!=20):
                        codeList.append([row[1],row[0]])
                    elif not re.search(r'\d{6}G[A-Z]\d{6}[A-Z]{3}\d{3}',row[0]):
                        codeList.append([row[1],row[0]])
                    elif "BS" not in row[0] and "MK" not in row[0] and "JSA" not in row[0]:
                        codeList.append([row[1],row[0]])
    elif feature == "T_PN_THREEORFOUR_GEO":
        with arcpy.da.SearchCursor(feature,("CODE","OBJECTID")) as cursor:
            for row in cursor:
                if row[0] is not None:
                    if (len(row[0])!=20):
                        codeList.append([row[1],row[0]])
                    elif not re.search(r'\d{6}G[A-Z]\d{6}[A-Z]{3}\d{3}',row[0]):
                        codeList.append([row[1],row[0]])
                    elif "STA" not in row[0] and "STB" not in row[0]:
                        codeList.append([row[1],row[0]])
    if(len(codeList)!=0):
        f=open("result.txt","a+")
        f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"������ڴ��󣬴������Ϊ��\n")
        for cl in codeList:
            try:
                f.write(str(cl[0])+"\t"+str(cl[1])+"\n")
            except UnicodeEncodeError:
                print cl[0],cl[1],"�豸��ʩ��������"
                pass
            continue
        f.close()

#����һ����ȡ�ܶα����ݵĺ���
def getPipeSegmentData():
    PipeSegmentList=[]
    with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("CODE","USEDDATE","DESIGNDEPNAME",\
                                                    "CONSTRUNIT","SUPERVISORUNIT","TESTUNIT",\
                                                    "FDNAME","COLLECTDATE","COLLECTUNIT",\
                                                    "INPUTDATETIME")) as PPcursor:
        for PC in PPcursor:
            if (PC[0] is not None) and (PC[0]!=""):
                PipeSegmentList.append([PC[0],PC[1],PC[2],PC[3],PC[4],PC[5],PC[6],PC[7],PC[8],PC[9]])
    return PipeSegmentList

#����һ�����ڼ���豸��ʩ�����Ƿ���ܶ����Ա���һ�µĺ���
def fieldIsSameTest(feature):
    #��ȡ�ܶ�����
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

    f=open("result.txt","a+")
    #���Ÿ������н��ܼ������������Ҫ��
    if feature in checkThreeFieldsList:
        CDErrorList=[]
        CUErrorList=[]
        #IDErrorList=[]
        with arcpy.da.SearchCursor(feature,("OBJECTID","PSCODE","COLLECTDATE","COLLECTUNIT",\
                                            "INPUTDATETIME","CODE")) as Tcousor:
            for TC in Tcousor:
                for PSL in PipeSegmentList:
                    if TC[5] is not None and TC[1]==PSL[0]:
                        if TC[2]!=PSL[7]:
                            CDErrorList.append([TC[0],TC[5],TC[2],TC[1],PSL[7]])
                        if TC[3]!=PSL[8]:
                            CUErrorList.append([TC[0],TC[5],TC[3],TC[1],PSL[8]])
                        #if TC[4]!=PSL[9]:
                            #IDErrorList.append([TC[0],TC[1]])
        if len(CDErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"�д��ڲɼ�ʱ����ܶβɼ�ʱ�䲻ƥ��������\n")
            for CEL in CDErrorList:
                try:
                    f.write(str(CEL[0])+"\t"+str(CEL[1])+"\t"+str(CEL[2])+"\t"+str(CEL[3])+"\t"+str(CEL[4])+"\n")
                except:
                    print CEL[0],CEL[1],CEL[2],CEL[3],CEL[4],"�ɼ�ʱ�䲻ƥ��"
                    pass
                continue
        if len(CUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"�д��ڲɼ���λ��ܶβɼ���λ��ƥ��������\n")
            for CUL in CUErrorList:
                try:
                    if CUL[2] is not None and CUL[4] is not None:
                        f.write(str(CUL[0])+"\t"+str(CUL[1])+"\t"+str(CUL[2].encode('gb2312'))\
                                +"\t"+str(CUL[3])+"\t"+str(CUL[4].encode('gb2312'))+"\n")
                    elif CUL[2] is None and CUL[4] is not None:
                        f.write(str(CUL[0])+"\t"+str(CUL[1])+"\t"+str(CUL[2])\
                                +"\t"+str(CUL[3])+"\t"+str(CUL[4].encode('gb2312'))+"\n")
                    elif CUL[2] is not None and CUL[4] is None:
                        f.write(str(CUL[0])+"\t"+str(CUL[1])+"\t"+str(CUL[2].encode('gb2312'))\
                                +"\t"+str(CUL[3])+"\t"+str(CUL[4])+"\n")
                except UnicodeEncodeError:
                    print CUL[0],CUL[1],CUL[2],CUL[3],CUL[4],"�ɼ�ʱ�䲻ƥ��"
                    pass
                continue
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
                    if TC[9] is not None and TC[1]==PSL[0]:
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
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"�д���Ͷ��������ܶ�Ͷ�����ڲ�ƥ��������\n")
            for UDL in UDErrorList:
                try:
                    f.write(str(UDL[0])+"\t"+str(UDL[1])+"\t"+str(UDL[2])+"\t"+str(UDL[3])+"\t"+str(UDL[4])+"\n")
                except:
                    print UDL[0],UDL[1],UDL[2],UDL[3],UDL[4],"Ͷ�����ڲ�ƥ��"
                    pass
                continue
        if len(COUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"�д���ʩ����λ��ܶ�ʩ����λ��ƥ��������\n")
            for COL in COUErrorList:
                try:
                    if COL[2] is not None and COL[4] is not None:
                        f.write(str(COL[0])+"\t"+str(COL[1])+"\t"+str(COL[2].encode('gb2312'))\
                                +"\t"+str(COL[3])+"\t"+str(COL[4].encode('gb2312'))+"\n")
                    elif COL[2] is None and COL[4] is not None:
                        f.write(str(COL[0])+"\t"+str(COL[1])+"\t"+str(COL[2])\
                                +"\t"+str(COL[3])+"\t"+str(COL[4].encode('gb2312'))+"\n")
                    elif COL[2] is not None and COL[4] is None:
                        f.write(str(COL[0])+"\t"+str(COL[1])+"\t"+str(COL[2].encode('gb2312'))\
                                +"\t"+str(COL[3])+"\t"+str(COL[4])+"\n")
                except:
                    print COL[0],COL[1],COL[2],COL[3],COL[4],"ʩ����λ��ƥ��"
                    pass
                continue
        if len(SUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"�д��ڼ���λ��ܶμ���λ��ƥ��������\n")
            for SUL in SUErrorList:
                try:
                    if SUL[2] is not None and SUL[4] is not None:
                        f.write(str(SUL[0])+"\t"+str(SUL[1])+"\t"+str(SUL[2].encode('gb2312'))\
                                +"\t"+str(SUL[3])+"\t"+str(SUL[4].encode('gb2312'))+"\n")
                    elif SUL[2] is None and SUL[4] is not None:
                        f.write(str(SUL[0])+"\t"+str(SUL[1])+"\t"+str(SUL[2])\
                                +"\t"+str(SUL[3])+"\t"+str(SUL[4].encode('gb2312'))+"\n")
                    elif SUL[2] is not None and SUL[4] is None:
                        f.write(str(SUL[0])+"\t"+str(SUL[1])+"\t"+str(SUL[2].encode('gb2312'))\
                                +"\t"+str(SUL[3])+"\t"+str(SUL[4])+"\n")
                except:
                    print SUL[0],SUL[1],SUL[2],SUL[3],SUL[4],"����λ��ƥ��"
                    pass
                continue
        if len(FDErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"�д��ڿ���ͼֽ�������ܶο���ͼֽ����Ų�ƥ��������\n")
            for FDL in FDErrorList:
                try:
                    if FDL[2] is not None and FDL[4] is not None:
                        f.write(str(FDL[0])+"\t"+str(FDL[1])+"\t"+str(FDL[2].encode('gb2312'))\
                                +"\t"+str(FDL[3])+"\t"+str(FDL[4].encode('gb2312'))+"\n")
                    elif FDL[2] is None and FDL[4] is not None:
                        f.write(str(FDL[0])+"\t"+str(FDL[1])+"\t"+str(FDL[2])\
                                +"\t"+str(FDL[3])+"\t"+str(FDL[4].encode('gb2312'))+"\n")
                    elif FDL[2] is not None and FDL[4] is None:
                        f.write(str(FDL[0])+"\t"+str(FDL[1])+"\t"+str(FDL[2].encode('gb2312'))\
                                +"\t"+str(FDL[3])+"\t"+str(FDL[4])+"\n")
                except:
                    print FDL[0],FDL[1],FDL[2],FDL[3],FDL[4],"����ͼֽ��ƥ��"
                    pass
                continue
        if len(CDErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"�д��ڲɼ�ʱ����ܶβɼ�ʱ�䲻ƥ��������\n")
            for CEL in CDErrorList:
                try:
                    f.write(str(CEL[0])+"\t"+str(CEL[1])+"\t"+str(CEL[2])+"\t"+str(CEL[3])+"\t"+str(CEL[4])+"\n")
                except:
                    print CEL[0],CEL[0],CEL[0],CEL[0],CEL[0],"�ɼ�ʱ�䲻ƥ��"
                    pass
                continue
        if len(CUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"�д��ڲɼ���λ��ܶβɼ���λ��ƥ��������\n")
            for CUL in CUErrorList:
                try:
                    if CUL[2] is not None and CUL[4] is not None:
                        f.write(str(CUL[0])+"\t"+str(CUL[1])+"\t"+str(CUL[2].encode('gb2312'))\
                                +"\t"+str(CUL[3])+"\t"+str(CUL[4].encode('gb2312'))+"\n")
                    elif CUL[2] is None and CUL[4] is not None:
                        f.write(str(CUL[0])+"\t"+str(CUL[1])+"\t"+str(CUL[2])\
                                +"\t"+str(CUL[3])+"\t"+str(CUL[4].encode('gb2312'))+"\n")
                    elif CUL[2] is not None and CUL[4] is None:
                        f.write(str(CUL[0])+"\t"+str(CUL[1])+"\t"+str(CUL[2].encode('gb2312'))\
                                +"\t"+str(CUL[3])+"\t"+str(CUL[4])+"\n")
                except:
                    print CUL[0],CUL[1],CUL[2],CUL[3],CUL[4],"�ɼ���λ��ƥ��"
                    pass
                continue
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
                    if TC[10] is not None and TC[1]==PSL[0]:
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
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"�д���Ͷ��������ܶ�Ͷ�����ڲ�ƥ��������\n")
            for UDL in UDErrorList:
                try:
                    f.write(str(UDL[0])+"\t"+str(UDL[1])+"\t"+str(UDL[2])+"\t"+str(UDL[3])+"\t"+str(UDL[4])+"\n")
                except:
                    print UDL[0],UDL[1],UDL[2],UDL[3],UDL[4],"Ͷ�����ڲ�ƥ��"
                    pass
                continue
        if len(COUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"�д���ʩ����λ��ܶ�ʩ����λ��ƥ��������\n")
            for COL in COUErrorList:
                try:
                    if COL[2] is not None and COL[4] is not None:
                        f.write(str(COL[0])+"\t"+str(COL[1])+"\t"+str(COL[2].encode('gb2312'))\
                                +"\t"+str(COL[3])+"\t"+str(COL[4].encode('gb2312'))+"\n")
                    elif COL[2] is None and COL[4] is not None:
                        f.write(str(COL[0])+"\t"+str(COL[1])+"\t"+str(COL[2])\
                                +"\t"+str(COL[3])+"\t"+str(COL[4].encode('gb2312'))+"\n")
                    elif COL[2] is not None and COL[4] is None:
                        f.write(str(COL[0])+"\t"+str(COL[1])+"\t"+str(COL[2].encode('gb2312'))\
                                +"\t"+str(COL[3])+"\t"+str(COL[4])+"\n")
                except:
                    print COL[0],COL[1],COL[2],COL[3],COL[4],"ʩ����λ��ƥ��"
                    pass
                continue
        if len(SUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"�д��ڼ���λ��ܶμ���λ��ƥ��������\n")
            for SUL in SUErrorList:
                try:
                    if SUL[2] is not None and SUL[4] is not None:
                        f.write(str(SUL[0])+"\t"+str(SUL[1])+"\t"+str(SUL[2].encode('gb2312'))\
                                +"\t"+str(SUL[3])+"\t"+str(SUL[4].encode('gb2312'))+"\n")
                    elif SUL[2] is None and SUL[4] is not None:
                        f.write(str(SUL[0])+"\t"+str(SUL[1])+"\t"+str(SUL[2])\
                                +"\t"+str(SUL[3])+"\t"+str(SUL[4].encode('gb2312'))+"\n")
                    elif SUL[2] is not None and SUL[4] is None:
                        f.write(str(SUL[0])+"\t"+str(SUL[1])+"\t"+str(SUL[2].encode('gb2312'))\
                                +"\t"+str(SUL[3])+"\t"+str(SUL[4])+"\n")
                except:
                    print SUL[0],SUL[1],SUL[2],SUL[3],SUL[4],"����λ��ƥ��"
                    pass
                continue
        if len(TUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"�д��ڼ�ⵥλ��ܶμ�ⵥλ��ƥ��������\n")
            for TUL in TUErrorList:
                try:
                    if TUL[2] is not None and TUL[4] is not None:
                        f.write(str(TUL[0])+"\t"+str(TUL[1])+"\t"+str(TUL[2].encode('gb2312'))\
                                +"\t"+str(TUL[3])+"\t"+str(TUL[4].encode('gb2312'))+"\n")
                    elif TUL[2] is None and TUL[4] is not None:
                        f.write(str(TUL[0])+"\t"+str(TUL[1])+"\t"+str(TUL[2])\
                                +"\t"+str(TUL[3])+"\t"+str(TUL[4].encode('gb2312'))+"\n")
                    elif TUL[2] is not None and TUL[4] is None:  
                        f.write(str(TUL[0])+"\t"+str(TUL[1])+"\t"+str(TUL[2].encode('gb2312'))\
                                +"\t"+str(TUL[3])+"\t"+str(TUL[4])+"\n")
                except:
                    print TUL[0],TUL[1],TUL[2],TUL[3],TUL[4],"��ⵥλ��ƥ��"
                    pass
                continue
        if len(FDErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"�д��ڿ���ͼֽ�������ܶο���ͼֽ����Ų�ƥ��������\n")
            for FDL in FDErrorList:
                try:
                    if FDL[2] is not None and FDL[4] is not None:
                        f.write(str(FDL[0])+"\t"+str(FDL[1])+"\t"+str(FDL[2].encode('gb2312'))\
                                +"\t"+str(FDL[3])+"\t"+str(FDL[4].encode('gb2312'))+"\n")
                    elif FDL[2] is None and FDL[4] is not None:
                        f.write(str(FDL[0])+"\t"+str(FDL[1])+"\t"+str(FDL[2])\
                                +"\t"+str(FDL[3])+"\t"+str(FDL[4].encode('gb2312'))+"\n")
                    elif FDL[2] is not None and FDL[4] is None:
                        f.write(str(FDL[0])+"\t"+str(FDL[1])+"\t"+str(FDL[2].encode('gb2312'))\
                                +"\t"+str(FDL[3])+"\t"+str(FDL[4])+"\n")
                except:
                    print FDL[0],FDL[1],FDL[2],FDL[3],FDL[4],"����ͼֽ��ƥ��"
                    pass
                continue
        if len(CDErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"�д��ڲɼ�ʱ����ܶβɼ�ʱ�䲻ƥ��������\n")
            for CEL in CDErrorList:
                try:
                    f.write(str(CEL[0])+"\t"+str(CEL[1])+"\t"+str(CEL[2])+"\t"+str(CEL[3])+"\t"+str(CEL[4])+"\n")
                except:
                    print CEL[0],CEL[1],CEL[2],CEL[3],CEL[4],"�ɼ�ʱ�䲻ƥ��"
                    pass
                continue
        if len(CUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"�д��ڲɼ���λ��ܶβɼ���λ��ƥ��������\n")
            for CUL in CUErrorList:
                try:
                    if CUL[2] is not None and CUL[4] is not None:
                        f.write(str(CUL[0])+"\t"+str(CUL[1])+"\t"+str(CUL[2].encode('gb2312'))\
                                +"\t"+str(CUL[3])+"\t"+str(CUL[4].encode('gb2312'))+"\n")
                    elif CUL[2] is None and CUL[4] is not None:
                        f.write(str(CUL[0])+"\t"+str(CUL[1])+"\t"+str(CUL[2])\
                                +"\t"+str(CUL[3])+"\t"+str(CUL[4].encode('gb2312'))+"\n")
                    elif CUL[2] is not None and CUL[4] is None:
                        f.write(str(CUL[0])+"\t"+str(CUL[1])+"\t"+str(CUL[2].encode('gb2312'))\
                                +"\t"+str(CUL[3])+"\t"+str(CUL[4])+"\n")
                except:
                    print CUL[0],CUL[1],CUL[2],CUL[3],CUL[4],"�ɼ���λ��ƥ��"
                    pass
                continue
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
                                            "COLLECTDATE","COLLECTUNIT","INPUTDATETIME","CODE")) as Tcousor:
            for TC in Tcousor:
                for PSL in PipeSegmentList:
                    if TC[10] is not None and TC[1]==PSL[0]:
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
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"�д���Ͷ��������ܶ�Ͷ�����ڲ�ƥ��������\n")
            for UDL in UDErrorList:
                try:
                    f.write(str(UDL[0])+"\t"+str(UDL[1])+"\t"+str(UDL[2])+"\t"+str(UDL[3])+"\t"+str(UDL[4])+"\n")
                except:
                    print UDL[0],UDL[1],UDL[2],UDL[3],UDL[4],"Ͷ�����ڲ�ƥ��"
                    pass
                continue
        if len(DUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"�д�����Ƶ�λ��ܶ���Ƶ�λ��ƥ��������\n")
            for DUL in DUErrorList:
                try:
                    if DUL[2] is not None and DUL[4] is not None:
                        f.write(str(DUL[0])+"\t"+str(DUL[1])+"\t"+str(DUL[2].encode('gb2312'))\
                                +"\t"+str(DUL[3])+"\t"+str(DUL[4].encode('gb2312'))+"\n")
                    if DUL[2] is None and DUL[4] is not None:
                        f.write(str(DUL[0])+"\t"+str(DUL[1])+"\t"+str(DUL[2])\
                                +"\t"+str(DUL[3])+"\t"+str(DUL[4].encode('gb2312'))+"\n")
                    if DUL[2] is not None and DUL[4] is None:
                        f.write(str(DUL[0])+"\t"+str(DUL[1])+"\t"+str(DUL[2].encode('gb2312'))\
                                +"\t"+str(DUL[3])+"\t"+str(DUL[4])+"\n")
                except:
                    print DUL[0],DUL[0],DUL[0],DUL[0],DUL[0],"��Ƶ�λ��ƥ��"
                    pass
                continue
        if len(COUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"�д���ʩ����λ��ܶ�ʩ����λ��ƥ��������\n")
            for COL in COUErrorList:
                try:
                    if COL[2] is not None and COL[4] is not None:
                        f.write(str(COL[0])+"\t"+str(COL[1])+"\t"+str(COL[2].encode('gb2312'))\
                                +"\t"+str(COL[3])+"\t"+str(COL[4].encode('gb2312'))+"\n")
                    elif COL[2] is None and COL[4] is not None:
                        f.write(str(COL[0])+"\t"+str(COL[1])+"\t"+str(COL[2])\
                                +"\t"+str(COL[3])+"\t"+str(COL[4].encode('gb2312'))+"\n")
                    elif COL[2] is not None and COL[4] is None:
                        f.write(str(COL[0])+"\t"+str(COL[1])+"\t"+str(COL[2].encode('gb2312'))\
                                +"\t"+str(COL[3])+"\t"+str(COL[4])+"\n")
                except:
                    print COL[0],COL[1],COL[2],COL[3],COL[4],"ʩ����λ��ƥ��"
                    pass
                continue
        if len(SUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"�д��ڼ���λ��ܶμ���λ��ƥ��������\n")
            for SUL in SUErrorList:
                try:
                    if SUL[2] is not None and SUL[4] is not None:
                        f.write(str(SUL[0])+"\t"+str(SUL[1])+"\t"+str(SUL[2].encode('gb2312'))\
                                +"\t"+str(SUL[3])+"\t"+str(SUL[4].encode('gb2312'))+"\n")
                    elif SUL[2] is None and SUL[4] is not None:
                        f.write(str(SUL[0])+"\t"+str(SUL[1])+"\t"+str(SUL[2])\
                                +"\t"+str(SUL[3])+"\t"+str(SUL[4].encode('gb2312'))+"\n")
                    elif SUL[2] is not None and SUL[4] is None:
                        f.write(str(SUL[0])+"\t"+str(SUL[1])+"\t"+str(SUL[2].encode('gb2312'))\
                                +"\t"+str(SUL[3])+"\t"+str(SUL[4])+"\n")
                except:
                    print SUL[0],SUL[1],SUL[2],SUL[3],SUL[4],"����λ��ƥ��"
                    pass
                continue
        if len(TUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"�д��ڼ�ⵥλ��ܶμ�ⵥλ��ƥ��������\n")
            for TUL in TUErrorList:
                try:
                    if TUL[2] is not None and TUL[4] is not None:
                        f.write(str(TUL[0])+"\t"+str(TUL[1])+"\t"+str(TUL[2].encode('gb2312'))\
                                +"\t"+str(TUL[3])+"\t"+str(TUL[4].encode('gb2312'))+"\n")
                    elif TUL[2] is None and TUL[4] is not None:
                        f.write(str(TUL[0])+"\t"+str(TUL[1])+"\t"+str(TUL[2])\
                                +"\t"+str(TUL[3])+"\t"+str(TUL[4].encode('gb2312'))+"\n")
                    elif TUL[2] is not None and TUL[4] is None:  
                        f.write(str(TUL[0])+"\t"+str(TUL[1])+"\t"+str(TUL[2].encode('gb2312'))\
                                +"\t"+str(TUL[3])+"\t"+str(TUL[4])+"\n")
                except:
                    print TUL[0],TUL[1],TUL[2],TUL[3],TUL[4],"��ⵥλ��ƥ��"
                    pass
                continue
        if len(CDErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"�д��ڲɼ�ʱ����ܶβɼ�ʱ�䲻ƥ��������\n")
            for CEL in CDErrorList:
                try:
                    f.write(str(CEL[0])+"\t"+str(CEL[1])+"\t"+str(CEL[2])+"\t"+str(CEL[3])+"\t"+str(CEL[4])+"\n")
                except:
                    print CEL[0],CEL[1],CEL[2],CEL[3],CEL[4],"�ɼ�ʱ�䲻ƥ��"
                    pass
                continue
        if len(CUErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"�д��ڲɼ���λ��ܶβɼ���λ��ƥ��������\n")
            for CUL in CUErrorList:
                try:
                    if CUL[2] is not None and CUL[4] is not None:
                        f.write(str(CUL[0])+"\t"+str(CUL[1])+"\t"+str(CUL[2].encode('gb2312'))\
                                +"\t"+str(CUL[3])+"\t"+str(CUL[4].encode('gb2312'))+"\n")
                    elif CUL[2] is None and CUL[4] is not None:
                        f.write(str(CUL[0])+"\t"+str(CUL[1])+"\t"+str(CUL[2])\
                                +"\t"+str(CUL[3])+"\t"+str(CUL[4].encode('gb2312'))+"\n")
                    elif CUL[2] is not None and CUL[4] is None:
                        f.write(str(CUL[0])+"\t"+str(CUL[1])+"\t"+str(CUL[2].encode('gb2312'))\
                                +"\t"+str(CUL[3])+"\t"+str(CUL[4])+"\n")
                except:
                    print CUL[0],CUL[1],CUL[2],CUL[3],CUL[4],"�ɼ���λ��ƥ��"
                    pass
                continue
        #if len(IDErrorList)!=0:
         #   print featureClassAliasDictionary[feature],feature, "�д���¼��ʱ����ܶ�¼��ʱ�䲻ƥ��������"
          #  for IEL in IDErrorList:
           #     print IEL
    f.close()
def facilityDiameterTest(feature):
    #�趨�����DNֵ�б�
    DNValueList=[15,20,25,32,40,50,65,80,100,125,150,200,250,300,350,400,450,500,600]
    #���йܾ�ֵ�б�
    DiameterList=[14, 17, 17.2, 18, 20, 21.3, 22, 25, 26.9, 32, 33.7, 34, 38, 40, 42.4, \
                  45, 48, 48.4, 50, 57, 60, 60.3, 63, 73, 75, 76, 76.1, 88.9, 89, 90, \
                  108, 110, 114.3, 125, 133, 140, 159, 160, 168, 168.3, 180, 200, 219, \
                  219.1, 225, 250, 273, 280, 315, 323.9, 325, 355, 355.6, 377, 400, 406,406.4, \
                  426, 450, 457, 480, 500, 508, 530, 560, 610, 630, 710, 711, 720, 800, 813, \
                  820, 900, 914, 920, 1000, 1016, 1020, 1200]
    #�趨ֱ����DNֵ֮��Ľ�-ֵ��ϵ
    DiameterDNDic={"14.0":10,"17.0":10,"17.2":10,"18.0":15,"20.0":15,"21.3":15,"22.0":15,"25.0":20,"26.9":20,\
                   "32.0":25,"33.7":25,"34.0":25,"38.0":32,"40.0":32,"42":32,"42.4":32,"45.0":40,"48.0":40,\
                   "48.4":40,"50.0":40,"57.0":50,"60.0":50,"60.3":50,"63.0":50,"73.0":65,"75.0":65,"76.0":65,\
                   "76.1":65,"88.9":80,"89.0":80,"90.0":80,"108.0":100,"110.0":100,"114.0":100,"114.3":100,\
                   "125.0":125,"133.0":125,"140.0":125,"159.0":150,"160.0":150,"168.0":150,"168.3":150,\
                   "180.0":150,"200.0":200,"219.0":200,"219.1":200,"225.0":200,"250.0":250,"273.0":250,\
                   "280.0":250,"315.0":300,"323.9":300,"325.0":300,"355.0":350,"355.6":350,"377.0":350,\
                   "400.0":400,"406.0":400,"406.4":400,"426.0":400,"450.0":450,"457.0":450,"480.0":450,"500.0":500,\
                   "508.0":500,"530.0":500,"560.0":500,"610.0":600,"630.0":600,"710.0":700,"711.0":700,\
                   "720.0":700,"800.0":800,"813.0":800,"820.0":800,"900.0":900,"914.0":900,"920.0":900,\
                   "1000.0":1000,"1016.0":1000,"1020.0":1000,"1200.0":1000}
    twoDiameterFeatureList=["T_PN_REDUCER_GEO","T_PN_SPE_GEO","T_PN_VALVE_GEO",\
                            "T_PN_ELBOW_GEO","T_PN_IJOINT_GEO"]
    diaFieldNameDict={"INDIAMETER":"���ֱ��","OUTDIAMETER":"����ֱ��","DIAMETER":"ֱ��",\
                   "MAINPIPEDIAMETER":"���ܵ��⾶","MAINDIAMETER":"����ֱ��","MINORDIAMETER":"֧��ֱ��"}

    DNErrorList=[]
    PipeSegmentDataList=[]
    with arcpy.da.SearchCursor("T_PN_PIPESEGMENT_GEO",("CODE","DIAMETER")) as PPcursor:
        for PC in PPcursor:
            try:
                if (PC[0] is not None) and (str(PC[0]).strip()!="") and \
                   (PC[1] is not None) and (PC[1] in DiameterList):
                    PipeSegmentDataList.append([PC[0],PC[1]])
            except:
                print PC[0],PC[1]
                pass
            continue
    #�������Ϊ�쾶��/����ת����ͷ/����/��ͷ/��Ե��ͷ
    if feature in twoDiameterFeatureList:
        with arcpy.da.SearchCursor(feature,("OBJECTID","CODE","INDIAMETER","OUTDIAMETER","PSCODE"))\
             as REcursor:
            for RProw in REcursor:
                for PLS in PipeSegmentDataList:
                    try:
                        if RProw[4]==PLS[0] and RProw[2]!=DiameterDNDic[str(round(PLS[1],1))]:
                            DNErrorList.append([RProw[0],PLS[0],PLS[1],RProw[1],"INDIAMETER",RProw[2]])
                        if RProw[4]==PLS[0] and RProw[3] not in DNValueList:
                            DNErrorList.append([RProw[0],PLS[0],PLS[1],RProw[1],"OUTDIAMETER",RProw[3]])
                    except:
                        print RProw[0],PLS[0],PLS[1],RProw[1],RProw[2],RProw[3],"���/����ֱ���쳣"
                        pass
                    continue

    #�������Ϊ����
    if feature =="T_PN_PIPERISER_GEO":
        with arcpy.da.SearchCursor(feature,("OBJECTID","CODE","DIAMETER","PSCODE"))\
             as REcursor:
            for RProw in REcursor:
                for PLS in PipeSegmentDataList:
                    try:
                        if RProw[3]==PLS[0] and RProw[2]!=DiameterDNDic[str(round(PLS[1],1))]:
                            DNErrorList.append([RProw[0],PLS[0],PLS[1],RProw[1],"DIAMETER",RProw[2]])
                    except:
                        print RProw[0],PLS[0],PLS[1],RProw[1],"DIAMETER",RProw[2]
                        pass
                    continue
    #�������Ϊ����
    if feature =="T_PN_TAPPING_GEO":
        with arcpy.da.SearchCursor(feature,("OBJECTID","CODE","MAINPIPEDIAMETER","PSCODE"))\
             as REcursor:
            for RProw in REcursor:
                for PLS in PipeSegmentDataList:
                    try:
                        if RProw[3]==PLS[0] and RProw[2]!=DiameterDNDic[str(round(PLS[1],1))]:
                            DNErrorList.append([RProw[0],PLS[0],PLS[1],RProw[1],"MAINPIPEDIAMETER",RProw[2]])
                    except:
                        print RProw[0],PLS[0],PLS[1],RProw[1],"MAINPIPEDIAMETER",RProw[2]
                        pass
                    continue

    #�������Ϊ��ͨ��ͨ
    if feature=="T_PN_THREEORFOUR_GEO":
        with arcpy.da.SearchCursor(feature,("OBJECTID","CODE","MAINDIAMETER","MINORDIAMETER","PSCODE"))\
             as REcursor:
            for RProw in REcursor:
                for PLS in PipeSegmentDataList:
                    try:
                        if RProw[4]==PLS[0] and RProw[2]!=DiameterDNDic[str(round(PLS[1],1))]:
                            DNErrorList.append([RProw[0],PLS[0],PLS[1],RProw[1],"MAINDIAMETER",RProw[2]])
                        if RProw[4]==PLS[0] and RProw[3] is not None and RProw[3] not in DNValueList:
                            DNErrorList.append([RProw[0],PLS[0],PLS[1],RProw[1],"MINORDIAMETER",RProw[3]])
                    except:
                        print RProw[0],PLS[0],PLS[1],RProw[1],RProw[2],RProw[3],"����/֧�ܹܾ��쳣"
    with open("result.txt","a+") as f:                    
        if len(DNErrorList)!=0:
            f.write(featureClassAliasDictionary[feature]+"("+str(feature)+")"+"���ڹܾ���д�쳣�����\n")
            for DNEL in DNErrorList:
                try:
                    f.write(str(DNEL[0])+"\t"+str(DNEL[1])+"\t"+\
                            str(DNEL[2])+"\t"+str(DNEL[3])+"\t"+str(diaFieldNameDict[DNEL[4]])+"\t"+str(DNEL[5])+"\n")
                except:
                    print DNEL[0],DNEL[1],DNEL[2],DNEL[3],diaFieldNameDict[DNEL[4]],DNEL[5],"�豸ֱ����ܶ�ֱ����ƥ��"
                    pass
                continue
                    
