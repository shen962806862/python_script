# !/usr/bin/env python
# -*- coding:utf-8 -*-

from PIL import Image,ImageDraw,ImageFilter
import os

def crop_max_square(pil_img):   #选取宽高中短的边作为正方形边长
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))

def crop_center(pil_img, crop_width, crop_height):  #在图片中截取最大正方形（居中）
    img_width, img_height = pil_img.size
    return pil_img.crop((
        (img_width - crop_width) // 2,
        (img_height - crop_height) // 2,
        (img_width + crop_width) // 2,
        (img_height + crop_height) // 2))

def mask_circle_transparent(pil_img, blur_radius, offset=0):    #画圆并将多余部分置为透明
    offset = blur_radius * 2 + offset
    mask = Image.new("L", pil_img.size, 0)
    draw = ImageDraw.Draw(mask) #创建一个图层
    # 画一个椭圆（圆），起点终点坐标为正方形的左上和右下角
    draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

    rst = pil_img.copy()
    rst.putalpha(mask)  #新图层覆盖
    return rst

def GetFileFromThisRootDir(dir,ext = None):
  allfiles = []
  needExtFilter = (ext != None)
  for root,dirs,files in os.walk(dir):
    for filespath in files:
      filepath = os.path.join(root, filespath)
      extension = os.path.splitext(filepath)[1][1:]
      if needExtFilter and extension in ext:
        allfiles.append(os.path.split(filepath)[1])
      elif not needExtFilter:
        allfiles.append(os.path.split(filepath)[1])
  return allfiles

if __name__ == '__main__':
    while True:
        filepath = input("输入文件夹路径:")
        if not os.path.exists(filepath + './Output'):
            os.mkdir(filepath + './Output')
        mode = input("是否进行批处理(y/n):")
        if mode == "y":
            files = GetFileFromThisRootDir(filepath, ['png', 'jpg'])
            for name in files:
                markimg = Image.open(filepath + '/' + name)
                im_square = crop_max_square(markimg)
                im_thumb = mask_circle_transparent(im_square, 0)
                im_thumb.save(filepath + '/Output/' + name)
        else:
            name = input("输入图片名:")
            thumb_width = input("设定图片宽度:")
            thumb_width = int(thumb_width)
            thumb_height = input("设定图片高度:")
            thumb_height = int(thumb_height)
            markimg = Image.open(filepath + '/' + name)
            im_square = crop_max_square(markimg).resize((thumb_width, thumb_height), Image.LANCZOS)
            im_thumb = mask_circle_transparent(im_square, 0)
            im_thumb.save(filepath + '/Output/' + name)
        print("----------Finished----------")
