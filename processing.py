import os
from PIL import Image, ExifTags
from skimage import io, transform, color
import numpy as np

folder_path = 'Imgfiles'
output_folder = 'processed-imgs'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

new_size = (800, 600)


def correct_orientation(img):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        exif = img._getexif()
        if exif is not None:
            orientation = exif.get(orientation)
            if orientation == 3:
                img = img.rotate(180, expand=True)
            elif orientation == 6:
                img = img.rotate(270, expand=True)
            elif orientation == 8:
                img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass
    return img


for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        img_path = os.path.join(folder_path, filename)
        with Image.open(img_path) as img:
            img = correct_orientation(img)
            img = np.array(img)  
            resized_img = transform.resize(img, new_size, anti_aliasing=True)  
            gray_img = color.rgb2gray(resized_img)   
            gray_img = (gray_img * 255).astype(np.uint8)    
            output_path = os.path.join(output_folder, filename)
            io.imsave(output_path, gray_img, check_contrast=False)

print(f"Processed all images and saved to {output_folder}")
