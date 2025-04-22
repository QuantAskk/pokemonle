## 说明

本项目是由个人开发的猜宝可梦小网站，灵感来源于CS猜职业选手（也称弗一把）。

数据来源为 [神奇宝贝百科](https://wiki.52poke.com/wiki/%E4%B8%BB%E9%A1%B5) 与 https://github.com/42arch/pokemon-dataset-zh 。

由于个人水平有限所以可能会出现许多意料之外的 bug ，欢迎在 Issues 提出。

视频：[https://www.bilibili.com/video/BV1XmLFz5E7Y](https://www.bilibili.com/video/BV1XmLFz5E7Y)

## 部署指南

#### 环境要求

- vue >= 5.0.8
- npm >= 10.2.1
- Python >= 3.12.0

### 部署步骤

#### 后端部署

1. 安装 flask 与 flask_cors 库

   ```
   pip install flask
   pip install flask_cors 
   ```

2. 更改后端文件路径：

打开 serve/src/utils/dataUtils.py 将第3行的

```python
root=xxx
```

中的 `xxx` 更改为 serve/src/app.py 所处文件夹的绝对路径

3. 更改 ip 与端口（默认为9000端口，可选）

打开 serve/src/app.py 将第 58 行的

```
app.run(host='0.0.0.0',port=9000)
```

更改为自己服务器所处ip与需要监听的端口

4. 启动后端服务器

使用 python 运行 serve/src/app.py 

#### 前端部署

1. 修改后端服务器url

打开 web/.env 文件，将其中的 `VUE_APP_API_BASE_URL` 环境变量更改为刚刚运行的后端服务器监听地址

2. 打包前端网页

在 web 文件夹下使用 cmd 运行

```
npm run build
```

之后打开 web/dist/index.html 检查是否打包成功。
