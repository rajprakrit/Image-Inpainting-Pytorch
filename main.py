import os
import argparse
# os.system("python test.py --baseroot ./test_data/ --baseroot_mask ./test_data_mask/ --results_path ./results --gan_type WGAN --gpu_ids -1 --epoch 40 --batch_size 1 --num_workers 0 --pad_type zero --activation elu --norm none")

import torch
import time
from torch.utils.data import DataLoader
from torchvision.utils import save_image

import network
import test_dataset
import utils

if __name__ == "__main__":

    # ----------------------------------------
    #        Initialize the parameters
    # ----------------------------------------
    parser = argparse.ArgumentParser()
    # General parameters
    parser.add_argument('--results_path', type=str, default='./results',
                        help='testing samples path that is a folder')
    parser.add_argument('--gan_type', type=str, default='WGAN',
                        help='the type of GAN for training')
    parser.add_argument('--gpu_ids', type=str, default="0",
                        help='gpu ids: e.g. 0  0,1,2, 0,2. use -1 for CPU')
    parser.add_argument('--cudnn_benchmark', type=bool,
                        default=True, help='True for unchanged input data type')
    # Training parameters
    parser.add_argument('--epoch', type=int, default=40,
                        help='number of epochs of training')
    parser.add_argument('--batch_size', type=int,
                        default=1, help='size of the batches')
    parser.add_argument('--num_workers', type=int, default=0,
                        help='number of cpu threads to use during batch generation')
    # Network parameters
    parser.add_argument('--in_channels', type=int, default=4,
                        help='input RGB image + 1 channel mask')
    parser.add_argument('--out_channels', type=int,
                        default=3, help='output RGB image')
    parser.add_argument('--latent_channels', type=int,
                        default=48, help='latent channels')
    parser.add_argument('--pad_type', type=str,
                        default='zero', help='the padding type')
    parser.add_argument('--activation', type=str,
                        default='elu', help='the activation type')
    parser.add_argument('--norm', type=str, default='none',
                        help='normalization type')
    parser.add_argument('--init_type', type=str,
                        default='xavier', help='the initialization type')
    parser.add_argument('--init_gain', type=float,
                        default=0.02, help='the initialization gain')
    # Dataset parameters
    parser.add_argument('--baseroot', type=str, default='test_data/')
    parser.add_argument('--baseroot_mask', type=str, default='test_data_mask/')
    opt = parser.parse_args()

    generator = utils.create_generator(opt)
    print('-------------------------Loading Pretrained Model-------------------------')
    model_path = os.path.join("saved_model", "deepfillv2_WGAN.pth")
    generator.load_state_dict(torch.load(model_path, map_location='cpu'))
    generator.eval()
    print('-------------------------Pretrained Model Loaded-------------------------')

    trainset = test_dataset.InpaintDataset(opt)
    print('The overall number of images equals to %d' % len(trainset))

    # # Define the dataloader
    dataloader = DataLoader(trainset, batch_size=opt.batch_size,
                            shuffle=False, num_workers=opt.num_workers, pin_memory=True)

    start = time.time()

    for batch_idx, (img, mask) in enumerate(dataloader):
        # img = img.cuda()
        # mask = mask.cuda()

        # Generator
        first_out, second_out = generator(img, mask)

        # forward propagation
        first_out_wholeimg = img * (1 - mask) + \
            first_out * mask        # in range [0, 1]
        second_out_wholeimg = img * (1 - mask) + \
            second_out * mask      # in range [0, 1]

        masked_img = img * (1 - mask) + mask
        mask = torch.cat((mask, mask, mask), 1)
        img_list = [second_out_wholeimg]
        name_list = ['second_out']
        utils.save_sample_png(sample_folder=opt.results_path, sample_name='%d' % (
            batch_idx + 1), img_list=img_list, name_list=name_list, pixel_max_cnt=255)
        print('----------------------batch_idx%d' %
              (batch_idx + 1) + ' has been finished----------------------')

    end = time.time()

    print(end - start)
