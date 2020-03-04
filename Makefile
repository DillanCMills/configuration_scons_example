all  :
	make -j -f Makefile.mentor   
	make -j -f Makefile.cadence  
	make    -f Makefile.synopsys 
	make    -f Makefile.mentor   clean
	make    -f Makefile.cadence  clean
	make    -f Makefile.synopsys clean
 
clean:
	make -f Makefile.mentor   clean
	make -f Makefile.cadence  clean
	make -f Makefile.synopsys clean
