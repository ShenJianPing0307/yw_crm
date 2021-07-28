# yw_crm
根据制造公司实际情况，开发的基于客户关系、生产流程等的管理系统

基于`python3.5.2`和`Django2.0`的CRM。 

## 主要功能：

- 基于Django-admin进行定制化开发
- 基于rbac进行权限控制

## 安装

- 安装python3.5.2
- 安装Django2.0

## 运行

修改`yw_crm/setting.py` 数据库配置，如下所示：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yw_crm',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
生成数据库表：
```shell
python manage.py makemigrations
python manage.py migrate
```


