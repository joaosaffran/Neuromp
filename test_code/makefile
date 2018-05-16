OUT?=a.out
icc: 
	gcc -std=c99 -O3 -parallel -par-threshold0 -qopt-report-phase=par -qopt-report:5  $(FILE) -o $(OUT)
	install_name_tool -change @rpath/libiomp5.dylib /opt/intel/compilers_and_libraries/mac/lib/libiomp5.dylib $(OUT)
	
neuromp:
	gcc -std=c99 -O3 -fopenmp $(FILE) -o $(OUT)
	#install_name_tool -change @rpath/libiomp5.dylib /opt/intel/compilers_and_libraries/mac/lib/libiomp5.dylib $(OUT)

seq:
	gcc -std=c99 -O3 $(FILE) -o $(OUT)
