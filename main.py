# -*- coding: utf-8 -*-

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

def collectFrame(rect, data, reverse_data=False):
  # empty 4x4 matrix
  C = [[0 for j in xrange(4)] for i in xrange(4)]

  size = (rect[2] - rect[0] + 1, rect[3] - rect[1] + 1)
  scale_factor = (1.0 / size[0] * 4, 1.0 / size[1] * 4)


  for x in xrange(size[0]):
    for y in xrange(size[1]):
      data_x = y + rect[1] if reverse_data else x + rect[0]
      data_y = x + rect[0] if reverse_data else y + rect[1]
      # if data[data_x, data_y] < 255:
      C[int(x * scale_factor[0])][int(y * scale_factor[1])] += 255 - data[data_x, data_y]

  return C

def response(mask, frame):
  R = [[frame[i][j] if mask[i, j] == 0 else -frame[i][j] for j in xrange(4)] for i in xrange(4)]
  return sum(map(lambda x: sum(x), R))


def getMinMaxPoints(values, xRange):
  last_dy = 0;
  points = []
  for i in xrange(1, len(values)):
    dy = values[i] - values[i-1]
    if last_dy * dy < 0:
      points.append(xRange[i-1])
    last_dy = dy
  return points


medians = {"cross": medianCross, "plus": medianPlus, "square": medianSquare}


parser = OptionParser()
parser.add_option("-m", "--median", dest="medianFilterType",
                  help="apply median filter of TYPE, types are [cross, plus, square]", metavar="TYPE", default="none")
parser.add_option("-s", "--step", dest="step", default=1, metavar="PIXELS",
                  help="sets up PIXELS step value for filter (default 1px)")
parser.add_option("-a", "--apperture", dest="appertureWidth", default=4, metavar="WIDTH",
                  help="sets up WIDTH value of filter apperture (default 2px)")
parser.add_option("-o", "--out", dest="outName", default=None, metavar="NAME",
                  help="sets up output file name - NAME")
parser.add_option("-l", "--slice",
                  action="store_true", dest="slice", default=False,
                  help="Slice candidates from image")
parser.add_option("-g", "--nograph",
                  action="store_true", dest="nograph", default=False,
                  help="Disable graph export")
parser.add_option("-r", "--recognition",
                  action="store_true", dest="recognition", default=False,
                  help="Enable recognition")
parser.add_option("--minw", dest="minw", default=15, metavar="MIN_WIDTH",
                  help="Min width value MIN_WIDTH for recognition (default=15px)")
parser.add_option("--maxw", dest="maxw", default=50, metavar="MAX_WIDTH",
                  help="Max width value MAX_WIDTH for recognition (default=50px)")
parser.add_option("--letters", dest="letters", default=6, metavar="LETTERS",
                  help="Letters count LETTERS expexted to appear in image (default=6)")


(options, args) = parser.parse_args()


assert len(args) > 0, "No input file!" 

infile = args[0]

im = Image.open(infile).convert('L')
# print im.format, im.size, im.mode

name, e = os.path.splitext(os.path.basename(infile))

data = np.array(im) 
median_out_data = np.array(data) 

name += '_' + options.medianFilterType

if options.medianFilterType != "none":
  medians[options.medianFilterType](data, median_out_data, (5, 5), 2)
  data = median_out_data

step = int(options.step)
imageWidth = data.shape[1]
imageHeight = data.shape[0]

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

if not options.nograph:
  file = open('./graphs/' + name, 'w')
  for i in range(0,len(xRange)):
      file.write( str(xRange[i]) + '\t' + str(values[i]) +'\n' ) 
  file.close()

if options.recognition:
  # Prepare patterns
  filter_dir = './patterns/masks/'
  patterns_dir = './patterns/' + os.path.basename(infile) + '/'
  assert os.path.exists(patterns_dir)

  masks = []

  for i in xrange(16):
    img = Image.open(filter_dir + 'filter' + str(i) + '.bmp').convert('L')
    masks.append(img.load())

  patterns_files = [ f for f in os.listdir(patterns_dir) if os.path.isfile(os.path.join(patterns_dir,f)) ]

  ref_responses = []

  for f in patterns_files:
    pattern_img = Image.open(patterns_dir + f).convert('L')
    pattern_data = pattern_img.load()
    
    C = collectFrame([0,0] + map(lambda x: x-1, pattern_img.size), pattern_data)

    ref_responses.append([])
    for mask in masks:
      ref_responses[-1].append(response(mask, C))

  # print ref_responses

  points = getMinMaxPoints(values, xRange)


  candidate_rects = []

  letters = patterns_files

  # pattern_img = Image.open(patterns_dir + "A.png").convert('L')
  # pattern_data = pattern_img.load()

  # idata = im.load()

  # asd = map(lambda x: x-1, pattern_img.size)
  # print asd
  # C_mask = collectFrame([0,0] + asd, pattern_data)
  # C = collectFrame((49, 0, 76, 79), idata)

  # print response(masks[0], C) - response(masks[0], C_mask)
  # s = 0
  # for x in xrange(28):
  #   for y in xrange(80):
  #     s += pattern_data[x, y] - idata[49+x, y]

  # print s     


  # C = collectFrame((77, 0, 101, 79), idata)
  # C = collectFrame((49, 0, 77, 79), data, reverse_data=True)

  # deltas = []
  # for l in xrange(len(ref_responses)):
  #   letter_responses = ref_responses[l]
  #   currentDelta = 0
  #   for i in xrange(len(masks)):
  #     currentDelta += math.fabs(response(masks[i], C) - letter_responses[i])
  #   deltas.append(currentDelta)

  # print letters[deltas.index(min(deltas))]



  for x1 in points:
    for x2 in points:
      delta = x2 - x1
      if delta > int(options.minw) and delta <= int(options.maxw):
        candidate_rects.append( (x1, 0) + (x2, imageHeight-1) )

  deltas = [] # набор разниц с образцами для каждого ректа   
  for rect in candidate_rects:
    # print rect
    C = collectFrame(rect, data, reverse_data=True)

    deltas.append([])
    for l in xrange(len(ref_responses)):
      letter_responses = ref_responses[l]
      currentDelta = 0
      for i in xrange(len(masks)):
        currentDelta += math.fabs(response(masks[i], C) - letter_responses[i])
      deltas[-1].append(currentDelta)


  deltas_symbols = zip(map(lambda x: (letters[x.index(min(x))], min(x)), deltas), candidate_rects)

  # for letter in letters:
  #   print sorted(filter(lambda x: x[0][0] == letter, deltas_symbols), key = lambda x: x[0][1])[:1]

  lettersCount = int(options.letters)

  deltas_symbols = sorted(deltas_symbols, key=lambda x: x[0][1])[:lettersCount]
  deltas_symbols = map(lambda item: item[0][0], sorted(deltas_symbols, key=lambda x: (x[1][0] + x[1][2]) / 2.0))
  print deltas_symbols

  exit()

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

if options.slice:
  points = getMinMaxPoints(values, xRange)

  for x in points:
    draw.line((x, 0) + (x, imageHeight-1), fill=0, width=1)

  for x1 in points:
    for x2 in points:
      delta = x2 - x1
      if delta > int(options.minw) and delta <= int(options.maxw):
        cropped = im.crop((x1, 0) + (x2, imageHeight))
        cropped.save('./images/temp/' + name + '_' + str(x1) + '_' + str(x2) + '.png')


out.save('./images/' + name + '_img.png')