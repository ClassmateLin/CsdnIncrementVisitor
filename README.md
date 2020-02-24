# CSDN自动刷访问量软件

## 实现功能
- 爬取西祠代理，66IP，快代理, FreeProxy站点代理。
- 自动爬取CSDN的所有文章。
- 通过代理方式访问CSDN的所有文章，以增加阅读量。


## 使用说明

### 代码方式使用
- `git clone`方式或者下载zip代码包。
- `virtualenv venv`创建一个虚拟环境。
- `source /venv/bin/activate` 激活虚拟环境。
- `pip install -r requirements.txt`
- `python main.py`启动窗体。
- 博客名称那一列填入博客名称，例如你的博客主页地址为: `https://blog.csdn.net/ClassmateLin`,
那么填入的就是: `ClassmateLin`。
- 点击开始按钮即可，可能会卡顿一下，爬取代理和文章没有做多线程和进度条。

### 二进制包使用

- 下载目录下的exe文件。
- 单击运行，填好博客名，点击开始即可。


### 注意

如果点击开始按钮失败，说明自动获取代理失败。
需要点击获取代理按钮，然后再点击开始按钮即可。


## 运行效果

[运行效果](./effect.png)

