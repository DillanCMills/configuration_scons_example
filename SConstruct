EnsureSConsVersion(3, 0) # for Help() append
 
######################
# File: SConstruct   #
######################
 
Help('''
Main SConstruct for configurations:
 
Runs all three SConstruct.<vendor> files in parallel using the num_jobs option.
Some of these will fail due to overwriting the work libraries - additional
steps would need to be taken to ensure each compile step uses a distinct work
library.
 
Run "scons -n" to see all the commands this file would run printed out.
 
Run "scons -c" to clean everything.
''', append=True) # Only works on newer install of SCons
# See the help text in each sub-file if using an older version of SCons
 
env = Environment()
 
# Default to -j 8
SetOption('num_jobs', 8)
 
# See individual scons files for help:
# scons -f SConstruct.cadence -h
SConscript('SConstruct.cadence')
SConscript('SConstruct.mentor')
SConscript('SConstruct.synopsys')
