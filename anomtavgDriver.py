#!/usr/bin/python

import matplotlib as mpl
mpl.use('Agg')
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os, sys, subprocess, glob



def int2str(mm):
	if(mm == '00'): ms = 'No Data'
	if(mm == '01'): ms = 'January'
	if(mm == '02'): ms = 'February'
	if(mm == '03'): ms = 'March'
	if(mm == '04'): ms = 'April'
	if(mm == '05'): ms = 'May'
	if(mm == '06'): ms = 'June'
	if(mm == '07'): ms = 'July'
	if(mm == '08'): ms = 'August'
	if(mm == '09'): ms = 'September'
	if(mm == '10'): ms = 'October'
	if(mm == '11'): ms = 'November'
	if(mm == '12'): ms = 'December'
	return ms


fdate = sys.argv[1]   #(expects format like: 201301)
yyyy = fdate[0:4]
mm = fdate[4:]
ms = int2str(mm)
labeldate = ms+' '+yyyy


imgsize = sys.argv[2]   #(expects 620, 1000, DIY, HD, HDSD, or GEO)

figdpi = 72

if(imgsize != 'GEO'):
	if not os.path.isdir('./Images'):
		cmd = 'mkdir ./Images'
		subprocess.call(cmd,shell=True)
	if not os.path.isdir('./Images/Temperature/'+imgsize):
		cmd = 'mkdir ./Images/Temperature/'+imgsize.lower()
		subprocess.call(cmd,shell=True)


p1 = subprocess.Popen("python anomtavgMap.py "+fdate+" "+imgsize, shell=True)
p1.wait()

if(imgsize != 'GEO'):
	p2 = subprocess.Popen("python anomtavgColorbar.py "+fdate+" "+imgsize, shell=True)
	p2.wait()



if(imgsize == '620' or imgsize == '1000'):
	im1 = Image.open("temporary_map.png")
	im2 = Image.open("temporary_cbar.png")
	im3 = Image.new('RGBA', size = (im1.size[0], im1.size[1]+im2.size[1]))
	im3.paste(im2, (0,im1.size[1]))
	im3.paste(im1, (0,0))
	img_path = './Images/Temperature/'+imgsize+'/'
	imgw = str(im3.size[0])
	imgh = str(im3.size[1])
	img_name = 'averagetempanom-monthly-cmb--'+imgw+'x'+imgh+'--'+yyyy+'-'+mm+'-00.png'
	pngfile = img_path+img_name
	print "Saving "+pngfile
	im3.save(pngfile)
	

if(imgsize == 'DIY'):
	im1 = "./temporary_map.png"
	imgs = Image.open(im1)
	imgw = str(imgs.size[0])
	imgh = str(imgs.size[1])
	img_path = './Images/Temperature/'+imgsize.lower()+'/'
	img_name = 'averagetempanom-monthly-cmb--'+imgw+'x'+imgh+'--'+yyyy+'-'+mm+'-00.png'
	cmd = 'mv '+im1+' '+img_name
	subprocess.call(cmd,shell=True)
	im2 = "./temporary_cbar.eps"
	cbar_name = 'averagetempanom-monthly-cmb--'+yyyy+'-'+mm+'-00_colorbar.eps'
	cmd = 'mv '+im2+' '+cbar_name
	subprocess.call(cmd,shell=True)
	cmd1 = 'zip averagetempanom-monthly-cmb--'+imgw+'x'+imgh+'--'+yyyy+'-'+mm+'-00.zip '+img_name+' '+cbar_name+' noaa_logo.eps '
	subprocess.call(cmd1,shell=True)
	cmd2 = 'mv averagetempanom-monthly-cmb--'+imgw+'x'+imgh+'--'+yyyy+'-'+mm+'-00.zip '+img_path
	subprocess.call(cmd2,shell=True)
	cmd3 = 'rm '+img_name+' '+cbar_name
	subprocess.call(cmd3,shell=True)


