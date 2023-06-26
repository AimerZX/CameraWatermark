import exifread
from PIL import Image
import numpy as np

def jointWatermark():
    f = open('IMG_3066.jpg', 'rb')
    tags = exifread.process_file(f)
    print('拍摄时间：', tags['EXIF DateTimeOriginal'])
    print('照相机制造商：', tags['Image Make'])
    print('照相机型号：', tags['Image Model'])
    print('镜头型号：', tags['EXIF LensModel'])
    print('拍摄参数：', tags['EXIF ExposureTime'], tags['EXIF FNumber'], tags['EXIF ISOSpeedRatings'], tags['EXIF FocalLength'])

    img = Image.open('IMG_3066.jpg')
    watermark = Image.new('RGB', (img.width, 128), (255, 255, 255))
    im = np.array(img)
    im_wm = np.concatenate((im, watermark), axis = 0)
    img_out = Image.fromarray(im_wm)
    img_out.save('test1.jpg')

if __name__ == '__main__':
    print()