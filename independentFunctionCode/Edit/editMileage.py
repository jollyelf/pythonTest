# -*- coding: cp936 -*-
import arcpy

# 设置工作空间
workSpace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"
arcpy.env.workspace=workSpace


def editMileage():
    '''
    定义一个计算设备设施表里程的函数；
    计算之前确保管段表中起点里程和终点里程已经正确填写；
    
    基本思路：
    首先利用创建路径工具构建库中所有管线的路径
    然后将设备设施的路径通过定位要素工具计算出其里程（或起点里程和终点里程）
    最后将里程值写入每一个要素的对应里程字段中

    三通表计算完的里程需要检验（特别是对于管段编码号较大但里程值为0的或者管段编码值较小但里程值较大的情况需要重点检查），
    '''
    #利用管段起点里程和终点里程字段创建管线的路径
    arcpy.CreateRoutes_lr("T_PN_PIPESEGMENT_GEO","PLCODE","routes", "TWO_FIELDS", "MSTART","MEND")

    #获取管线地理要素集中的所有要素类
    featureClassList=arcpy.ListFeatureClasses("","","PIPEGEO")
    for FC in featureClassList:
        try:
            #对所有不为空的点状要素进行里程计算
            if arcpy.Describe(FC).shapeType=="Point" and\
               int(arcpy.GetCount_management(FC).getOutput(0))!=0:
                
                #获取输入要素的所有字段名称
                fieldList=[]
                fieldNameList=[]
                fieldList=arcpy.ListFields(FC)  #获取表中字段列表
                for FL in fieldList: #获取每一个表的所有字段名称
                    fieldNameList.append(FL.name)
                if "MILEAGE" in fieldNameList:
                    print FC
                    #添加一个字段用于复制要素的OBJECTID
                    arcpy.AddField_management(FC,"OBJECTIDCOPY","TEXT")
                    # 将目标表中的OBJECTID字段计算到设备编号中
                    arcpy.CalculateField_management(FC,"OBJECTIDCOPY","!OBJECTID!","PYTHON")
                    #计算目标要素表的里程数据
                    arcpy.LocateFeaturesAlongRoutes_lr(FC,"routes","PLCODE","0.01 Kilometers","out")
                    #利用属性连接将输出含有里程数据的表与目标要素表连接
                    arcpy.JoinField_management(FC,"OBJECTIDCOPY","out","OBJECTIDCOPY","MEAS")
                    # 将属性连接后的字段计算成要素的管段编码
                    arcpy.CalculateField_management(FC,"MILEAGE","!MEAS!","PYTHON")
                    # 删除连接时多出的临时字段
                    arcpy.DeleteField_management(FC,["MEAS","OBJECTIDCOPY"])
                    # 删除中间文件
                    arcpy.Delete_management("out")     
        except Exception,e:
            print e.message
            pass
        continue
    #删除创建的轨迹图层
    arcpy.Delete_management("routes")
editMileage()
