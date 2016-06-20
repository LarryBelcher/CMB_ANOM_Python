#!/usr/bin/python

import matplotlib as mpl
mpl.use('Agg')
import os, datetime, sys, shapefile, glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.collections import LineCollection
import matplotlib.colors as colors
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.font_manager as font_manager
from PIL import Image
from matplotlib.colors import from_levels_and_colors

def divlookup(dfile, division, year, month):
	'''
	Function divlookup: pulls division data from CMB data (i.e., text file)
	'''
	cmd = 'grep '+division+'01'+year+' '+dfile
	#print cmd
	dval = os.popen(cmd)
	dval = float(dval.read().split()[month])
	return dval

def normlookup(normfile, division, month):
	'''
	Function divlookup: pulls division data from CMB data (i.e., text file)
	'''
	cmd = 'grep ^'+division+'010009 '+normfile
	#print cmd
	nval = os.popen(cmd)
	nval = float(nval.read().split()[month])
	#print division
	return nval	



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


imgsize = sys.argv[2]   #(expects 620, 1000, DIY, HD, or HDSD)


dfile = glob.glob('./Data/climdiv-pcp*')
dfile = dfile[0]

normfile = glob.glob('./Data/norm-climdiv-norm-pcp*')
normfile = normfile[0]

path = '/usr/local/share/fonts/truetype/msttcorefonts/Trebuchet_MS.ttf'
propr = font_manager.FontProperties(fname=path)
path = '/usr/local/share/fonts/truetype/msttcorefonts/Trebuchet_MS_Bold.ttf'
propb = font_manager.FontProperties(fname=path)

if(imgsize == '620'):
	figxsize = 8.62
	figysize = 5.56
	figdpi = 72
	lllon, lllat, urlon, urlat = [-119.8939, 21.6678, -62.3094, 49.1895]
	logo_image = './noaa_logo_42.png'
	logo_x = 566
	logo_y = 4
	framestat = 'False'
	base_img = './CONUS_620_BaseLayer.png'
	line_img = './CONUS_620_stateLines.png'
	bgcol = '#F5F5F5'
	cmask = "./Custom_mask.png"

if(imgsize == '1000'):
	figxsize = 13.89
	figysize = 8.89
	figdpi = 72
	lllon, lllat, urlon, urlat = [-119.8939, 21.6678, -62.3094, 49.1895]
	logo_image = './noaa_logo_42.png'
	logo_x = 946
	logo_y = 4
	framestat = 'False'
	base_img = './CONUS_1000_BaseLayer.png'
	line_img = './CONUS_1000_stateLines.png'
	bgcol = '#F5F5F5'
	cmask = "./Custom_mask.png"

if(imgsize == 'DIY'):
	figxsize = 13.655
	figysize = 8.745
	figdpi = 300
	lllon, lllat, urlon, urlat = [-119.8939, 21.6678, -62.3094, 49.1895]
	logo_image = './noaa_logo_42.png'
	logo_x = 946
	logo_y = 4
	framestat = 'False'
	base_img = './CONUS_DIY_BaseLayer.png'
	line_img = './CONUS_DIY_stateLines.png'
	bgcol = '#F5F5F5'
	cmask = "./Custom_mask.png"

if(imgsize == 'HD'):
	figxsize = 21.33
	figysize = 10.25
	figdpi = 72
	lllon, lllat, urlon, urlat = [-126.95182, 19.66787, -52.88712, 46.33016]
	logo_image = './noaa_logo_100.png'
	logo_x = 1421
	logo_y = 35
	framestat = 'True'
	base_img = './CONUS_HD_BaseLayer.png'
	line_img = './CONUS_HD_stateLines.png'
	framestat = 'False'
	bgcol = '#F5F5F5'
	cmask = "./Custom_HD_mask.png"

if(imgsize == 'HDSD'):
	figxsize = 16
	figysize = 9.75
	figdpi = 72
	lllon, lllat, urlon, urlat = [-120.8000, 19.5105, -57.9105, 48.9905]
	logo_image = './noaa_logo_100.png'
	logo_x = 1037
	logo_y = 35
	framestat = 'True'
	base_img = './CONUS_HDSD_BaseLayer.png'
	line_img = './CONUS_HDSD_stateLines.png'
	framestat = 'False'
	bgcol = '#F5F5F5'
	cmask = "./Custom_HDSD_mask.png"


