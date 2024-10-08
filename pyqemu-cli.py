#!/usr/bin/python

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2015 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2015 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: qemu-cli.py - Last Update: 4/07/2015 Ver. 0.0.1 RC 1 - Author: cooldude2k $
'''

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import re
import subprocess
import sys

__project__ = "PyQEMU-CLI"
__version_info__ = (0, 0, 1, "RC 1")
if (__version_info__[3] is not None):
    __version__ = "{major}.{minor}.{build} {release}".format(
        major=__version_info__[0],
        minor=__version_info__[1],
        build=__version_info__[2],
        release=__version_info__[3])
if (__version_info__[3] is None):
    __version__ = "{major}.{minor}.{build}".format(
        major=__version_info__[0],
        minor=__version_info__[1],
        build=__version_info__[2])
__version_alt__ = "{major}.{minor}.{build}".format(
    major=__version_info__[0],
    minor=__version_info__[1],
    build=__version_info__[2])

qemuimgexecname = "qemu-img"
qemu64execname = "qemu-system-x86_64"
qemu32execname = "qemu-system-i386"
if (sys.platform == "win32"):
    qemuimgexecname = "qemu-img.exe"
    qemu64execname = "qemu-system-x86_64.exe"
    qemu32execname = "qemu-system-i386.exe"
if (len(sys.argv) == 1):
    cmdargpath = os.path.realpath(os.getcwd())
if (len(sys.argv) > 1):
    cmdargpath = sys.argv[1]
    if (not os.path.exists(cmdargpath)):
        cmdargpath = os.path.realpath(os.getcwd())
    cmdargpath = os.path.realpath(cmdargpath)
    if (not os.path.isdir(cmdargpath)):
        cmdargpath = os.path.dirname(os.path.realpath(cmdargpath))
    if (not os.path.exists(cmdargpath)):
        cmdargpath = os.path.realpath(os.getcwd())

os.environ["PATH"] = os.environ["PATH"] + os.pathsep + \
    os.path.dirname(os.path.realpath(__file__)) + os.pathsep + os.getcwd()


def which_exec(execfile):
    for path in os.environ["PATH"].split(":"):
        if os.path.exists(path + "/" + execfile):
            return path + "/" + execfile


def listize(varlist):
    il = 0
    ix = len(varlist)
    ilx = 1
    newlistreg = {}
    newlistrev = {}
    newlistfull = {}
    while (il < ix):
        newlistreg.update({ilx: varlist[il]})
        newlistrev.update({varlist[il]: ilx})
        ilx = ilx + 1
        il = il + 1
    newlistfull = {1: newlistreg, 2: newlistrev,
                   'reg': newlistreg, 'rev': newlistrev}
    return newlistfull


def twolistize(varlist):
    il = 0
    ix = len(varlist)
    ilx = 1
    newlistnamereg = {}
    newlistnamerev = {}
    newlistdescreg = {}
    newlistdescrev = {}
    newlistfull = {}
    while (il < ix):
        newlistnamereg.update({ilx: varlist[il][0].strip()})
        newlistnamerev.update({varlist[il][0].strip(): ilx})
        newlistdescreg.update({ilx: varlist[il][1].strip()})
        newlistdescrev.update({varlist[il][1].strip(): ilx})
        ilx = ilx + 1
        il = il + 1
    newlistnametmp = {1: newlistnamereg, 2: newlistnamerev,
                      'reg': newlistnamereg, 'rev': newlistnamerev}
    newlistdesctmp = {1: newlistdescreg, 2: newlistdescrev,
                      'reg': newlistdescreg, 'rev': newlistdescrev}
    newlistfull = {1: newlistnametmp, 2: newlistdesctmp,
                   'name': newlistnametmp, 'desc': newlistdesctmp}
    return newlistfull


def arglistize(proexec, *varlist):
    il = 0
    ix = len(varlist)
    ilx = 1
    newarglist = [proexec]
    while (il < ix):
        if varlist[il][0] is not None:
            newarglist.append(varlist[il][0])
        if varlist[il][1] is not None:
            newarglist.append(varlist[il][1])
        il = il + 1
    return newarglist


qemuimgllocatout = which_exec(qemuimgexecname)
qemuimghelplistp = subprocess.Popen(
    [qemuimgllocatout, '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
qemuimglhelpout, qemuimglhelperr = qemuimghelplistp.communicate()
qemuimglformatsprelist = re.findall(
    "Supported formats: ([\\w\\_ ]+)\n",
    qemuimglhelpout,
    flags=re.MULTILINE)[0]
qemuimglformatslist = qemuimglformatsprelist.split(" ")
qemuimglformatsnlist = listize(qemuimglformatslist)
qemuimglversion = re.findall(
    "^qemu-img version ([\\w\\_\\. \\-]+)\\,",
    qemuimglhelpout,
    flags=re.MULTILINE)[0].strip()


qemu32llocatout = which_exec(qemu32execname)
qemu32helplistp = subprocess.Popen(
    [qemu32llocatout, '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
qemu32lhelpout, qemu32lhelperr = qemu32helplistp.communicate()
qemu32lverfull = re.findall(
    "QEMU emulator version ([\\w\\_\\.\\+\\(\\) \\-]+)\\, Copyright",
    qemu32lhelpout,
    flags=re.MULTILINE)[0].strip()
qemu32lversion = re.findall(
    "([\\w\\_\\. \\-]+)", qemu32lverfull, flags=re.MULTILINE)[0].strip()
qemu32lvgaprelist = re.findall(
    "vga \\[([\\w\\|]+)\\]\n", qemu32lhelpout, flags=re.MULTILINE)[0]
qemu32lvgalist = qemu32lvgaprelist.split("|")
qemu32lvganlist = listize(qemu32lvgalist)
qemu32lrtcbaseprelist = re.findall(
    "\\[base\\=([\\w\\|]+)\\]", qemu32lhelpout, flags=re.MULTILINE)[0]
qemu32lrtcbaselist = qemu32lrtcbaseprelist.split("|")
qemu32lrtcbasenlist = listize(qemu32lrtcbaselist)
qemu32lrtcclockprelist = re.findall(
    "\\[\\,clock\\=([\\w\\|]+)\\]", qemu32lhelpout, flags=re.MULTILINE)[0]
qemu32lrtcclocklist = qemu32lrtcclockprelist.split("|")
qemu32lrtcclocknlist = listize(qemu32lrtcclocklist)
qemu32lrtcdriftfixprelist = re.findall(
    "\\[\\,driftfix\\=([\\w\\|]+)\\]", qemu32lhelpout, flags=re.MULTILINE)[0]
qemu32lrtcdriftlist = qemu32lrtcdriftfixprelist.split("|")
qemu32lrtcdriftnlist = listize(qemu32lrtcdriftlist)
qemu32cpulistp = subprocess.Popen(
    [qemu32llocatout, '-cpu', 'help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
qemu32lcpuout, qemu32lcpuerr = qemu32cpulistp.communicate()
qemu32lcpulist = re.findall(
    "^x86\\s\\s+([\\w]+)  ([\\s]+|[\\w\\(\\)\\.\\@\\_\\/ \\-]+)\n",
    qemu32lcpuout,
    flags=re.MULTILINE)
qemu32lcpunlist = twolistize(qemu32lcpulist)
qemu32machinelistp = subprocess.Popen(
    [qemu32llocatout, '-machine', 'help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
qemu32lmachineout, qemu32lmachineerr = qemu32machinelistp.communicate()
qemu32lmachinelist = re.findall(
    "^([\\w\\-\\.]+)\\s\\s+([\\w\\(\\)\\+\\,\\. \\-]+)\n",
    qemu32lmachineout,
    flags=re.MULTILINE)
qemu32lmachinenlist = twolistize(qemu32lmachinelist)
qemu32soundhwlistp = subprocess.Popen(
    [qemu32llocatout, '-soundhw', 'help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
qemu32lsoundhwout, qemu32lsoundhwerr = qemu32soundhwlistp.communicate()
qemu32lsoundhwlist = re.findall(
    "^([\\w]+)\\s\\s+([\\w\\(\\) ]+)\n", qemu32lsoundhwout, flags=re.MULTILINE)
qemu32lsoundhwlist.append(('all', 'Enable all sound cards'))
qemu32lsoundhwnlist = twolistize(qemu32lsoundhwlist)
qemu32larglist = arglistize(
    qemu32llocatout,
    ('-hda',
     '/dev/null'),
    ('-cdrom',
     '/home/cooldude2k/Emu/Minix3/minix_R3.3.0-588a35b.iso'),
    ('-boot',
     'order=acd,once=d,menu=on'),
    ('-cpu',
     qemu32lcpunlist['name']['reg'][9]),
    ('-machine',
     qemu32lmachinenlist['name']['reg'][16]),
    ('-soundhw',
     qemu32lsoundhwnlist['name']['reg'][8]),
    ('-sdl',
     None))
print("PATH environment variable is set to " + os.environ["PATH"])
print("Python " + sys.version)
print(__project__ + " version " + __version__)
print("QEMU emulator version " + qemu32lverfull)
print(qemu32larglist)
qemu32cmdlaunch = subprocess.Popen(
    qemu32larglist, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
qemu32cmdlaunch.wait()
print(str(qemu32cmdlaunch.returncode))
print("")


qemu64llocatout = which_exec(qemu64execname)
qemu64helplistp = subprocess.Popen(
    [qemu64llocatout, '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
qemu64lhelpout, qemu64lhelperr = qemu64helplistp.communicate()
qemu64lverfull = re.findall(
    "QEMU emulator version ([\\w\\_\\.\\+\\(\\) \\-]+)\\, Copyright",
    qemu64lhelpout,
    flags=re.MULTILINE)[0].strip()
qemu64lversion = re.findall(
    "([\\w\\_\\. \\-]+)", qemu64lverfull, flags=re.MULTILINE)[0].strip()
qemu64lvgaprelist = re.findall(
    "vga \\[([\\w\\|]+)\\]\n", qemu64lhelpout, flags=re.MULTILINE)[0]
qemu64lvgalist = qemu64lvgaprelist.split("|")
qemu64lvganlist = listize(qemu64lvgalist)
qemu64lrtcbaseprelist = re.findall(
    "\\[base\\=([\\w\\|]+)\\]", qemu64lhelpout, flags=re.MULTILINE)[0]
qemu64lrtcbaselist = qemu64lrtcbaseprelist.split("|")
qemu64lrtcbasenlist = listize(qemu64lrtcbaselist)
qemu64lrtcclockprelist = re.findall(
    "\\[\\,clock\\=([\\w\\|]+)\\]", qemu64lhelpout, flags=re.MULTILINE)[0]
qemu64lrtcclocklist = qemu64lrtcclockprelist.split("|")
qemu64lrtcclocknlist = listize(qemu64lrtcclocklist)
qemu64lrtcdriftfixprelist = re.findall(
    "\\[\\,driftfix\\=([\\w\\|]+)\\]", qemu64lhelpout, flags=re.MULTILINE)[0]
qemu64lrtcdriftlist = qemu64lrtcdriftfixprelist.split("|")
qemu64lrtcdriftnlist = listize(qemu64lrtcdriftlist)
qemu64cpulistp = subprocess.Popen(
    [qemu64llocatout, '-cpu', 'help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
qemu64lcpuout, qemu64lcpuerr = qemu64cpulistp.communicate()
qemu64lcpulist = re.findall(
    "^x86\\s\\s+([\\w]+)  ([\\s]+|[\\w\\(\\)\\.\\@\\_\\/ \\-]+)\n",
    qemu64lcpuout,
    flags=re.MULTILINE)
qemu64lcpunlist = twolistize(qemu64lcpulist)
qemu64machinelistp = subprocess.Popen(
    [qemu64llocatout, '-machine', 'help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
qemu64lmachineout, qemu64lmachineerr = qemu64machinelistp.communicate()
qemu64lmachinelist = re.findall(
    "^([\\w\\-\\.]+)\\s\\s+([\\w\\(\\)\\+\\,\\. \\-]+)\n",
    qemu64lmachineout,
    flags=re.MULTILINE)
qemu64lmachinenlist = twolistize(qemu64lmachinelist)
qemu64soundhwlistp = subprocess.Popen(
    [qemu64llocatout, '-soundhw', 'help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
qemu64lsoundhwout, qemu64lsoundhwerr = qemu64soundhwlistp.communicate()
qemu64lsoundhwlist = re.findall(
    "^([\\w]+)\\s\\s+([\\w\\(\\) ]+)\n", qemu64lsoundhwout, flags=re.MULTILINE)
qemu64lsoundhwlist.append(('all', 'Enable all sound cards'))
qemu64lsoundhwnlist = twolistize(qemu64lsoundhwlist)
qemu64larglist = arglistize(
    qemu64llocatout,
    ('-hda',
     '/dev/null'),
    ('-cdrom',
     '/home/cooldude2k/Emu/Minix3/minix_R3.3.0-588a35b.iso'),
    ('-boot',
     'order=acd,once=d,menu=on'),
    ('-cpu',
     qemu64lcpunlist['name']['reg'][9]),
    ('-machine',
     qemu64lmachinenlist['name']['reg'][17]),
    ('-soundhw',
     qemu64lsoundhwnlist['name']['reg'][8]),
    ('-sdl',
     None))
print("PATH environment variable is set to " + os.environ["PATH"])
print("Python " + sys.version)
print(__project__ + " version " + __version__)
print("QEMU emulator version " + qemu64lverfull)
print(qemu64larglist)
qemu64cmdlaunch = subprocess.Popen(
    qemu64larglist, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
qemu64cmdlaunch.wait()
print(str(qemu64cmdlaunch.returncode))
