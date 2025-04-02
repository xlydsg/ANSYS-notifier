<#
仿真完成邮件通知脚本
#>

param(
    [string]$smtpServer = "smtp.163.com",
    [int]$smtpPort = 25,
    [string]$fromEmail = "xxxxxxxxxxxx@163.com",
    [string]$toEmail = "xxxxxxxxxxxx@qq.com",
    [string]$emailSubject = "HFSS Simulation Notification",
    [string]$emailBody = "Simulation finished",
    [string]$password = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
)

try {
    # 创建 SMTP 客户端
    $smtp = New-Object System.Net.Mail.SmtpClient($smtpServer, $smtpPort)
    $smtp.EnableSsl = $false
    $smtp.Credentials = New-Object System.Net.NetworkCredential($fromEmail, $password)

    # 创建邮件对象
    $mail = New-Object System.Net.Mail.MailMessage
    $mail.From = $fromEmail
    $mail.To.Add($toEmail)
    $mail.Subject = $emailSubject
    $mail.Body = $emailBody

    # 发送邮件
    $smtp.Send($mail)
    Write-Output "[SUCCESS] Email sent to $toEmail"
    exit 0
}
catch {
    Write-Output "[ERROR] $_"
    exit 1
}
finally {
    if ($smtp -ne $null) { $smtp.Dispose() }
    if ($mail -ne $null) { $mail.Dispose() }
}