fig = plt.figure(figsize=(figxsize,figysize))
# create an axes instance, leaving room for colorbar at bottom.
ax1 = fig.add_axes([0.0,0.0,1.0,1.0], frameon=framestat)#, axisbg=bgcol)
ax1.spines['left'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.spines['top'].set_visible(False)

# Create Map and Projection Coordinates
kwargs = {'epsg' : 5070,
          'resolution' : 'i',
          'llcrnrlon' : lllon,
          'llcrnrlat' : lllat,
          'urcrnrlon' : urlon,
          'urcrnrlat' : urlat,
          'lon_0' : -96.,
          'lat_0' : 23.,
          'lat_1' : 29.5,
          'lat_2' : 45.5,
		  'area_thresh' : 15000,
		  'ax' : ax1,
		  'fix_aspect' : False
}

#Set up the Basemap
m =Basemap(**kwargs)


#Add the BaseLayer image 1st pass
outline_im = Image.open(base_img)
m.imshow(outline_im, origin='upper', aspect='auto')


valmax = 400.
valmin = 0.
cmap = plt.cm.BrBG

num_levels = 255
vmin, vmax = 0, 300
midpoint = 100
levels = np.linspace(vmin, vmax, num_levels)
midp = np.mean(np.c_[levels[:-1], levels[1:]], axis=1)
vals = np.interp(midp, [vmin, midpoint, vmax], [0, 0.5, 1])
colors = plt.cm.BrBG(vals)
cmap, norm = from_levels_and_colors(levels, colors)

if(mm != '00'):
	#Now read in the Climate Division Shapes and fill the basemap 
	r = shapefile.Reader(r"./Shapefiles/GIS_OFFICIAL_CLIM_DIVISIONS")
	shapes = r.shapes()
	records = r.records()

	for record, shape in zip(records,shapes):
	    lons,lats = zip(*shape.points)
	    data = np.array(m(lons, lats)).T
	 
	    if len(shape.parts) == 1:
	        segs = [data,]
	    else:
	        segs = []
	        for i in range(1,len(shape.parts)):
	            index = shape.parts[i-1]
	            index2 = shape.parts[i]
	            segs.append(data[index:index2])
	        segs.append(data[index2:])
	 
	    lines = LineCollection(segs,antialiaseds=(1,))
	    #Now obtain the data in a given poly and assign a color to the value
	    div = str(record[5])
	    dval = divlookup(dfile,div,yyyy,int(mm))
	    if(len(div) < 4): div = '0'+div
	    nval = normlookup(normfile, div, int(mm))
	    dval = (dval/nval)*100.
	    #Now normalize the data and map it to the color ramp
	    #dval = (dval - valmin) * (255/(valmax-valmin))
	    #Map the value out to the point in the color ramp
	    pts = np.where(levels < dval)
	    if(dval != 0): dval = max(pts[0])
	    if(dval == cmap.N): dval = dval-1
	    lines.set_facecolors(cmap(int(dval)))
	    lines.set_edgecolors(cmap(int(dval)))
	    lines.set_linewidth(0.25)
	    ax1.add_collection(lines)


#Add the custom mask
omask_im = Image.open(cmask)
m.imshow(omask_im, origin='upper', alpha=1., zorder=10, aspect='auto', interpolation='nearest')

#Add the Line image
outline_im = Image.open(line_img)
m.imshow(outline_im, origin='upper', alpha=0.75, zorder=10, aspect='auto')


#Add the NOAA logo (except for DIY)
if(imgsize != 'DIY'):
	logo_im = Image.open(logo_image)
	height = logo_im.size[1]
	# We need a float array between 0-1, rather than
	# a uint8 array between 0-255 for the logo
	logo_im = np.array(logo_im).astype(np.float) / 255
	fig.figimage(logo_im, logo_x, logo_y, zorder=10)



outpng = "temporary_map.png"

if(imgsize == '620' or imgsize == '1000' or imgsize == 'DIY'):
	plt.savefig(outpng,dpi=figdpi, orientation='landscape', bbox_inches='tight', pad_inches=0.00)

if(imgsize == 'HD' or imgsize =='HDSD'):
	plt.savefig(outpng, dpi=figdpi, orientation='landscape')#, bbox_inches='tight', pad_inches=0.01)


