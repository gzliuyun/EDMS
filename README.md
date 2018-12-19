# Expert Database Management System  专家库系统
---
## 运行前的准备

### 1.安装Scrapy
- 预先安装twisted库，下载地址为：[https://www.lfd.uci.edu/~gohlke/pythonlibs/](https://www.lfd.uci.edu/~gohlke/pythonlibs/) ，  
![安装twisted组件](https://img-blog.csdn.net/20180903220228865?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3RpbmcwOTIy/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)  
找到合适自己的版本下载（如：python3.7，64位版本，选择最后一个下载）。  
然后在当前下载目录下安装对应的whl文件，如：  
`pip install Twisted-18.7.0-cp37-cp37m-win_amd64.whl`。
- 在命令行中执行：`pip install scrapy`。

### 2.安装pywin32
- 打开[https://sourceforge.net/projects/pywin32/files/pywin32/](https://sourceforge.net/projects/pywin32/files/pywin32/)，下载合适自己的版本的pywin32可执行安装文件并安装。

### 3.安装jieba
- 请先于控制台运行`easy_install jieba`或者`pip install jieba`/`pip3 install jieba`，或者将jieba-0.39.zip解压，然后在解压文件夹路径下运行`python setup.py install`。
