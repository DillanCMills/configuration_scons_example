"""SCons.Tool.vsim
 
Tool-specific initialization for the Questa compiler.
 
There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.
"""
import os
from SCons.Script import *
 
######################################################################
# BUILDERS:
######################################################################
### vlog
def generate_vlog(source, target, env, for_signature):
  action = [env['VLOG']]
  for s in source:
    if os.path.splitext(str(s))[1] == '.f':
      action.append('-F')
    elif 'libmap' in str(s):
      action.append('-libmap')
    action.append(str(s))
 
  action.extend(['-work ${TARGET.dir}/${WORK}'])
  action.extend(env['VLOG_ARGS'])
  action.extend(['-l $TARGET'])
 
  return ' '.join(action)
 
def Vlog(env, target, source, *args, **kw):
  """A pseudo-Builder wrapper for the vlog executable."""
 
  _vlog_builder = Builder(generator=generate_vlog, suffix='.log')
 
  result = _vlog_builder.__call__(env, target, source, **kw)
 
  # Ensures multiple vlog calls don't attempt to write to the work directory simultaneously.
  env.SideEffect(str(result[0].dir)+'/${WORK}/_lib.qdb', result[0])
 
  # Removes the .done file and the work directory, in addition to the logfile
  env.Clean(result, ['.done', str(result[0].dir)+'/${WORK}'])
 
  return result
 
### vsim
def generate_vsim(source, target, env, for_signature):
  action = [env['VSIM']]
 
  action.extend(['-lib ${TARGET.dir}/${WORK}'])
  action.extend(env['VSIM_ARGS'])
  action.extend(['-l $TARGET'])
 
  return ' '.join(action)
 
def Vsim(env, target, source, *args, **kw):
  """A pseudo-Builder wrapper for the vsim executable."""
 
  _vsim_builder = Builder(generator=generate_vsim, suffix='.log')
 
  result = _vsim_builder.__call__(env, target, source, **kw)
 
  # Removes the .done file and the logfile
  env.Clean(result, ['.done'])
 
  return result
 
 
######################################################################
# TOOL FUNCTIONS:
#   generate() and exists() are required by SCons
######################################################################
def generate(env):
  """Add Builders and construction variables to the Environment."""
 
  env['VLOG'] = env.WhereIs('vlog')
  env['VSIM'] = env.WhereIs('vsim')
 
  env.SetDefault(
    SIM_DIR='./',
    WORK='work',
    VLOG_ARGS=[],
    VSIM_ARGS=[],
  )
 
  env.AddMethod(Vlog, "Com")
  env.AddMethod(Vsim, "Sim")
 
def exists(env):
  return True
