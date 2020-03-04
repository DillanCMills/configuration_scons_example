"""SCons.Tool.xrun
 
Tool-specific initialization for the Xcelium compiler.
 
There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.
"""
import os
from SCons.Script import *
 
######################################################################
# BUILDERS:
######################################################################
### xrun
def generate_xrun(source, target, env, for_signature):
  action = [env['XRUN'], '-elaborate']
  for s in source:
    if os.path.splitext(str(s))[1] == '.f':
      action.append('-F')
    elif 'libmap' in str(s):
      action.append('-libmap')
    action.append(str(s))
 
  action.extend([
    '-xmlibdirname ${TARGET.dir}/${WORK}',
    '-history_file ${TARGET.dir}/xrun.history',
  ])
  action.extend(env['XRUN_ARGS'])
  action.extend(['-l $TARGET'])
 
  return ' '.join(action)
 
def Xrun(env, target, source, *args, **kw):
  """A pseudo-Builder wrapper for the xrun executable."""
 
  _xrun_builder = Builder(generator=generate_xrun, suffix='.log')
 
  result = _xrun_builder.__call__(env, target, source, **kw)
 
  # Ensures multiple xrun calls don't attempt to write to the work directory simultaneously.
  env.SideEffect(str(result[0].dir)+'/${WORK}/run.d/cds.lib', result[0])
 
  # Removes the work directory and the .history files, in addition to the logfile
  env.Clean(result, [
    str(result[0].dir)+'/${WORK}',
    env.Glob(str(result[0].dir)+'/*.history')
  ])
 
  return result
 
 
### xrun_sim
def generate_xrun_sim(source, target, env, for_signature):
  action = [env['XRUN_SIM'], '-R']
 
  action.extend([
    '-xmlibdirname ${TARGET.dir}/${WORK}',
    '-history_file ${TARGET.dir}/xrun.history',
  ])
  action.extend(env['XRUN_SIM_ARGS'])
  action.extend(['-l $TARGET'])
 
  return ' '.join(action)
 
def Xrun_sim(env, target, source, *args, **kw):
  """A pseudo-Builder wrapper for the xrun_sim executable."""
 
  _xrun_sim_builder = Builder(generator=generate_xrun_sim, suffix='.log')
 
  result = _xrun_sim_builder.__call__(env, target, source, **kw)
 
  return result
 
 
### xrun_all
def generate_xrun_all(source, target, env, for_signature):
  action = [env['XRUN_ALL']]
 
  for s in source:
    if os.path.splitext(str(s))[1] == '.f':
      action.append('-F')
    elif 'libmap' in str(s):
      action.append('-libmap')
    action.append(str(s))
 
  action.extend([
    '-xmlibdirname ${TARGET.dir}/${WORK}',
    '-history_file ${TARGET.dir}/xrun.history',
  ])
  action.extend(env['XRUN_ALL_ARGS'])
  action.extend(['-l $TARGET'])
 
  return ' '.join(action)
 
def Xrun_all(env, target, source, *args, **kw):
  """A pseudo-Builder wrapper for the xrun_all executable."""
 
  _xrun_all_builder = Builder(generator=generate_xrun_all, suffix='.log')
 
  result = _xrun_all_builder.__call__(env, target, source, **kw)
 
  # Removes the work directory and the .history files, in addition to the logfile
  env.Clean(result, [
    str(result[0].dir)+'/${WORK}',
    env.Glob(str(result[0].dir) + '/*.history'),
  ])
  return result
 
 
######################################################################
# TOOL FUNCTIONS:
#   generate() and exists() are required by SCons
######################################################################
def generate(env):
  """Add Builders and construction variables to the Environment."""
 
  env['XRUN'] = env.WhereIs('xrun')
  env['XRUN_SIM'] = env.WhereIs('xrun')
  env['XRUN_ALL'] = env.WhereIs('xrun')
 
  env.SetDefault(
    SIM_DIR='./',
    WORK='work',
    XRUN_ARGS=[],
    XRUN_SIM_ARGS=[],
    XRUN_ALL_ARGS=[],
  )
 
  env.AddMethod(Xrun, "Com")
  env.AddMethod(Xrun_sim, "Sim")
  env.AddMethod(Xrun_all, "AllIn1")
 
def exists(env):
  return True
