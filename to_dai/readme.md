模型介绍和predict.py使用方法：

安装lightgbm package
```
pip install lightgbm
```

union站点的模型分为两种, 一种是不加o3作为x变量的, 一种是将o3作为x变量的，

- union model, 不加o3作为x变量的
  - model 路径: models/without_o3/
  - 使用predict.py 时候，修改：

    ```
    air_pollution = "no2" #对应的污染物
    with_o3 = False
    if_union = True
    if_tc = False
    single_site_code = 'MY1' #不用在意这个
    csv_path = "MaryleboneRoad.csv" #输入的csv地址，格式类似google drive里面的csv就可
    ```


- union model, 加o3作为x变量的
  - model 路径: models/with_o3/
  - 使用predict.py 时候，修改：

    ```
    air_pollution = "no2" #对应的污染物
    with_o3 = True
    if_union = True
    if_tc = False
    single_site_code = 'MY1' #不用在意这个
    csv_path = "MaryleboneRoad.csv" #输入的csv地址，格式类似google drive里面的csv就可
    ```


- single model的话之前我们train了MY1和KC1, 这里注明使用方法: 
  - model 路径: single_model/
  - 使用predict.py 时候，修改：

    ```
    air_pollution = "no2" #对应的污染物
    with_o3 = False #模型是否带有o3, 如果这里False, if_tc需要等于False
    if_union = False
    if_tc = False #只有MY1有一个加o3,加tc的模型，如果这里选True, with_o3需要等于True, 且single_site_code = 'MY1'
    single_site_code = 'MY1' #MY1 or KC1
    csv_path = "MaryleboneRoad.csv" #输入的csv地址，格式类似google drive里面的csv就可
    ```

- 最终的预测结果会是返回的csv里面的一列
  - 如果预测no2的话，列名就为no2_predict

- 目前目录下有两个模型predict的结果：
  - no2_MY1_single_with_o3_tc_MaryleboneRoad.csv #no2 MY1 single model, 加o3加tc
  - no2_union_without_o3_MaryleboneRoad.csv #no2 unoin model 不加o3


运行predict代码
```
python predict.py
```
