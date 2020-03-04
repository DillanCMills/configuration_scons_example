"""SCons.Tool.vcs
 
Tool-specific initialization for the VCS compiler.
 
There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.
"""
import os
from SCons.Script import *
 
######################################################################
# BUILDERS:
######################################################################
### vlogan
def generate_vlogan(source, target, env, for_signature):
  action = [env['VLOGAN']]
  for s in source:
    if os.path.splitext(str(s))[1] == '.f':
      action.append('-F')
    elif 'libmap' in str(s):
      action.append('-libmap')
    action.append(str(s))
 
  action.extend(env['VLOGAN_ARGS'])
  action.extend(['-l $TARGET'])
 
  return ' '.join(action)
 
def Vlogan(env, target, source, *args, **kw):
  """A pseudo-Builder wrapper for the vlogan executable."""
 
  _vlogan_builder = Builder(generator=generate_vlogan, suffix='.log')
 
  result = _vlogan_builder.__call__(env, target, source, **kw)
 
  # Ensures multiple vlogan calls don't attempt to write to the work directory simultaneously.
  env.SideEffect(str(result[0].dir)+'/${WORK}/AN.DB/.vcs_lib_lock', result[0])
 
  # Removes the .done file and the work directory, in addition to the logfile
  env.Clean(result, [
    str(result[0].dir) + '/${WORK}',
    '.vlogansetup.args',
  ])
 
  return result
 
### vcs
def generate_vcs(source, target, env, for_signature):
  action = [env['VCS'], '-R']
 
  action.extend([
    '-Mdir=${TARGET.dir}/csrc',
    '-o ${TARGET.dir}/simv',
  ])
  action.extend(env['VCS_ARGS'])
  action.extend(['-l $TARGET'])
 
  return ' '.join(action)
 
def Vcs(env, target, source, *args, **kw):
  """A pseudo-Builder wrapper for the vcs executable."""
 
  _vcs_builder = Builder(generator=generate_vcs, suffix='.log')
 
  result = _vcs_builder.__call__(env, target, source, **kw)
 
  # Removes the .done file and the logfile
  env.Clean(result, [
    str(result[0].dir)+'/csrc',
    str(result[0].dir)+'/simv',
    str(result[0].dir)+'/simv.daidir',
  ])
 
  return result
 
 
######################################################################
# TOOL FUNCTIONS:
#   generate() and exists() are required by SCons
######################################################################
def generate(env):
  """Add Builders and construction variables to the Environment."""
 
  env['VLOGAN'] = env.WhereIs('vlogan')
  env['VCS'] = env.WhereIs('vcs')
 
  env.SetDefault(
    SIM_DIR='./',
    WORK='work',
    TOP_TB='top',
    VLOGAN_ARGS=['-sverilog'],
    VCS_ARGS=[],
  )
 
  env.AddMethod(Vlogan, "Com")
  env.AddMethod(Vcs, "Sim")
 
def exists(env):
  return True
