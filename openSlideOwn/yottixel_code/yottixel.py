import os
from os import makedirs
from os.path import join, splitext, basename, isfile
from multiprocessing import Pool
from functools import partial
import argparse
import ast

import h5py
import openslide
import numpy as np
import pandas as pd
from cv2 import filter2D
from tqdm import tqdm
from sklearn.cluster import KMeans

from yottixel_code.processing import prepare_slide, extract_features
from yottixel_code.search import main_search

def run(query_slide_path_input):
    query_slide_path = query_slide_path_input
    metadata_path = "/home/data/yottixel/DATABASE/sampled_metadata.csv"
    database_dir = "/home/data/nejm_ai/DATABASE/"
    database_features_path = "/home/data/yottixel/DATABASE/features.pkl"
    query_extension = "svs"
    k = 5
    subtype_search = False
    query_site = None
    save_dir = "./outputs"
    tissue_threshold = 0.7
    kmeans_clusters = 9
    percentage_selected = 15.0
    use_gpu = True
    network_weights_address = './checkpoints/KimiaNetKerasWeights.h5'
    network_input_patch_width = 1000
    batch_size = 1024
    img_format = 'png'

    if use_gpu:
        os.environ['NVIDIA_VISIBLE_DEVICES'] = '0'
        os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    else:
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

    prepare_slide(query_slide_path, save_dir, tissue_threshold, kmeans_clusters, percentage_selected)
    extract_features(query_slide_path, save_dir, network_weights_address, network_input_patch_width, batch_size, img_format)
    res = main_search(query_slide_path, save_dir, database_dir, database_features_path, metadata_path, query_extension, k, subtype_search, query_site)
    return res

# if __name__ == "__main__":
#     args = parser.parse_args()
#
#     query_slide_path = args.query_slide_path
#     metadata_path = args.metadata_path
#     database_dir = args.database_dir
#     database_features_path = args.database_features_path
#     query_extension = args.query_extension
#     k = args.k
#     subtype_search = args.subtype_search
#     query_site = args.query_site
#     save_dir = args.save_dir
#     tissue_threshold = args.tissue_threshold
#     kmeans_clusters = args.kmeans_clusters
#     percentage_selected = args.percentage_selected
#     use_gpu = args.use_gpu
#     network_weights_address = args.network_weights_address
#     network_input_patch_width = args.network_input_patch_width
#     batch_size = args.batch_size
#     img_format = args.img_format
#
#     if use_gpu:
#         os.environ['NVIDIA_VISIBLE_DEVICES'] = '0'
#         os.environ['CUDA_VISIBLE_DEVICES'] = '0'
#     else:
#         os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
#         os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
#
#     prepare_slide(query_slide_path, save_dir, tissue_threshold, kmeans_clusters, percentage_selected)
#     extract_features(query_slide_path, save_dir, network_weights_address, network_input_patch_width, batch_size, img_format)
#     print(main_search(query_slide_path, save_dir, database_dir, database_features_path, metadata_path, query_extension, k, subtype_search, query_site))
        