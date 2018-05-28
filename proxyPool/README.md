## ProxyPool
ProxyPool 代理池项目，提供代理 ip，以便自身爬虫需要。

### 环境
Ubuntu 16.04  
Python 3.5.2

### 项目依赖
1.安装 redis 数据库: 
```python
apt-get install redis-server
```
2.安装 requests, bs4, flask, lxml, redis
```python
pip install -r requirements.txt
```

### 项目说明
run.py 作为主函数启动  
api.py flask 网页显示代理  
crawler.py 代理 ip 爬取器(用到 BeautifulSoup、lxml、xpath、re、requests 等解析提取方法)  
db.py redis 数据库的设置都在这里面  
getter.py 代理获取器  
tester.py 代理测试器(使用多线程测试代理是否可用)  
scheduler.py 爬虫调度器(使用多进程开启 3 个进程:代理获取器、代理测试器、flask 网页)  
settings.py 爬虫的各种设置

### 使用说明(本地使用)
1.将项目 clone 到当前文件夹
```python
git clone XXX
```
2.切换目录
```python
cd proxyPool/
```
3.切换到虚拟环境 venv (项目自带虚拟环境)
```python
source venv/bin/activate
```
4.运行爬虫
```python
python run.py
```
5.获取可用代理  
在浏览器输入网址：http://localhost:5555/

注：如果虚拟环境不能用，可以将上面的项目依赖安装一下

### 项目部署到服务器
1.将 proxypool 工程全部传到服务器上(使用 scp 命令)
```python
scp -r proxypool root@39.108.62.133:/proxypool  # 具体用法查询 scp 命令
```
