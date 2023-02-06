
############################################################################################
# Cristina Almagro-Perez, February 2023, PSI, Switzerland
############################################################################################
# Convert histologies from .svs format (raw microscopy format) to readable format in python
############################################################################################

# Import necessary packages
import glob
import os
import slideio  #('pip install slideio' on terminal)
import matplotlib.pyplot as plt
from PIL import Image

# Please select all the resolutions the images will be saved (Original res = 20x, 0.5 um/pixel)
res10x = True  # 1 um/pixel
res5x = True   # 2 um/pixel
res1x = False   # 4 um/pixel

# Please specify the type of image: either 'HE' or 'other'
stain_type = 'other'
if stain_type == 'HE':
    # Path to H&E Images
    pthHE = '/das/work/p20/p20847/histology/A18-3_H&E_serial_sections/'
elif stain_type == 'other':
    pth_immuno = '/das/work/p20/p20847/histology/other_stainings/'
else:
    raise Warning("Stain type not valid")

###########################################################################################
# Auxiliary function to save .svs images in multiple resolutions
###########################################################################################


def save_multiple_resolutions(pth0):
    imlist = glob.glob(os.path.join(pth0, '*.svs')) # List of '.svs' files
    for count, image_path in enumerate(imlist):
        print("Downsampling image " + str(count+1) + '/' + str(len(imlist)) + " with name: " + image_path.split('/')[-1])
        slide = slideio.open_slide(image_path, 'SVS')
        scene = slide.get_scene(0)
        print(slide.num_scenes, scene.name, scene.rect, scene.resolution)
        # Read metadata
        raw_string = slide.raw_metadata
        print(raw_string.split("|"))

        width20x = scene.rect[2]
        output_name = image_path.split('/')[-1].replace(".svs", ".tif")

        if res10x:
            outpth10x = os.path.join(pth0, '10x')
            if not os.path.exists(outpth10x):
                os.makedirs(outpth10x)
            width10x = round(width20x / 2)
            image = scene.read_block(size=(width10x, 0))
            print("Image dimensions in 10x:", image.shape)
            # Save image in tif format
            output_datafile = os.path.join(outpth10x, output_name)
            im = Image.fromarray(image)
            im.save(output_datafile)

        if res5x:
            outpth5x = os.path.join(pth0, '5x')
            if not os.path.exists(outpth5x):
                os.makedirs(outpth5x)
            width5x = round(width20x / 4)
            image = scene.read_block(size=(width5x, 0))
            print("Image dimensions in 5x:", image.shape)
            # Save image in tif format
            output_datafile = os.path.join(outpth5x, output_name)
            im = Image.fromarray(image)
            im.save(output_datafile)

        if res1x:
            outpth1x = os.path.join(pth0, '1x')
            if not os.path.exists(outpth1x):
                os.makedirs(outpth1x)
            width1x = round(width20x / 8)
            image = scene.read_block(size=(width1x, 0))
            print("Image dimensions in 1x:", image.shape)
            # Save image in tif format
            output_datafile = os.path.join(outpth1x, output_name)
            im = Image.fromarray(image)
            im.save(output_datafile)

############################################################################################
# Main
############################################################################################


if stain_type == 'other':
    folder_list = os.listdir(pth_immuno)
    for immuno_stain_type in folder_list:
        pth_immuno_subtype = os.path.join(pth_immuno, immuno_stain_type)
        save_multiple_resolutions(pth_immuno_subtype)

elif stain_type == 'HE':
    save_multiple_resolutions(pthHE)
