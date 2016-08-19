@echo off
echo "Running xnormal and baking based on xml files"

REM   Unfortunately, xnormal doesn't cache high obj between xmls
REM    so there's not benefit in running it all at once
REM    but there is of course the minor beneit of not restart xnormal
REM    since it does take a bit of time to start
REM
"C:\Program Files\Santiago Orgaz\xNormal 3.18.10\x64\xnormal.exe" c:\users\joe\Desktop\xnormal_bake_normals_os.xml c:\Users\joe\Desktop\xnormal_bake_normals_ts.xml c:\Users\joe\Desktop\xnormal_bake_vcols.xml c:\Users\joe\Desktop\xnormal_bake_base.xml c:\Users\joe\Desktop\xnormal_bake_ao_cavity_convexity_curvature.xml c:\Users\joe\Desktop\xnormal_bake_smooth_height_as_raw_float_exr.xml c:\Users\joe\Desktop\xnormal_bake_ao_cavity_convexity_curvature_as_exr.xml

REM "C:\Program Files\Santiago Orgaz\xNormal 3.18.10\x64\xnormal.exe" c:\users\joe\Desktop\xnormal_bake_normals_os.xml 
REM "C:\Program Files\Santiago Orgaz\xNormal 3.18.10\x64\xnormal.exe" c:\Users\joe\Desktop\xnormal_bake_normals_ts.xml
REM "C:\Program Files\Santiago Orgaz\xNormal 3.18.10\x64\xnormal.exe" c:\Users\joe\Desktop\xnormal_bake_vcols.xml

REM "C:\Program Files\Santiago Orgaz\xNormal 3.18.10\x64\xnormal.exe" c:\Users\joe\Desktop\xnormal_bake_smooth_height_as_raw_float_exr.xml
REM "C:\Program Files\Santiago Orgaz\xNormal 3.18.10\x64\xnormal.exe" c:\Users\joe\Desktop\xnormal_bake_ao_cavity_convexity_curvature.xml
REM "C:\Program Files\Santiago Orgaz\xNormal 3.18.10\x64\xnormal.exe" c:\Users\joe\Desktop\xnormal_bake_ao_cavity_convexity_curvature_as_exr.xml



REM     Fix the case problem, where it makes TIF instead of tif
copy /y c:\Users\Joe\Desktop\low_normals_unity.TIF c:\Users\Joe\Desktop\low_normals_unity_tmp.TIF
copy /y c:\Users\Joe\Desktop\low_normals_unity_tmp.TIF c:\Users\Joe\Desktop\low_normals_unity.tif

copy /y c:\Users\Joe\Desktop\low_normals_unity.PNG c:\Users\Joe\Desktop\low_normals_unity_tmp.PNG
copy /y c:\Users\Joe\Desktop\low_normals_unity_tmp.PNG c:\Users\Joe\Desktop\low_normals_unity.tif
del c:\Users\Joe\Desktop\low_normals_unity_tmp.PNG
del c:\Users\Joe\Desktop\low_normals_unity_tmp.TIF
