# -*- coding: cp936 -*-
import arcpy
import re

#��ʩ�����ռ�
workSpace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"
arcpy.env.workspace=workSpace


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
editGascross()
