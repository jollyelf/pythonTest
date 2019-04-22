# -*- coding: cp936 -*-
import arcpy
import re

# ���ù����ռ�
arcpy.env.workspace="C:\Users\lenovo\Desktop\PyTest\geodb.gdb"

#��ȡ���ߵ���Ҫ�ؼ��е�����Ҫ����

featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")



#����һ�����ܶκ��豸��ʩ���ڲ������߼��Լ��ĺ���
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
    
    steelDiameterList=[14,17,17.2,18,21.3,22,25,26.9,32,33.7,34,38,42.4,45,48,48.4,57,60,60.3,73,76,76.1,88.9,\
                       89,108,114.3,133,140,159,168,168.3,219,219.1,273,323.9,325,355.6,377,406.4,426,\
                       457,480,508,530,610,630,711,720,813,820,914,920,1016,1020] #���峣�øֹܹܾ��б�
    PEDiameterList=[20,25,32,40,50,63,75,90,110,125,160,180,200,225,250,280,315,\
                    355,400,450,500,560,630,710,800,900,1000,1200]#����PE��ֱ���б�
    steelThicknessList=[1.2,1.6,2.0,2.8,3.0,3.5,4.0,4.5,5.0,6.0,6.5,7.0,8.0,9.5,11.0,13.0,14.0,15.0,\
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
                    if (PC[15] is not None) and (PC[7] is not None)\
                       and (str(PC[7]).strip()!=""):
                        if "-" in PC[7]:
                            if float(re.search(r'[^-]+$',PC[7]).group())>PC[15]:
                                PRLDPErrorList.append([PC[0],PC[1],PC[7],PC[15]])
                        elif "~" in PC[7]:
                            if float(re.search(r'[^~]+$',PC[7]).group())>PC[15]:
                                PRLDPErrorList.append([PC[0],PC[1],PC[7],PC[15]])                        
                        elif re.search(r'[0-0].[0-9]',PC[7]):
                            if float(PC[7])>PC[15]:
                                PRLDPErrorList.append([PC[0],PC[1],PC[7],PC[15]])
                        else:
                            continue

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
                        
                    
                
                
                
    if len(TRANSAMOUNTErrorList) !=0:
        print "�ܶα��д���ʵ����������������������������\n"
        for TMEL in TRANSAMOUNTErrorList:
            print TMEL[0],TMEL[1],TMEL[2],TMEL[3]
    if len(PNPErrorList) !=0:
        print "�ܶα��д�����һ�ܶκ���һ�ܶ�δ��д�������\n"
        for PNPEL in PNPErrorList:
            print PNPEL[0],PNPEL[1]
    if len(PLDPErrorList) !=0:
        print "�ܶα��д���ѹ�����������ѹ����д�Ĳ�ƥ��������\n"
        for PLDPEL in PLDPErrorList:
            print PLDPEL[0],PLDPEL[1],PLDPEL[2],PLDPEL[3]
    if len(ANMErrorList) !=0:
        print "�ܶα��д���PE���з�����ʽ�������\n"
        for ANMEL in ANMErrorList:
            print ANMEL[0],ANMEL[1],ANMEL[2],ANMEL[3]
    if len(PRLDPErrorList) !=0:
        print "�ܶα��д�������ѹ���������ѹ���������\n"
        for PRLDPEL in PRLDPErrorList:
            print PRLDPEL[0],PRLDPEL[1],PRLDPEL[2],PRLDPEL[3]
    if len(DiameterErrorList)!=0:
        print "�ܶα��д��ڹܾ��쳣�������\n"
        for DEL in DiameterErrorList:
            print DEL[0],DEL[1],DEL[2]
    if len(ThicknessErrorList)!=0:
        print "�ܶα��д��ڱں��쳣�������\n"
        for TEL in ThicknessErrorList:
            print TEL[0],TEL[1],TEL[2]
    if len(MileageErrorList)!=0:
        print "�ܶα��д�������쳣�������\n"
        for MLE in MileageErrorList:
            print MLE[0],MLE[1],MLE[2],MLE[3],MLE[4]

            
            
    #���ܶ������ظ����
    if len(NameAndPLList)!=len(set(NameAndPLList)):
        print "�ܶα��д���ͬһ�����¹ܶ������ظ��������\n"
        duNameList=[]
        for NL in NameAndPLList:
            if NameAndPLList.count(NL)>1:
                duNameList.append(NL)
        for dc in set(duNameList):
            for NAO in NameAndOtherList:
                if NAO[3] in dc:
                    print NAO[0],NAO[1],NAO[2],NAO[3]


pipeSegmentLogicTest("T_PN_PIPESEGMENT_GEO")
                    
                

