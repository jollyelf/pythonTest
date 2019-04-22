# -*- coding: cp936 -*-
import arcpy
import re

#设施工作空间
workSpace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"
arcpy.env.workspace=workSpace


def copyPipesegmenttoGascross():
    """
    本函数为将管段表中的穿跨越段连同其相关属性写入到穿跨越表中
    基本思路：
    首先从管段表中选出敷设方式为穿跨越的要素，因此要求填写管段表时，
        必须正确填写其敷设方式（如果为穿跨越必须将其敷设方式设置为穿越或跨越）
    然后将这些要素连同其属性添加到穿跨越表中
    """

    if arcpy.Exists("ForCross"):
        arcpy.Delete_management("ForCross")
    #从管段表中选择敷设方式为穿越/跨越的要素
    arcpy.Select_analysis("T_PN_PIPESEGMENT_GEO","ForCross","LAYMODE = 4 OR LAYMODE = 5")

    #新建字段映射列表对象
    fieldMappings = arcpy.FieldMappings()     #创建字段映射对象
    fieldTuple=("PIPENAME","PSCODE","PIPESEGNO","MSTART","MEND","USEDDATE","REFOBJSTART",\
                "OFFSETSTART","XSTART","YSTART","ZSTART","REFOBJEND","OFFSETEND",\
                "XEND","YEND","ZEND","CONSTRUNIT","SUPERVISORUNIT","TESTUNIT",\
                "FDNAME","INPUTDATETIME","COLLECTUNIT","COLLECTDATE","NAME")
    for FT in fieldTuple:
        if FT!="PSCODE" and FT!="PIPESEGNO":
            #新建字段映射对象
            fm=arcpy.FieldMap()        
            #将源字段添加入字段映射中
            fm.addInputField("ForCross",FT)
            #设置目标字段映射
            fm_name=fm.outputField
            fm_name.name = FT
            fm.outputField = fm_name
            #将字段映射放入字段映射列表中
            fieldMappings.addFieldMap(fm)
        elif FT=="PSCODE":
            #新建字段映射对象
            fm=arcpy.FieldMap()        
            #将源字段添加入字段映射中
            fm.addInputField("ForCross","CODE")
            #设置目标字段映射
            fm_name=fm.outputField
            fm_name.name = FT
            fm.outputField = fm_name
            #将字段映射放入字段映射列表中
            fieldMappings.addFieldMap(fm)
        elif FT=="PIPESEGNO":
            #新建字段映射对象
            fm=arcpy.FieldMap()        
            #将源字段添加入字段映射中
            fm.addInputField("ForCross","NAME")
            #设置目标字段映射
            fm_name=fm.outputField
            fm_name.name = FT
            fm.outputField = fm_name
            #将字段映射放入字段映射列表中
            fieldMappings.addFieldMap(fm)
            
    #将筛选出的穿跨越管段,添加到穿跨越表中
    arcpy.Append_management("ForCross","T_LP_GASCROSS_GEO","NO_TEST",fieldMappings,"")
    #删除中间文件
    arcpy.Delete_management("ForCross")
    
def editGascrossFields():
    """
    依据管段名称来解析穿跨越表中部分字段的填写，因此必须保证穿跨越管段的名称格式为：
    ***XX穿（跨）越段，**代表地名形容词，XX代表类型形容词，如高速公路、铁路，**河，**渠等。
    1、地区等级默认为三级地区，是否受温度影响默认为否，是否受杂散电流影响默认为否，是否有套管默认为有
    2、穿越编码为PTA，跨越编码为ACA，铁路等级默认为一级铁路，非高速路的穿越公路等级默认为街道
    """
    if int(arcpy.GetCount_management("T_LP_GASCROSS_GEO").getOutput(0))!=0:
        with arcpy.da.UpdateCursor("T_LP_GASCROSS_GEO",("PSCODE","CODE","PIPESEGNO","DOH","AREALEVEL","CROSSOBJ",\
                                                        "RAILLEVEL","ROADLEVEL","MINDEPTH","HASCASING","ISTEMPAFFECT",\
                                                        "HASCURRENT","HYDRLEVEL","NAME")) as cursor:
            for row in cursor:
                try:
                    if row[0] is not None and len(row[0])==14 and re.search(r'\d{6}GB\d{6}',row[0]):
                        #如果管段名称中包含穿越，则编码为PTA001，穿越深度=1.2，地区等级=三级地区，
                        #如果管段名称中包含铁路，则穿跨越类型=铁路穿越，穿越铁路等级=一级铁路，其他穿跨越类型=公路穿越，穿越
                        #如果管段名称中包含高速，穿越公路等级=高速公路，其他的穿越公路等级=三级及以下
                        #是否受温度影响=否，是否受杂散电流影响=否，是否有套管=是
                        row[4]=3
                        row[9]=1
                        row[10]=0
                        row[11]=0
                        if "穿越".decode("gb2312") in row[2]:
                            row[1]=row[0]+"PTA001"
                            row[3]=1.2
                            row[8]=1.2
                            if "铁路".decode("gb2312") in row[2]:
                                row[6]=1
                                row[5]=5
                            else:
                                row[5]=3
                                if "高速".decode("gb2312") in row[2]:
                                    row[7]=1
                                else:
                                    row[7]=4
                        else:
                            row[1]=row[0]+"ACA001"
                            row[12]=3
                            if "渠".decode("gb2312") in row[2]:
                                row[5]=14
                            else:
                                row[5]=2
                    row[13]=row[13][:-1]
                    cursor.updateRow(row)
                except Exception,e:
                    print "编辑穿跨越字段时出错，错误信息：",e.message
                    pass
                continue
def editGascross():
    copyPipesegmenttoGascross()
    editGascrossFields()
editGascross()
