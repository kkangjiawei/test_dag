1.data0.txt为论文中的数据+table4中的可用数据，**共101条**，先前的实验将其作为**训练集**。经过确认，Table4中的数据为Table4中$MFI^{NF} (Cytosolic\ Entry)^b$数值不为空的CPP12和12条pBCP。

2.Table5.txt为Table5中$MFI^{NF} (Cytosolic\ Entry)^b$数值不为空的Tat和8条BCP数据，**共9条**，先前的实验将其作为**测试集**。

3.Table6.txt为Table6中$MFI^b$数值不为空的pBCP数据(去除pBCP427，table4中包含)，**共7条**，由于Table6和Table4、Table5的数据实验条件不同，因此先前的实验没有将Table6中的数据加入到data0中作为训练集。

4.Table7.txt为Table7中$MFI^{NF} (Cytosolic\ Entry)^b$数值不为空的7条BCP数据(不包含BCP427；)，**共7条**，先前的实验曾将data0和Table5的数据作为训练集、Table7的数据作为测试集进行尝试。

备注：

1.data0.txt(包含Table4)和Table5.txt的实验条件为5μM的荧光蛋白标记；Table6.txt和Table7.txt的实验条件为2μM的荧光蛋白标记。