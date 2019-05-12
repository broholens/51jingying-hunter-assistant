# 51jingying-hunter-assistant
51精英猎头刷专业值和简历数助手


### 整体思路  

1. selenium+chromedriver获取cookie
2. requests进行名片投递


### 食用方法  

**请自备Chrome浏览器**
1. 下载[51.zip](https://pan.baidu.com/s/1aEyWEy71k90knritW864vg)并解压(提取码：70q3)
2. 进入51目录，在hunters.csv中添加自己的账号
3. 运行51.exe(建议添加快捷方式到桌面，方便以后运行)


### TODO  

* <s>随机选取经理人</s>
* ~~对页面进行解析，判断是第一次递出还是第二次递出~~  不再判断，投递失败重新尝试其他经理人
* <s>自动将下载简历上传到猎管家</s>  **请不要在法律的边缘试探**
* **[BUG]** 用phantomjs做driver，在强制下线时判断失败导致卡死


### 各文件说明  

1. `assistant.py`   投递名片主程序，包含HunterAssistant类
2. `gui.py`             图形化界面
3. `utils.py`          一些有用的函数，包括使用selenium获取cookie
4. `config.py`        配置文件，包括requests post名片时的headers


### 开发小记  

1. pyinstaller 打包命令 `pyinstaller.exe -i="icon.ico" --add-data="chromedriver.exe;."  --add-data="icon.ico;." --add-data="hunters.csv;." -w .\gui.py -n "51`，加上`-F`参数后，调用不到chromedriver/phantomjs
2. pyinstaller 打包时需要退出电脑管家、360等杀毒软件，否则会自动被放到沙盒中
3. 虽然phantomjs已经不再维护，但是因为其不需要浏览器依赖，仍希望能实现Phantomjs获取cookies
4. GUI中的`print_log`需要一直获取(`while 1`)，而不是`while not log_q.empty()`
5. 写GUI时，需要将之前的print输出到tk的listbox中，开始想的是logging，自定义handler。最后使用`multiprocess.Queue`
6. 删除过期cookies的时候，使用`shutil.rmtree`
