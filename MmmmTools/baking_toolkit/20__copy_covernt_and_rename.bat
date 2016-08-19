
echo Copying and renaming files, please wait...

REM     Object space and will be 16 bit, tangent space 8bit
REM     Also fix the case problem, where it makes TIF instead of tif
echo ...progressing...
c:\program_portables\appps\imagemagick\convert.exe "c:\Users\Joe\Desktop\low_normals.tif" "c:\Users\Joe\Desktop\low_normals.png"
echo ...progressing...
c:\program_portables\appps\imagemagick\convert.exe "c:\Users\Joe\Desktop\low_normals_unity.tif" -depth 8 "c:\Users\Joe\Desktop\low_normals_unity.png"
rename c:\Users\Joe\Desktop\low_normals_unity.TIF low_normals_unity_tmp_for_rename.TIF
rename c:\Users\Joe\Desktop\low_normals_unity_tmp_for_rename.TIF low_normals_unity.tif
rename c:\Users\Joe\Desktop\low_normals_unity.PNG low_normals_unity_tmp_for_rename.PNG
rename c:\Users\Joe\Desktop\low_normals_unity_tmp_for_rename.PNG low_normals_unity.png



echo ...progressing...
copy /y "c:\Users\Joe\Desktop\low_ts_normals.TIF" "c:\Users\Joe\Desktop\low_normals_ts.tif"

echo ...progressing...
c:\program_portables\appps\imagemagick\convert.exe "c:\Users\Joe\Desktop\low_normals_ts.tif" -depth 8 "c:\Users\Joe\Desktop\low_normals_ts.png"
echo ...progressing...
REM     Other map types
copy /y "c:\Users\Joe\Desktop\low_baseTexBaked.tif" "c:\Users\Joe\Desktop\low_base.tif"
c:\program_portables\appps\imagemagick\convert.exe "c:\Users\Joe\Desktop\low_base.tif" "c:\Users\Joe\Desktop\low_base.png"
copy /y "c:\Users\Joe\Desktop\low_base.png" "c:\Users\Joe\Desktop\low_baseTexBaked.png" 

echo ...progressing...
c:\program_portables\appps\imagemagick\convert.exe "c:\Users\Joe\Desktop\low_occlusion.tif" "c:\Users\Joe\Desktop\low_occlusion.png"
echo ...progressing...
c:\program_portables\appps\imagemagick\convert.exe "c:\Users\Joe\Desktop\low_curvature.tif" "c:\Users\Joe\Desktop\low_curvature.png"
echo ...progressing...
c:\program_portables\appps\imagemagick\convert.exe "c:\Users\Joe\Desktop\low_cavity.tif" "c:\Users\Joe\Desktop\low_cavity.png"
echo ...progressing...
c:\program_portables\appps\imagemagick\convert.exe "c:\Users\Joe\Desktop\low_convexity.tif" "c:\Users\Joe\Desktop\low_convexity.png"
echo ...progressing...
c:\program_portables\appps\imagemagick\convert.exe "c:\Users\Joe\Desktop\low_vcols.tif" "c:\Users\Joe\Desktop\low_vcols.png"
echo ...progressing...


echo ...progressing...
echo Done!
pause