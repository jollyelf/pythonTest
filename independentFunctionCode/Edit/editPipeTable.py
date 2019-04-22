# -*- coding: cp936 -*-
import arcpy

# ���ù����ռ�
workSpace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"
arcpy.env.workspace=workSpace

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
                print e.message
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
    #for aa in pipeEndDataList:
     #   print aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8],aa[9],aa[10],aa[11],aa[12],aa[13],\
      #        aa[14],aa[15],aa[16],aa[17],aa[18],aa[19],aa[20],aa[21],aa[22],aa[23],aa[24],aa[25],aa[26],aa[27]
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
                print e.message
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
editPipeTableNonGeometricalProperties()
editPipeTableGeometricalProperties()


    
    
