# -*- coding: cp936 -*-
import arcpy
import time
import dataEditFunction as Function

def main(workSpace):
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    # ���ù����ռ�
    arcpy.env.workspace=workSpace

    #��ȡ���ߵ���Ҫ�ؼ��е�����Ҫ����
    featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")
    Function.editPipesegmentData()                      #��д�ܶα��е������ιܶ���Ϣ
    for FC in featureClassList:
        if FC!="T_PN_THREEORFOUR_GEO":
            Function.deleteIdentical(FC)                    #ɾ��Ҫ�����е��ظ�Ҫ��
            Function.PPCodeFill(FC)                         #��д�ܶα���
            Function.coordinateFill(FC)                     #��д����
            Function.featureCoding(FC)                      #��дҪ�ر���
            Function.fieldsFill(FC)                         #��д�����ֶ�
    Function.editPipeTable()                            #��д���߱�
    Function.editMileage()                              #��дҪ�����ֵ
    Function.editThreeorFour()                          #�༭��ͨ��
    Function.editGascross()                             #�༭����Խ��
    Function.editBLOCK()                                #���ܶ��յ㼸����Ϣд���Ӧ�ķ���Ｘ����Ϣ������

#���¹������������϶����ݿ�����޶����ʹ��
    
    #Function.copyGascrosstoCasing()                     #�Ӵ���Խ���н����׹ܲ���д���׹ܱ�,�˹���������д�괩��Խ��֮��ִ��
    #Function.databaseReCoding()                         #Ҫ�����±��룬�޸����������
    #Function.editDefaultValuesForFeature()              #�༭����Ҫ�����Ĭ��ֵ
    print "Edit Finished"
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
# arcpy.GetParameter(0) 
if __name__ == '__main__':
    #�ڴ˴�����Ҫ�������ݿ�Ŀ¼����
    workSpace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"
    main(workSpace)
        
        
        