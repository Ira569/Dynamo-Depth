# todo 我现在已经获得了所有关键帧的深度图，但是是分不同相机来做的，
#  所以每个相机里会有10个场景，每个场景会有38个左右有深度的关键帧(虽然除了第一帧和最后一帧以外，非关键帧的深度图我也能获得）
#  我需要把6个不同相机的深度图统一到一起，虽然在不同相机中关键帧的名称可能不一样，比如有的相机关键帧在第六张图，有的相机关键帧在第五张图
#  目录
#  scenes/scene-0061
#                    FRONT
#                    FRONT_LEFT
#                    FRONT_RIGHT
#                    BACK
#                    BACK_LEFT
#                    BACK_RIGHT
#                        rgb
#                           downsample
#                               0000xx.jpg/dep_0000xx.pt
import torch

import os
import shutil
import os.path as osp
data_dir = 'data_dir/nuscenes/'
# 源目录和目标目录
source_dir = data_dir+'scenes'
target_dir = data_dir+'depth_map'

# 遍历相机目录
for camera in ['FRONT', 'FRONT_LEFT', 'FRONT_RIGHT', 'BACK', 'BACK_LEFT', 'BACK_RIGHT']:
    camera_dir = osp.join(source_dir, 'scene-0061', camera)

    # 遍历场景目录
    scene_dir = osp.join(camera_dir, 'rgb', 'downsample')

    # 获取场景中深度图的文件列表
    depth_files = sorted([file for file in os.listdir(scene_dir) if file.startswith('dep_')])

    idx_lists = []
    sample_token_map = {}
    with open(os.path.join(scene_dir,'keyframe_idx.txt'), 'r') as file:
        for line in file:  #  scene-0061  filename  sample_token   eg: scene-0061 0 ca9a282c9e77460f8360f564131a8af5
            words = line.strip().split()
            idx_lists.append(int(words[1]))
            sample_token_map[words[1]]= words[2]  #idx 2 token

    # 遍历深度图文件列表，并按关键帧顺序进行整理和保存
    for i, depth_file in enumerate(depth_files):
        #当前相机的cam
        cam_keyframe_idx = int(depth_file[4:-3])
        # 干脆以这个token为名保存深度图好了
        # todo 目录  scenes
        #           depth_map/scenes-0061/token/
        #                                       FRONT.pt
        #                                       BACK.pt
        #                                       ...
        cam_keyframe_token = sample_token_map[str(cam_keyframe_idx)]
        source_path = os.path.join(scene_dir, depth_file)
        dep_save_dir =osp.join(target_dir,'scene-0061','{:04}'.format(i+1)+'_'+cam_keyframe_token)
        os.makedirs(dep_save_dir,exist_ok=True)

        depthmap = torch.load(source_path)
        torch.save(depthmap,osp.join(dep_save_dir,camera+'.pt'),)
