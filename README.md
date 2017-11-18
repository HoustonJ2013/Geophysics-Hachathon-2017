# Geophysics-Hachathon-2017
DCGAN for seismic image generation

This is a weekend project for 2017 Geophysics Hackathon. The idea is to learn the intrinsic patterns of a seismic image using Deep Convolutional Generative Adversarial Networks (DCGAN). 

The DCGAN structure and code were adapted from [this link](https://github.com/carpedm20/DCGAN-tensorflow)

The seismic images are from [SEG WIKI](https://wiki.seg.org/wiki/Open_data#3D_land_seismic_data). We selected the 3D Land seismic image (post-stack migrated image) from Teapot dome 3D Survey. 

We showed that with appropriate pre-processing steps and format conversions, DCGAN is able to "learned" the patterns from 120,000 2D seismic images and generate similar images from the learned patterns. 





Further thoughts：
The learn parameters in DCGAN provides a good representation of the patterns in seismic images, and can be embeded into other seismic image recognition networks to boost the performance. 

For better generalization, more seismic images from different surveys and geologies should be used to train DCGAN. 
