# CSDN自动刷访问量软件

## 实现功能
- 爬取西刺代理，66IP，快代理, FreeProxy站点代理。
- 自动爬取CSDN的所有文章。
- 通过代理方式访问CSDN的所有文章，以增加阅读量。


## 使用说明

### 代码方式运行
- `git clone`方式或者下载zip代码包。
- `virtualenv venv`创建一个虚拟环境。
- `source /venv/bin/activate` 激活虚拟环境。
- `pip install -r requirements.txt`
- `python main.py`启动窗体。

### 二进制包运行

- 下载项目目录下的main.exe文件。

### 功能使用

- 在博客名那里填入个人博客名, 进入你的博客, 如网页链接为: `https://blog.csdn.net/xxxx`, 那么就把xxx填在博客名称那栏。

- 线程数量越大，刷得效率越高，占内存越大，使用默认值即可。访问轮数表示所有文章访问多少轮。理论总访问次数=线程数x访问轮数，访问间隔表示
间隔多久访问一篇文章。

- 代理页数表示免费代理需要爬多少页的代理，对应获取代理功能。

- 使用付费代理需要购买讯代理的动态代理, 然后填入订单和秘钥，直接点开始。

- 从文件导入代理文件编码为utf8, 内容格式为如下形式:
```
182.46.85.205:9999
110.243.19.204:9999
115.218.211.81:9000
45.166.84.6:8080
```
导入成功点开始运行即可。

- 使用免费代理, 需要导入或者先获取代理，代理会进行汇总， 然后点开始运行即可。

- [代理提取](http://www.66ip.cn/nmtq.php?getnum=10000&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=0&proxytype=2&api=66ip)，点击即可提取66代理一万个ip。
然后保存为txt即可。


### 注意

- 推荐使用文件导入代理方式。
- 软件开发原理可以见[博文](https://blog.csdn.net/ClassmateLin/article/details/104423904)。
## 运行效果


[MAC运行效果](./mac_effect.png)

[win7运行效果](./win7_effect.png)




**更多内容, 请关注个人博客:**`https://www.classmatelin.top`
