from PIL import Image
import os


def ImgMerge(imgLoc, imgMode):
  images = [Image.open(x) for x in imgLoc]
  widths, heights = zip(*(i.size for i in images))

  max_width = max(widths)
  total_height = sum(heights)

  new_im = Image.new(imgMode, (max_width, total_height))

  x_offset = 0
  for im in images:
    new_im.paste(im, (0, x_offset))
    x_offset += im.size[1]

  return new_im


for dirpath, dirnames, files in os.walk(r'Tachiyomi'):
    print(dirpath)
    
    imgList = {}
    prev = None
    index = 0
    maxheight = 0
    
    for file_name in files:
      try:
        imgloc = dirpath + "\\" + file_name
        with Image.open(imgloc) as im:
          print(imgloc, im.format, f"{im.size}x{im.mode}")
          if im.height > 8000 or maxheight > 25000:
            prev = None
            maxheight = 0
          if (f"{im.format}{im.width}{im.mode}" != prev):
            index = index + 1
            imgList[index] = []
            prev = f"{im.format}{im.width}{im.mode}"
          imgList[index].append((imgloc, im))
          maxheight = maxheight + im.height

      except OSError:
        pass

    for k, v in imgList.items():
      if len(v) > 1:
        imgloc, im = list(zip(*v))
        im = ImgMerge(imgloc, im[0].mode)
        for oldImg in imgloc:
          os.remove(oldImg)
        try:
          im.save(imgloc[0])
        except:
          imLoc = imgloc[0]
          if imLoc[imLoc.rfind("."):] != ".bin":
            os.remove(imLoc)
          
          imLoc = imLoc[:imLoc.rfind(".")]+".jpg"
          im.convert('RGB').save(imLoc,"JPEG")
