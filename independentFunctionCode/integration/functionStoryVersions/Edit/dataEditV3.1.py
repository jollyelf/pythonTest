# -*- coding: cp936 -*-
import arcpy
import time
import dataEditFunction as Function

def main(workSpace):
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    # 设置工作空间
    arcpy.env.workspace=workSpace

    #获取管线地理要素集中的所有要素类
    featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")
    for FC in featureClassList:
        if FC!="T_PN_THREEORFOUR_GEO":
            Function.deleteIdentical(FC)                    #删除要素类中的重复要素
            Function.PPCodeFill(FC)                         #填写管段编码
            #Function.coordinateFill(FC)                     #填写坐标
            #Function.featureCoding(FC)                      #填写要素编码
            Function.fieldsFill(FC)                         #填写特殊字段
    #Function.editPipeTableNonGeometricalProperties()    #填写管线非几何属性
    #Function.editPipeTableGeometricalProperties()       #填写管线几何属性
    Function.editMileage()                              #填写要素里程值
    #Function.editGascross()                             #编辑穿跨越表
#   Function.copyGascrosstoCasing()                     #从穿跨越表中将有套管部分写入套管表,此功能须在填写完穿跨越表之后执行
#   Function.databaseReCoding()                         #要素重新编码，修改特征编码后
    Function.editThreeorFour()                          #编辑三通表
#   Function.editBLOCK()                                #将管段终点几何信息写入对应的封堵物几何信息属性中
#   Function.editDefaultValuesForFeature()              #编辑部分要素类的默认值
    print "Edit Finished"
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
# arcpy.GetParameter(0) 
if __name__ == '__main__':
    #在此处将需要检查的数据库目录复制
    workSpace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"
    main(workSpace)
        
        
        
