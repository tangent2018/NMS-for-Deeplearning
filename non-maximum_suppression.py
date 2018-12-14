# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 10:50:44 2018

@author: dingchen

non-maximum suppression
https://blog.csdn.net/lanchunhui/article/details/71216463
"""

import numpy as np

def IOU(bbox1, bbox2):
    if min(bbox1[0], bbox1[1]) > max(bbox2[0], bbox2[1]): return 0
    if min(bbox2[0], bbox2[1]) > max(bbox1[0], bbox1[1]): return 0
    if min(bbox1[2], bbox1[3]) > max(bbox2[2], bbox2[3]): return 0
    if min(bbox2[2], bbox2[3]) > max(bbox1[2], bbox1[3]): return 0
    bbox1_area = np.abs((bbox1[1]-bbox1[0])*(bbox1[3]-bbox1[2]))
    bbox2_area = np.abs((bbox2[1]-bbox2[0])*(bbox2[3]-bbox2[2]))
    cross_x = min(np.abs(bbox1[1]-bbox1[0]), np.abs(bbox1[1]-bbox2[0]), np.abs(bbox2[1]-bbox2[0]), np.abs(bbox2[1]-bbox1[0]))
    cross_y = min(np.abs(bbox1[3]-bbox1[2]), np.abs(bbox1[3]-bbox2[2]), np.abs(bbox2[3]-bbox2[2]), np.abs(bbox2[3]-bbox1[2]))
    bbox_cross = cross_x * cross_y
    bbox_union = bbox1_area + bbox2_area - bbox_cross
    
    return bbox_cross/bbox_union
#%%
def NMS(bbox_group, iou_threshold):
    '''
    input: Nx4的数组，4是各个顶点的位置，依次是x1, x2, y1, y2
    output: NMS后的选定框
    '''
    bbox_result=[]
    
    while bbox_group.shape[0] != 0:
        bbox_area = np.abs((bbox_group[:,1]-bbox_group[:,0])*(bbox_group[:,3]-bbox_group[:,2]))
        bbox_max = bbox_group[np.argmax(bbox_area), :]
        print ('max',bbox_max)
        bbox_group = np.delete(bbox_group, np.argmax(bbox_area), axis=0)
        bbox_result.append(bbox_max)
        print (bbox_group.shape)
        
        bbox_group_tmp = bbox_group
        for i in range(bbox_group.shape[0]):
            print (i,'/', bbox_group.shape[0])
            if IOU(bbox_max, bbox_group[i,:])>iou_threshold:
                print (i)
                bbox_group_tmp = np.delete(bbox_group, i, axis=0)        
        bbox_group = bbox_group_tmp
    
    return np.array(bbox_result)
    
