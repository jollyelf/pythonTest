# -*- coding: cp936 -*-
import arcpy
import dataEditFunction

arcpy.env.workspace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"

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
    #�������е�PTA����ACA�滻ΪTGA
    dataEditFunction.featureCoding("T_LP_CASING_GEO")
copyGascrosstoCasing()
