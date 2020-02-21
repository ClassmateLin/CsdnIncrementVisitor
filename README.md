# 自动刷CSDN文章阅读量

- 使用讯代理动态更换IP进行文章访问。

- [讯代理官网](http://www.xdaili.cn?invitationCode=A158EF9DD1C6431AB0F049A660B0B27E)，购买动态IP，记录order_no和secret。

- 修改`config.ini`中代码的配置
```ini
[conf]
#订单号
order_no=你的订单号

#秘钥
secret=你的博客

#博客文章列表
blog=https://blog.csdn.net/你的博客名/article/list/

#博客页数， 你的博客列表有多少页填多少
page=2
```


  

- `pip install -r requirements.txt`安装依赖
- `python main.py`运行。



```abb2878586f049b6ad069a33a1858632
ZF20202191471gpt5kN
```

```
abb2878586f049b6ad069a33a1858632
```