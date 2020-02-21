# 自动刷CSDN文章阅读量

- 使用讯代理动态更换IP进行文章访问。

- [讯代理官网](http://www.xdaili.cn?invitationCode=A158EF9DD1C6431AB0F049A660B0B27E)，购买动态IP，记录order_no和secret。

- 修改`main.py`中代码段：

  ```python
  if __name__ == '__main__':
      base_site = 'https://blog.csdn.net/你的博客名/article/list/'
      site = CSDNSite(base_site, 2) // 文章列表的最大页数
      visitor = RequestVisitor(order_no='你的订单号', secret='你的secret')
      app = Application(visitor, site)
      app.run()
      for i in range(20): // 线程数
          Thread(target=app.run).start()
  
  ```

  

- `pip install -r requirements.txt`安装依赖
- `python main.py`运行。



```abb2878586f049b6ad069a33a1858632
ZF20202191471gpt5kN
```

```
abb2878586f049b6ad069a33a1858632
```