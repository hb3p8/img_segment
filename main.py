import Image, ImageDraw
import os, sys, random
import numpy as np
import math
from optparse import OptionParser

def saveImage(imageData, outFileName):
    out = Image.new(im.mode, (imageData.shape[0], imageData.shape[1]))  
    out = Image.fromarray(imageData) 
    out.save(outFileName)

def medianSquare(in_data, out_data, size, offset=1):
    for x in xrange(offset, in_data.shape[0]-offset):  
        for y in xrange(offset, in_data.shape[1]-offset):
            colors = []
            for j in range(-(size[0] / 2), size[0] / 2 + 1): 
                for i in range(-(size[1] / 2), size[1] / 2 + 1): 
                    colors.append( in_data[x+i,y+j])
            colors.sort()
            out_data[x,y] = colors[len(colors)/2]

def medianPlus(in_data, out_data, size, offset=1):
    for x in xrange(offset, in_data.shape[0]-offset):  
        for y in xrange(offset, in_data.shape[1]-offset):
            colors = []
            for j in range(-(size[0] / 2), size[0] / 2 + 1): 
                for i in range(-(size[1] / 2), size[1] / 2 + 1): 
                    if (i == j) or (i==-j): 
                        colors.append( in_data[x+i,y+j])
            colors.sort()
            out_data[x,y] = colors[len(colors)/2]

def medianCross(in_data, out_data, size, offset=1):
    for x in xrange(offset, in_data.shape[0]-offset):  
        for y in xrange(offset, in_data.shape[1]-offset):
            colors = []
            for j in range(-(size[0] / 2), size[0] / 2 + 1): 
                colors.append( in_data[x,y+j])
            for i in range(-(size[1] / 2), size[1] / 2 + 1): 
                colors.append( in_data[x+i,y])
            colors.sort()
            out_data[x,y] = colors[len(colors)/2]

medians = {"cross": medianCross, "plus": medianPlus, "square": medianSquare}


parser = OptionParser()
parser.add_option("-m", "--median", dest="medianFilterType",
                  help="apply median filter of TYPE, types are [cross, plus, square]", metavar="TYPE", default="none")
parser.add_option("-s", "--step", dest="step", default=1, metavar="PIXELS",
                  help="sets up PIXELS step value for filter (default 1px)")
parser.add_option("-a", "--apperture", dest="appertureWidth", default=2, metavar="WIDTH",
                  help="sets up WIDTH value of filter apperture (default 2px)")
parser.add_option("-o", "--out", dest="outName", default=None, metavar="NAME",
                  help="sets up output file name - NAME")

(options, args) = parser.parse_args()
print options
print args
print options.medianFilterType



assert len(args) > 0, "No input file!" 

infile = args[0]

im = Image.open(infile).convert('L')
print im.format, im.size, im.mode

name, e = os.path.splitext(infile)

data = np.array(im) 
median_out_data = np.array(data) 

name += '_' + options.medianFilterType

if options.medianFilterType != "none":
  medians[options.medianFilterType](data, median_out_data, (5, 5), 2)
  data = median_out_data

# saveImage(data, name + '_.png')

step = int(options.step)
imageWidth = data.shape[1]
imageHeight = data.shape[0]
# print imageWidth, imageHeight

appWidth = int(options.appertureWidth)
appHalfWidth = appWidth / 2
values = []

name += '_' + str(step) + '_' + str(appWidth)

if options.outName != None:
  name = options.outName

for originX in xrange(appHalfWidth, imageWidth - appHalfWidth, step):  
    # print "p: " + str(originX)
    left, right = 0, 0
    for x in xrange(-appHalfWidth, 0):
        for y in xrange(0, imageHeight):
            left += data[y, originX+x]
            right += data[y, originX+appHalfWidth+x]
    values.append(right-left)

maxElem = max(map(abs, values))
scaledValues = map(lambda x: int(x/float(maxElem)*(imageHeight/2-1)), values)
xRange = range(appHalfWidth, imageWidth - appHalfWidth, step)

file = open('./graphs/' + name, 'w')
for i in range(0,len(xRange)):
    file.write( str(xRange[i]) + '\t' + str(values[i]) +'\n' ) 
file.close()

out = Image.new(im.mode, (data.shape[0], data.shape[1]))  
out = Image.fromarray(data) 
draw = ImageDraw.Draw(out) 

def drawOverlay(color, lineWidth):
  draw.line((0, scaledValues[0]+imageHeight/2) + (xRange[0], scaledValues[0]+imageHeight/2), fill=color, width=lineWidth)
  for i in range(1, len(xRange)):
      currentPoint = (xRange[i], scaledValues[i]+imageHeight/2)
      prevPoint = (xRange[i-1], scaledValues[i-1]+imageHeight/2)
      draw.line(prevPoint + currentPoint, fill=color, width=lineWidth)

  draw.line((xRange[-1], scaledValues[-1]+imageHeight/2) + (imageWidth, scaledValues[-1]+imageHeight/2), fill=color, width=lineWidth)

drawOverlay(255, 3)
drawOverlay(40, 1)

out.save('./images/' + name + '_img.png')