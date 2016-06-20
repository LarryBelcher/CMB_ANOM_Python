#!/usr/bin/python


import os, sys, time, subprocess


###Check the avg temp file
cmd = 'curl ftp://ftp.ncdc.noaa.gov/pub/data/cirs/climdiv/ | grep climdiv-tmpcdv'
proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
serverfilename = out.split()[8]
fileurl = 'ftp://ftp.ncdc.noaa.gov/pub/data/cirs/climdiv/'+serverfilename
serverfiledate = int(out.split('-')[9])

cmd = 'ls ./Data/climdiv-tmpcdv*'
proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
localfilename = out
clientfiledate = int(out.split('-')[3])

if(serverfiledate != clientfiledate):
	cmd = 'rm '+localfilename
	subprocess.call(cmd, shell=True)
	cmd = 'wget '+fileurl
	subprocess.call(cmd, shell=True)
	cmd = 'mv '+serverfilename+' ./Data/'
	subprocess.call(cmd, shell=True)
	
	
###Check the avg temp file
cmd = 'curl ftp://ftp.ncdc.noaa.gov/pub/data/cirs/climdiv/ | grep climdiv-pcpndv'
proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
serverfilename = out.split()[8]
fileurl = 'ftp://ftp.ncdc.noaa.gov/pub/data/cirs/climdiv/'+serverfilename
serverfiledate = int(out.split('-')[9])

cmd = 'ls ./Data/climdiv-pcpndv*'
proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
localfilename = out
clientfiledate = int(out.split('-')[3])

if(serverfiledate != clientfiledate):
	cmd = 'rm '+localfilename
	subprocess.call(cmd, shell=True)
	cmd = 'wget '+fileurl
	subprocess.call(cmd, shell=True)
	cmd = 'mv '+serverfilename+' ./Data/'
	subprocess.call(cmd, shell=True)