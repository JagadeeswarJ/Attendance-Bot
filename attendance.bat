@echo off
setlocal enabledelayedexpansion

:: Change to project directory
e:
cd "E:\079_data\Skills\projects\Attendance-Bot"

:: Run the Node.js script
node fetchAttendance.util.js > output.txt

:: Prepare sanitized result string for HTML
set "result="
for /f "delims=" %%a in ('type output.txt') do (
    set "line=%%a"
    set "line=!line:<=^&lt;!"
    set "line=!line:>=^&gt;!"
    set "line=!line:&=^&amp;!"
    set "line=!line:"=^&quot;!"
    set "result=!result!!line!<br>"
)

:: Write script to update the result in the HTA
> update.js echo var resultDiv = document.getElementById('result');
>> update.js echo resultDiv.innerHTML = "!result!";
>> update.js echo resultDiv.style.display = 'block';
>> update.js echo document.querySelector('h2').innerText = 'Attendance Report';

:: Inject into HTA
type update.js >> "E:\079_data\scripts\attendance.hta"

:: Cleanup
del output.txt
del update.js
exit
