import Image, ImageDraw, ImageFont
import os, sys, random
import math

def lerp(a, b, t):
  return a * t + b * (1.-t)

def inBound(point, bound):
  return point[0] in xrange(bound[0]) and point[1] in xrange(bound[1])

im = Image.new('L', (250, 80), 255)

draw = ImageDraw.Draw(im) 
fonts = [ImageFont.truetype("LiberationSerif-Italic.ttf",50 + i * 5) for i in xrange(5)]
chars = list('csdH4kz')
random.shuffle(chars)
curr_x = random.randint(20, 40)
for char in chars:
  font_number = random.randint(0, 4)
  draw.text((curr_x, 5), char, font=fonts[font_number])
  curr_x += draw.textsize(char, font=fonts[font_number])[0]-random.randint(7, 10)

# im.save('new.png')
# exit()

for i in xrange(10):
  noise_point = (random.randint(10, im.size[0]-10), random.randint(10, im.size[1]-10))
  offset = (noise_point[0] + random.randint(0, 6)-3, noise_point[1] + random.randint(10, 20))
  draw.line(noise_point + offset, fill=180, width=2)


new_im = im.copy()

data = im.load()
new_data = new_im.load()

freqs = [random.randint(700000, 1000000) / 15000000.0 for i in range(4)]
phases = [random.randint(0, 3141592) / 1000000.0 for i in range(4)]
amplitudes = [random.randint(400, 600) / 100.0 for i in range(2)]

for x in xrange(1, im.size[0]):
  for y in xrange(1, im.size[1]):
    sx = x + ( math.sin(x * freqs[0] + phases[0]) + math.sin(y * freqs[2] + phases[1]) ) * amplitudes[0];
    sy = y + ( math.sin(x * freqs[1] + phases[2]) + math.sin(y * freqs[3] + phases[3]) ) * amplitudes[1];
    point = (math.ceil(sx), math.ceil(sy))

    new_color = 255
    if inBound(point, im.size) and inBound((point[0]-1, point[1]), im.size) and inBound((point[0], point[1]-1), im.size):
      new_color = lerp(data[point[0]-1, point[1]], data[point[0], point[1]], point[0] - sx)
      new_color = lerp(data[point[0], point[1]-1], new_color, point[1] - sy)


    new_data[x, y] = new_color

new_im.save('4.png')
