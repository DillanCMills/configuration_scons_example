"""SCons.site_init
 
SCons site_init file
 
There normally shouldn't be any need to import this module directly,
it will usually be imported by SCons automatically.
"""
import os, re, subprocess
 
 
######################################################################
# OPTIONS:
#   Add all command line options here (-o, --option)
######################################################################
 
AddOption('--tool',
          dest='tool',
          type='choice',
          choices=['vcs', 'vsim', 'xrun'],
          nargs=1,
          action='store',
          default='vsim',
          help='The vendor tool to use [vcs|vsim|xrun]. Default: vsim')
 
 
AddOption('--svconfig',
          dest='svconfig',
          type='choice',
          choices=['', '1', '2'],
          nargs=1,
          action='store',
          default='',
          help='The alternate configuration to use [1|2]. Default: None')
 
 
######################################################################
# SCANNERS:
#   Scanners to parse .f files and .sv files for dependencies
######################################################################
f_re = re.compile(r'^-f\s+(\S+\.f)$', re.M | re.I)
sv_re = re.compile(r'^(/?[^/+]\S+\.s?vh?)$', re.M | re.I)
include_re = re.compile(r'^\s*`include\s+"(\S+)"$', re.M | re.I)
 
def ffile_scan(node, env, path, arg=None):
  contents = node.get_text_contents()
 
  sv_files = sv_re.findall(contents)
  sv_files = [sv.strip() for sv in sv_files]
  f_files = f_re.findall(contents)
 
  while f_files:
    for f in f_files:
      # We use the following line to expand any environment variables in the filepath using
      # our custom SCons environment. This will catch any variables declared in the SConstruct.
      ef = subprocess.check_output('echo ' + f, shell=True, env=env['ENV']).strip()
      if os.path.isfile(ef):
        current_dir = os.path.dirname(ef) + '/'
        contents = env.File(ef).get_text_contents()
 
        sv_files.extend([(current_dir + x.strip()) for x in sv_re.findall(contents)])
        f_files.extend([(current_dir + x.strip()) for x in f_re.findall(contents)])
        sv_files.append(str(ef))
      f_files.remove(f)
 
  results = []
  for f in env.File(sv_files):
    results.extend(svfile_scan(f, env, path, arg))
 
  return results
 
def svfile_scan(node, env, path, arg=None):
  contents = node.get_text_contents()
  includes = include_re.findall(contents)
 
  starting_dir = str(node.dir) + '/'
 
  if includes == []:
    return [node]
 
  results = [str(node)]
  for inc in includes:
    if os.path.exists(starting_dir + inc):
      results.append(starting_dir + inc)
 
  return env.File(results)
 
svscan = Scanner(
  name='svfile',
  function=svfile_scan,
  argument=None,
  skeys=['.v', '.vh', '.sv', '.svh'])
 
fscan = Scanner(
  name='ffile',
  function=ffile_scan,
  argument=None,
  skeys=['.f'])
 
scanners = Environment().Dictionary('SCANNERS')
