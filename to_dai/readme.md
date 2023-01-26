模型介绍和predict.py使用方法：

union站点的模型分为两种, 一种是不加o3作为x变量的, 一种是将o3作为x变量的，


- 1.union model, 不加o3作为x变量的
  - 1. model 路径: models/without_o3/
  - 2. 使用predict.py 时候，修改：

    ```
    air_pollution = "no2" #对应的污染物
    with_o3 = False
    if_union = True
    if_tc = False
    single_site_code = 'MY1' #不用在意这个
    csv_path = "MaryleboneRoad.csv" #输入的csv地址，格式类似google drive里面的csv就可
    ```


- 2.union model, 加o3作为x变量的
  - 1. model 路径: models/with_o3/
  - 2. 使用predict.py 时候，修改：

    ```
    air_pollution = "no2" #对应的污染物
    with_o3 = True
    if_union = True
    if_tc = False
    single_site_code = 'MY1' #不用在意这个
    csv_path = "MaryleboneRoad.csv" #输入的csv地址，格式类似google drive里面的csv就可
    ```


single model的话之前我们train了MY1和KC1, 这里注明使用方法: 
model 路径: single_model/
    ```
    air_pollution = "no2" #对应的污染物
    with_o3 = False #模型是否带有o3, 如果这里Flase, if_tc需要等于False
    if_union = False
    if_tc = False #只有MY1有一个加o3,加tc的模型，如果这里选True, with_o3需要等于True, 且single_site_code = 'MY1'
    single_site_code = 'MY1' #MY1 or KC1
    csv_path = "MaryleboneRoad.csv" #输入的csv地址，格式类似google drive里面的csv就可
    ```