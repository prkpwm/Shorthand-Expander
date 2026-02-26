Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = WScript.Arguments(1) & "\Shorthand Expander.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = WScript.Arguments(0)
oLink.WorkingDirectory = WScript.Arguments(1)
oLink.IconLocation = WScript.Arguments(0) & ",0"
oLink.Description = "Shorthand Expander - Text expansion tool"
oLink.Save
WScript.Echo "Shortcut created successfully at: " & sLinkFile
