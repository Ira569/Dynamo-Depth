from nuscenes.nuscenes import NuScenes
import os
import imageio
from PIL import Image

nusc = NuScenes(version='v1.0-mini', dataroot='nuscenes-mini', verbose=True)
scenes = nusc.scene
output_dir = 'scenes'

cam_names = ['CAM_FRONT', 'CAM_FRONT_LEFT', 'CAM_FRONT_RIGHT', 'CAM_BACK', 'CAM_BACK_LEFT', 'CAM_BACK_RIGHT']
# 需要的目录结构
# scenes
#    scene-0061
#       FRONT
#           rgb
#               downsample
#               origin
for scene in scenes:
    scene_token = scene['token']
    sample_token = scene['first_sample_token']
    scene_name = scene['name']

    idx = 0
    while sample_token != '':
        sample = nusc.get('sample', sample_token)
        for cam in cam_names:
            scene_dir = os.path.join(output_dir, scene_name, cam[4:], 'rgb', 'original')
            os.makedirs(scene_dir, exist_ok=True)
            sample_data = nusc.get('sample_data', sample['data'][cam])
            image_path = nusc.get_sample_data_path(sample_data['token'])

            # 在这里可以使用image_path进行后续处理，比如读取图像等操作
            image = imageio.imread(image_path)
            image_filename = '{:06d}'.format(idx) + '.jpg'
            image_save_path = os.path.join(scene_dir, image_filename)
            imageio.imwrite(image_save_path, image)
            # if cam == 'CAM_FRONT':
            #     with open('scene-img-sampletoken.txt', 'a') as f:
            #         f.write(scene_name+' '+image_filename+' '+sample_token+'\n')
            # image_filename = os.path.basename(image_path)

            scene_dir_downsample = os.path.join(output_dir, scene_name, cam[4:], 'rgb', 'downsample')
            os.makedirs(scene_dir_downsample, exist_ok=True)
            image = Image.open(image_path)
            scaled_image = image.resize((512, 288))
            image_filename = '{:06d}'.format(idx) + '.jpg'
            image_save_path = os.path.join(scene_dir_downsample, image_filename)
            scaled_image.save(image_save_path)

        idx = idx + 1
        sample_token = sample['next']