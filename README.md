# flask_document_system

### 一、说明

这是一个文档系统，可以用来管理pdf、html文档，启动系统后，对这些文档你可以在页面上增加、删除、重命名文档，并且可以对文档进行归类。

作者：岐山凤鸣（Ecohnoch）

### 二、启动系统

启动前需要配置mongodb数据库，配置好用于存放文档信息的数据库名称、数据库端口、访问数据库用户名和密码。

并且根据这些配置，修改configs下对应的配置。

配置好数据库并且相关的配置都设置成功后，即可直接运行run.py就可以启动文档系统了。

启动后直接访问：ip:端口/docs

例如： http://localhost:10086/docs

### 三、配置说明

上传的文档存放的路径在configs下的app_store_dir指定的位置，修改这个文件夹即可改变文档存放的路径。

如果需要用户登陆管理的话，接口都保留了，直接套层皮即可。


### 四、Docker部署

仓库拉下来之后，进入dockerfile文件夹，运行:

```
docker-compose up
```

等待便可构建好mongo和flask两个镜像，并且会直接运行。然后直接输入http://127.0.0.1:5000/docs即可。

注意：这里mongo镜像初始化是默认的管理员用户名密码+docs数据库用户名和密码，如果需要修改的话请修改dcokerfile/docker-compose.yml和dockerfile/mongo/setup.sh里的管理员用户名密码和docs数据库用户名和密码。

两个镜像：

flask: [https://hub.docker.com/repository/docker/ecohnoch/flask_document](https://hub.docker.com/repository/docker/ecohnoch/flask_document)

mongo: [https://hub.docker.com/repository/docker/ecohnoch/mongo](https://hub.docker.com/repository/docker/ecohnoch/mongo)