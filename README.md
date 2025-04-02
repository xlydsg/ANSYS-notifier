# ANSYS-notifier
# ANSYS 仿真自动通知系统 催命小工具
# 仿真完了给你发个通知
📨 **邮件+微信双通道通知**

[![GitHub stars](https://img.shields.io/github/stars/xlydsg/ANSYS-notifier?style=social)](https://github.com/xlydsg/ANSYS-notifier) 

- 实时监控 ANSYS 仿真进度
- 支持邮件+微信双通道提醒
- Ansys 2021r2 测试通过
- 把ansys的ironpy和发邮件用的ps脚本分离了。因为我在2021r2的测试中发现自带的.net库妹有smtp mail的dll哈哈哈。直接调用一下powershell绕过了这个问题
- 大部分都是用deepseek生成的，有啥bug问deepseek就好

## 🛠️ 快速配置

### 1. 邮箱设置（以163邮箱为例）
```python
command = """
powershell -ExecutionPolicy Bypass -File "{0}" `
-smtpServer "smtp.163.com" `
-smtpPort 25 `                  # 25端口不带ssl加密
-fromEmail "[您的邮箱地址]" `    # 例：yourname@163.com
-toEmail "[接收邮箱]" `          # 例：notify@qq.com
-password "[邮箱授权码]"         # 获取方式：网页邮箱 > 设置 > SMTP  授权码 ≠ 登录密码，需通过邮箱网页生成
"""
```


### 2. 微信通知配置
```python
SCKEY = "[您的SCKEY]"  # 前往 https://sct.ftqq.com 申请
```

🚀 使用指南

将脚本放入 HFSS 工程目录

把仿真开始代码段插入通知触发点这个位置：
```python
# simulation code here
# oProject = oDesktop.NewProject()
# oDesign = oProject.InsertDesign("HFSS", "MyDesign", "", "")
# oDesign.Analyze("Setup1")
```

🔧 PowerShell 需开启脚本执行权限：

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```
📶 确保运行环境可访问外网

⏱️ 企业邮箱建议使用SSL加密（端口465），参考邮箱说明

🧷 常见问题

Q：收不到微信通知？

A：检查 Server 酱消息队列 https://sct.ftqq.com/forward

Q：邮件发送超时？

A：尝试关闭防火墙临时测试：

```powershell
Test-NetConnection smtp.163.com -Port 25
```

Q：如何验证脚本权限？

A：在 PowerShell 中运行：

```powershell
Get-ExecutionPolicy -List
```