if(imgsize == 'GEO'):
	im1 = "./temporary_map.tif"
	tifimgs = Image.open(im1)
	tifimgw = str(tifimgs.size[0])
	tifimgh = str(tifimgs.size[1])
	tifimg_name = 'averagetempanom-monthly-cmb--'+tifimgw+'x'+tifimgh+'--'+yyyy+'-'+mm+'-00.tif'
	cmd = 'gdal_translate -of GTiff -a_srs EPSG:4326  -a_ullr -179.9853516 74.9853516 -59.9853516 14.9853516 '+im1+' '+tifimg_name
	subprocess.call(cmd,shell=True)
	zpath = './Images/Temperature/diy/*'+yyyy+'-'+mm+'-00.zip'
	zipfile = glob.glob(zpath)
	cmd = 'zip -u '+zipfile[0]+' '+tifimg_name
	subprocess.call(cmd,shell=True)
 	cmd2 = 'rm '+tifimg_name
	subprocess.call(cmd2,shell=True)

	
if(imgsize == 'HD'):
	hdim = Image.new("RGB", (1920,1080), color='#FFFFFF')
	imgw = '1920'
	imgh = '1080'
	
	im1 = Image.open("temporary_map.png")
	bbox = (0,0,1534,736)
	im1 = im1.crop(bbox)
	osize = im1.size
	new_size = (osize[0]+2,osize[1]+2)
	im1new = Image.new("RGB", new_size)
	im1new.paste(im1, ((new_size[0]-osize[0])/2, (new_size[1]-osize[1])/2))
		
	hdim.paste(im1new, (192,108))
	
	draw = ImageDraw.Draw(hdim)
	fntpath = './Fonts/Trebuchet_MS.ttf'
	fnt1 = ImageFont.truetype(fntpath, 18)
	if(mm == '00'): xpos = 1632
	if(mm == '01'): xpos = 1615
	if(mm == '02'): xpos = 1610
	if(mm == '03'): xpos = 1623
	if(mm == '04'): xpos = 1625
	if(mm == '05'): xpos = 1630
	if(mm == '06'): xpos = 1624
	if(mm == '07'): xpos = 1626
	if(mm == '08'): xpos = 1618
	if(mm == '09'): xpos = 1595
	if(mm == '10'): xpos = 1615
	if(mm == '11' or mm == '12'): xpos = 1600	
	if(mm != '00'): draw.text((xpos,815), labeldate, (0,0,0), font=fnt1)
	if(mm == '00'): draw.text((xpos,815), ms, (0,0,0), font=fnt1)	
	fnt2 = ImageFont.truetype(fntpath, 16)
	ttext = "Difference from average temperature"
	draw.text((213,797), ttext, (0,0,0), font=fnt2)
	#fnt2a = ImageFont.truetype(fntpath, 8)
	#draw.text((495,797), "o", (0,0,0), font=fnt2a)
	fnt3 = ImageFont.truetype(fntpath, 14)
	ttext = "Compared to 1981-2010 average"
	draw.text((213,815), ttext, (0,0,0), font=fnt3)
	
	#Add the colorbar
	cbar_orig = Image.open('temporary_cbar.png')
	bbox = (1,1,972,43)
	cbar_orig = cbar_orig.crop(bbox)
	old_size = cbar_orig.size
	new_size = (old_size[0]+2,old_size[1]+2)
	cbar_im = Image.new("RGB", new_size)
	cbar_im.paste(cbar_orig, ((new_size[0]-old_size[0])/2,
                      (new_size[1]-old_size[1])/2))
	hdim.paste(cbar_im, (474,866))


	fnt4 = ImageFont.truetype(fntpath, 47)
	text2 = "cooler"
	draw.text((515,905), text2, (0,0,0), font=fnt4)
	text3 = "warmer"
	draw.text((1245,905), text3, (0,0,0), font=fnt4)
	
	draw.polygon([(500,946), (485,936), (500,926)], fill="black", outline="black")
	draw.polygon([(1420,946), (1435,936), (1420,926)], fill="black", outline="black")
	
	img_path = './Images/Temperature/'+imgsize.lower()+'/'
	img_name = 'averagetempanom-monthly-cmb--'+imgw+'x'+imgh+'hd--'+yyyy+'-'+mm+'-00.png'
	pngfile = img_path+img_name
	print "Saving "+pngfile
	hdim.save(pngfile)


