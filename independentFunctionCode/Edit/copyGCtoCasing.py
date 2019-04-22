# -*- coding: cp936 -*-
import arcpy
import dataEditFunction

arcpy.env.workspace="C:\Users\lenovo\Desktop\PyTest\data\geodb.gdb"

def copyGascrosstoCasing():
    """
    本函数为将穿跨越中标识有套管的要素连同其相关属性复制到套管表中
    基本思路：
    首先从穿跨越表中选出有套管的穿跨越要素，因此要求填写穿跨越表时，
        必须正确填写是否有套管字段
    然后将这些要素连同其属性添加到套管表中
    """
    #从穿跨越表中选择是否有套管为真的要素
    arcpy.Select_analysis("T_LP_GASCROSS_GEO","ForCasing","HASCASING=1")       
    #将筛选出的穿跨越管段,添加到穿跨越表中
    arcpy.Append_management("ForCasing","T_LP_CASING_GEO","NO_TEST","","")
    #删除中间文件
    arcpy.Delete_management("ForCasing")
    #将编码中的PTA或者ACA替换为TGA
    dataEditFunction.featureCoding("T_LP_CASING_GEO")
copyGascrosstoCasing()
