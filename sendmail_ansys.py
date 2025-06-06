# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Version 2021.2.0
# ----------------------------------------------
import sys
import os
import clr
clr.AddReference("System")
clr.AddReference("System.Net")
from System.Net import WebClient
from System.Diagnostics import Process, ProcessStartInfo

import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()

def send_email(subject="HFSS Simulation Notification", body="Simulation finished"):
    ps_script_path = os.path.join(os.path.dirname(__file__), "sendmail.ps1")
    
    if not os.path.exists(ps_script_path):
        AddInfoMessage("Error: PowerShell script not found "+ ps_script_path)
        return False

    try:
        command = """
        powershell -ExecutionPolicy Bypass -File "{0}" `
        -smtpServer "smtp.163.com" `
        -smtpPort 25 `
        -fromEmail "[您的邮箱地址]" `
        -toEmail "[接收邮箱]" `
        -emailSubject "{1}" `
        -emailBody "{2}" `
        -password "[邮箱授权码]"
        """.format(ps_script_path, subject.replace('"', '`"'), body.replace('"', '`"'))

        p = Process()
        p.StartInfo = ProcessStartInfo()
        p.StartInfo.FileName = "powershell.exe"
        p.StartInfo.Arguments = command
        p.StartInfo.UseShellExecute = False
        p.StartInfo.RedirectStandardOutput = True
        p.Start()
        
        output = p.StandardOutput.ReadToEnd()
        p.WaitForExit()
        
        AddInfoMessage("Mail send output "+ output.strip())
        return p.ExitCode == 0

    except Exception as e:
        AddWarningMessage("Mail send failed:"+ str(e))
        return False

def send_serverchan(text, text2):
    SCKEY = "[您的SCKEY]"
    url = "https://sctapi.ftqq.com/{}.send".format(SCKEY) 
    wc = WebClient()
    wc.Headers.Add("Content-Type", "application/x-www-form-urlencoded")
    post_data = "title=" + text +"&desp=" + text2
    try:
        response = wc.UploadString(url, "POST", post_data)
        AddInfoMessage("ServerChan:"+ response)
        return True
    except Exception as e:
        AddWarningMessage("ServerChan failed:"+ str(e))
        return False 

try:
    # simulation code here
    # oProject = oDesktop.NewProject()
    # oDesign = oProject.InsertDesign("HFSS", "MyDesign", "", "")
    # oDesign.Analyze("Setup1")
    oDesktop.ClearMessages("","",3)
    oProject = oDesktop.SetActiveProject("20250331_TimeDomainSimulationTest")
    oDesign = oProject.SetActiveDesign("0052_00_FullChainDC_includeLC_test")
    oDesign.Analyze("Setup2")
    oProject.Save()
    e = oDesktop.GetMessages("","",0)
    # oModule = oDesign.GetModule("Optimetrics")
    # oModule.SolveSetup("ParametricSetup2")
    # oProject.Save()
    # oDesign.AnalyzeAll()

    
    # if send_email("HFSS Simulation Notification", "Simulation finished"):
    #     AddInfoMessage("mail send success")
    # else:
    #     AddWarningMessage("mail send failed")

    if send_serverchan("HFSS Simulation finished", str(e)):
        AddInfoMessage("ServerChan send success")
    else:
        AddWarningMessage("ServerChan send failed")

except Exception as e:
    AddErrorMessage("Simulation failed: " + str(e))
    #send_email() #simulation failed
    if send_serverchan("simulation error ", str(e)):
        AddInfoMessage("ServerChan send success")
    else:
        AddWarningMessage("ServerChan send failed")


finally:
    ScriptEnv.Shutdown()
