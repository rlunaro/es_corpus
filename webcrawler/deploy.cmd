rem
rem deploy.cmd
rem 

set local_copy=1
set dest="PUT-HERE-THE-DESTINATION-ADDRESS"
rem set dest="ec2-user@PUT-HERE-THE-IP:/PUT/HERE/THE/DESTINATION/PATH"
rem set pwd="PUT-HERE-THE-PASSWORD"

if "%local_copy%" == "1" (
	rem copy "src\*.py" %dest%
	rem copy "00_template.cmd" %dest%
	rem copy "00_template.sh" %dest%
) else (
	rem pscp -pw %pwd% "src\*.py" %dest%
	rem pscp -pw %pwd% "00_template.cmd" %dest%
	rem pscp -pw %pwd% "00_template.sh" %dest%
)




