# 51jingying-hunter-assistant
51精英猎头刷专业值和简历数助手


### 整体思路  

1. selenium+chromedriver获取cookie
2. requests进行名片投递


### 食用方法  
**如果有杀毒软件的话，程序可能会被移动到沙盒中，重新将其添加到信任区即可**

1. [下载](https://pan.baidu.com/s/1Pie6TnSeW9Ptp_V8o7DRtg)可执行程序(提取码:grk7)
2. 进入解压目录，在hunters.xlsx中添加自己的账号
3. 运行51jingying.exe(建议添加快捷方式到桌面，方便以后运行)


### TODO  

* ~~随机选取经理人~~
* ~~对页面进行解析，判断是第一次递出还是第二次递出~~
* ~~自动将下载简历上传到猎管家~~  **请不要在法律的边缘试探**
* ~~**[BUG]** 用phantomjs做driver，在强制下线时判断失败导致卡死~~
* 程序运行期间,若手动登陆网站则会导致cookie失效.若手动登陆的账号尚未投递名片完成,即使重启程序也不能再为此用户继续投递.考虑的解决方法一是：登陆一个用户投递完一个用户,弊端是chromedriver/phantonjs的窗口会一直存在.且如果是在投递到一半时登陆此种方法失效.二是建立日志记录,对于在程序运行期间手动登陆导致未投递完成的进行记录,在程序运行结束时清除掉此用户cookie,重启时就会重新获取此用户cookie.
* 有投递失败的账号自动重新尝试
* 每日投递日志记录

### 各文件说明  
| 文件名 | 说明 |
| :--- | :--- |
| assistant.py | 投递名片主程序，包含HunterAssistant类 |
| gui.py | 图形化界面 |
| utils.py | 一些有用的函数，包括使用selenium获取cookie |
| config.py | 配置文件，包括requests post名片时的headers |


### 开发小记  

1. pyinstaller 打包命令 `pyinstaller.exe -i="icon.ico" --add-data="phantomjs.exe;."  --add-data="icon.ico;." --add-data="hunters.xlsx;." -w .\gui.py -n "51ingying"`，加上`-F`参数后，调用不到chromedriver/phantomjs
2. pyinstaller 打包时需要退出电脑管家、360等杀毒软件，否则会自动被放到沙盒中
3. 虽然phantomjs已经不再维护，但是因为其不需要浏览器依赖，仍希望能实现Phantomjs获取cookies
4. GUI中的`print_log`需要一直获取(`while 1`)，而不是`while not log_q.empty()`
5. 写GUI时，需要将之前的print输出到tk的listbox中，开始想的是logging，自定义handler。最后使用`multiprocess.Queue`
6. 删除过期cookies的时候，使用`shutil.rmtree`
