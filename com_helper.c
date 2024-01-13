#include <stdlib.h>
#include <stdio.h>

int main()
{
    // PowerShell command as a string
    char command[] = "powershell -Command \"Get-WmiObject Win32_PnPEntity | Where-Object { $_.Name -match 'COM\\d+' } | Select-Object Caption, DeviceID\"";

    // Execute the command and redirect output to a file
    int result = system(command);

    // Check the result
    if (result == 0)
    {
        printf("Command %u\n", result);
    }
    else
    {

        printf("Error executing command.\n");
    }

    return 0;
}
