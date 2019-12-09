# RQAMS 助手

[RQAMS](https://www.ricequant.com/welcome/ams) 是由米筐科技开发的，集多资产管理、实时监控、绩效分析、风险分析等多种功能于一体的智能投资组合管理平台。

RQAMS 助手是一个简单的客户端，用于连接资金账号并把资金账号产生的交割单自动同步到 RQAMS 系统。资金账号在本地连接，密码等关键信息不会上传到服务器，保证资金安全。

已支持的交易平台:
* CTP


## 运行环境

* windows 64-bit

## 构建环境

* windows 64-bit
* python 3.6

构建安装包所需的依赖：

* 安装 [Inno Setup](http://www.jrsoftware.org/isinfo.php)
* 下载 [Inno Setup 的中文本地化文件](https://raw.github.com/jrsoftware/issrc/master/Files/Languages/Unofficial/ChineseSimplified.isl) 并将其置于安装目录
* 添加 Inno Setup 的安装目录至 PATH

## 构建步骤

### 运行

```cmd
make run
```

### 构建安装包

```cmd
make build
```

