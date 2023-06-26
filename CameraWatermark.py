import os
import glob
import exifread
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def getPath():
    input_folder_path = '.\input'
    extensions = ['*.jpg', '*.jpeg', '*.png']
    files = []
    for extension in extensions:
        files.extend(glob.glob(os.path.join(input_folder_path, extension)))
    return files


def jointWatermark(img_path):
    f = open(img_path, 'rb')
    tags = exifread.process_file(f)

    output_folder_path = '.\output\\'
    img = Image.open(img_path)

    while img.width < 1500:
        img = img.resize((img.width*2, img.height*2))
    
    wm_height = int(img.height*0.1)
    watermark = Image.new('RGB', (img.width, wm_height), (255, 255, 255))

    logo = Image.open('asset\logo\\'+str(tags['Image Make'])+'.png')
    logo_ratio = logo.width/logo.height
    if img.width < img.height :
        logo_height = int(wm_height*0.2)
    else:
        logo_height = int(wm_height*0.35)
    logo_width = int(logo_ratio*logo_height)
    logo = logo.convert('P')
    logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
    log_x = int(img.width-wm_height*0.215*14-logo_width)
    log_y = int(wm_height*0.35)
    watermark.paste(logo, (log_x, log_y))

    draw = ImageDraw.Draw(watermark)
    
    
    Modelfont = ImageFont.truetype(font='asset\\font\方正粗黑宋简体.ttf', size=np.floor(wm_height*0.25).astype('int32')) 
    if 'Image Model' in tags:
        draw.text((int(img.width*0.02), int(wm_height*0.25)), str(tags['Image Model']), fill='black', font=Modelfont)
    
    LensModelfont = ImageFont.truetype(font='asset\\font\STFANGSO.TTF', size=np.floor(wm_height*0.175).astype('int32')) 
    if 'EXIF LensModel' in tags:
        draw.text((int(img.width*0.02), int(wm_height*0.6)), str(tags['EXIF LensModel']), fill='black', font=LensModelfont)

    draw_x = logo_width+log_x+5
    draw_width = int(img.width*0.001)
    draw.line([(draw_x, log_y-5*draw_width), (draw_x, log_y+logo_height+5*draw_width)], fill='black', width=draw_width)

    Parameterfont = ImageFont.truetype(font='asset\\font\STFANGSO.TTF', size=np.floor(wm_height*0.215).astype('int32'))
    if 'EXIF FocalLength' in tags:
        Parameter = str(tags['EXIF FocalLength']) + 'mm  f/' +str(float(tags['EXIF FNumber'].values[0])) + '  ' + str(tags['EXIF ExposureTime'])+\
            's  ISO'+str(tags['EXIF ISOSpeedRatings']) 
        draw.text((draw_x+10*draw_width, int(wm_height*0.25)), Parameter, fill='black', font=Parameterfont)
    
    Timefont = ImageFont.truetype(font='asset\\font\simhei.TTF', size=np.floor(wm_height*0.15).astype('int32')) 
    if 'EXIF DateTimeOriginal' in tags:
        draw.text((draw_x+12*draw_width, int(wm_height*0.6)), str(tags['EXIF DateTimeOriginal']), fill='black', font=Timefont)

    Markfont = ImageFont.truetype(font='asset\\font\方正粗黑宋简体.TTF', size=np.floor(wm_height*0.2).astype('int32'))
    draw.text((draw_x+12*draw_width+int(wm_height*0.15*11), int(wm_height*0.55)), u'@name', fill='blue', font=Markfont)#自定义ID

    im = np.array(img)
    im_wm = np.concatenate((im, watermark), axis = 0)
    img_out = Image.fromarray(im_wm)
    img_out.save(output_folder_path + img_path.split('\\')[-1])

if __name__ == '__main__':
    imgs_path = getPath()
    for path in imgs_path:
        jointWatermark(path)
        print(path + " was successfully processed")

