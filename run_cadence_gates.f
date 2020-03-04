###########
# Cleanup old runs and enable elaboration debugging
-clean
-cleanlib
-libverbose
 
##########
# Compile and design configuration management files
# design configuration compiled into "worklib"
-libmap libmap_gates.sv 
-compcnfg configs.sv
 
##########
# Source Code
-f source_code.f
