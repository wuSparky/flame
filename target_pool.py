# Copyright (c) 2014, The Flame Authors.
# All rights reserved.
# Author: Chao Xiong <fancysimon@gmail.com>

import os
import copy
from util import *
from dependence_analyser import *

_target_pool = {}
_build_library_pool = {}

def WriteRuleForAllTargets():
    global _target_pool
    GenerateRecursiveForSort()
    sorted_target_node_list = GetSortedTargetNodes(_target_pool)
    ComplementSubDeps(sorted_target_node_list)
    for node in sorted_target_node_list:
        target = _target_pool[node.key]
        target.WriteRule()

def GetAllTargets():
    global _target_pool
    sorted_target_node_list = GetSortedTargetNodes(_target_pool)
    targets = []
    for node in sorted_target_node_list:
        target = _target_pool[node.key]
        targets.append(target)
    return targets

def ComplementSubDeps(sorted_target_node_list):
    global _target_pool
    for node in sorted_target_node_list:
        target = _target_pool[node.key]
        recursive_library_list_str = ''
        for key in target.recursive_library_list:
            sub_target = _target_pool[key]
            # Dependant sub library must be put after this library,
            # or there will be link error(undefined reference to).
            target.dep_library_list += sub_target.dep_library_list
            target.system_library_list += sub_target.system_library_list
            target.dep_paths += sub_target.dep_paths
            target.dep_header_list += sub_target.dep_header_list
            target.sub_objs += sub_target.sub_objs + sub_target.objs
            if sub_target.prebuilt == 1:
                target.prebuilt_library_list.append(sub_target.name)
            recursive_library_list_str += sub_target.name + ','
        target.dep_library_list = RemoveDuplicate(target.dep_library_list)
        target.system_library_list = RemoveDuplicate(target.system_library_list)
        target.dep_paths = RemoveDuplicate(target.dep_paths)
        target.dep_header_list = RemoveDuplicate(target.dep_header_list)
        target.sub_objs = RemoveDuplicate(target.sub_objs)
        target.prebuilt_library_list = RemoveDuplicate(target.prebuilt_library_list)

# Dynamic library only dependent prebuild and system library.
def GenerateRecursiveForSort():
    global _target_pool
    for target in _target_pool.values():
        if target.export_dynamic == 0:
            target.recursive_library_list_for_sort = \
                    copy.copy(target.recursive_library_list)
            continue
        new_recursive_library_list = []
        for key in target.recursive_library_list:
            if key not in _target_pool:
                continue
            sub_target = _target_pool[key]
            if sub_target.prebuilt == 1:
                new_recursive_library_list.append(key)
        target.recursive_library_list_for_sort = new_recursive_library_list

def GetTargetPool():
    global _target_pool
    return _target_pool

def GetBuildLibraryPool():
    global _build_library_pool
    return _build_library_pool

