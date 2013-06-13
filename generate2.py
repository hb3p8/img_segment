import Image, ImageDraw, ImageFont
import os, sys, random
import math

def lerp(a, b, t):
  return a * t + b * (1.-t)

def inBound(point, bound):
  return point[0] in xrange(bound[0]) and point[1] in xrange(bound[1])

im = Image.new('L', (210, 80), 255)

draw = ImageDraw.Draw(im) 
fonts = [ImageFont.truetype("Kinnari-Italic.ttf", 45 + i * 3) for i in xrange(5)]
chars = list('svRtUh84')
random.shuffle(chars)
curr_x = 30
for char in chars:
  font_number = random.randint(0, 4)
  draw.text((curr_x, -10), char, font=fonts[font_number])
  curr_x += draw.textsize(char, font=fonts[font_number])[0]-random.randint(7, 9)

for i in xrange(random.randint(7, 11)):
  noise_point = (random.randint(10, im.size[0]-10), random.randint(10, im.size[1]-10))
  offset = (noise_point[0] + random.randint(0, 6)-3, noise_point[1] + random.randint(10, 20))
  draw.line(noise_point + offset, fill=180, width=2)

for i in xrange(random.randint(3, 5)):
  first_point = (random.randint(10, 50), random.randint(10, 70))
  second_point = (random.randint(im.size[0] - 50, im.size[0] - 10), random.randint(10, 70))
  draw.line(first_point + second_point, fill=0, width=1)

im.save('5.png')
