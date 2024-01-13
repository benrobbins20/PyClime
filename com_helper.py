import subprocess
import re

# PowerShell command as a string
command = "Get-WmiObject Win32_PnPEntity | Where-Object { $_.Name -match 'COM\d+' } | Select-Object Caption, DeviceID, Manufacturer, SystemName"

# Execute the command
process = subprocess.Popen(["powershell", "-Command", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

# Decode and print the output
if process.returncode == 0:
    # Decode the byte string
    output = stdout.decode('utf-8')
    print(output)
else:
    print("Error:", stderr.decode('utf-8'))
