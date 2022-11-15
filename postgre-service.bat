for /F "tokens=3 delims=: " %%H in ('sc query "postgresql-x64-15" ^| findstr "        STATE"') do (
  if /I "%%H" NEQ "RUNNING" (
   net start "postgresql-x64-15"
  ) else (
   net stop "postgresql-x64-15"
  )
)