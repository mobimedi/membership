echo 清理

rmdir /S /Q build
rmdir /S /Q dist
del /F /Q membershipaio.spec

pause

echo 打包
pyinstaller all-in-one.py --clean -w -F -n membershipaio -i app.ico --version-file version.txt
copy /Y app.ico dist