if(imgsize == 'HDSD'):
	hdim = Image.new("RGB", (1920,1080), color='#FFFFFF')
	imgw = '1920'
	imgh = '1080'
	
	im1 = Image.open("temporary_map.png")
	bbox = (0,0,1150,700)
	im1 = im1.crop(bbox)
	osize = im1.size
	new_size = (osize[0]+2,osize[1]+2)
	im1new = Image.new("RGB", new_size)
	im1new.paste(im1, ((new_size[0]-osize[0])/2, (new_size[1]-osize[1])/2))
		
	hdim.paste(im1new, (384,108))
	
	draw = ImageDraw.Draw(hdim)
	fntpath = './Fonts/Trebuchet_MS.ttf'
	fnt1 = ImageFont.truetype(fntpath, 18)
	if(mm == '00'): xpos = 1440
	if(mm == '01'): xpos = 1420
	if(mm == '02'): xpos = 1417
	if(mm == '03'): xpos = 1427
	if(mm == '04'): xpos = 1434
	if(mm == '05'): xpos = 1437
	if(mm == '06'): xpos = 1433
	if(mm == '07'): xpos = 1434
	if(mm == '08'): xpos = 1425
	if(mm == '09'): xpos = 1403
	if(mm == '10'): xpos = 1420
	if(mm == '11' or mm == '12'): xpos = 1410
	if(mm != '00'): draw.text((xpos,781), labeldate, (0,0,0), font=fnt1)
	if(mm == '00'): draw.text((xpos,781), ms, (0,0,0), font=fnt1)		
	fnt2 = ImageFont.truetype(fntpath, 14)
	ttext = "Difference from average temperature"
	draw.text((400,768), ttext, (0,0,0), font=fnt2)
	#fnt2a = ImageFont.truetype(fntpath, 8)
	#draw.text((646,767), "o", (0,0,0), font=fnt2a)
	fnt3 = ImageFont.truetype(fntpath, 14)
	ttext = "Compared to 1981-2010 average"
	draw.text((400,785), ttext, (0,0,0), font=fnt3)
	
	#Add the colorbar
	cbar_orig = Image.open('temporary_cbar.png')
	bbox = (1,1,972,43)
	cbar_orig = cbar_orig.crop(bbox)
	old_size = cbar_orig.size
	new_size = (old_size[0]+2,old_size[1]+2)
	cbar_im = Image.new("RGB", new_size)
	cbar_im.paste(cbar_orig, ((new_size[0]-old_size[0])/2,
                      (new_size[1]-old_size[1])/2))
	hdim.paste(cbar_im, (474,830))
		
	fnt4 = ImageFont.truetype(fntpath, 47)
	text2 = "cooler"
	draw.text((515,870), text2, (0,0,0), font=fnt4)
	text3 = "warmer"
	draw.text((1245,870), text3, (0,0,0), font=fnt4)
	
	draw.polygon([(500,911), (485,901), (500,891)], fill="black", outline="black")
	draw.polygon([(1420,911), (1435,901), (1420,891)], fill="black", outline="black")
	
	img_path = './Images/Temperature/'+imgsize.lower()+'/'
	img_name = 'averagetempanom-monthly-cmb--'+imgw+'x'+imgh+'hdsd--'+yyyy+'-'+mm+'-00.png'
	pngfile = img_path+img_name
	print "Saving "+pngfile
	hdim.save(pngfile)