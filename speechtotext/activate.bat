SET mypath=%~dp0
call conda activate %mypath%./envs
cd /d %mypath%
cmd /k