echo clear...

rmdir /S /Q build
rmdir /S /Q dist
del /F /Q membershipaio.spec

pause

echo pack...

pyinstaller moas.py --clean -w -F -n moas -i moas.ico --version-file version.txt

pause
