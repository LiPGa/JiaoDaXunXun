# -*- coding: utf-8 -*-
import cv2  
import numpy as np  
import math
import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

def get_scents(scents):
    # [[前调们],[中调],[后调]]
    scents_list=[]
    if scents[:3]=='气味：':
        print 'ys'
        scents=scents[3:]
        print scents
        scents_list=scents.split(',')
    else:
        if scents[:3]=='前调：':
            mid_scent_index=scents.find('中调：')
            last_scent_index=scents.find('后调：')
            
            former_scents=scents[3:mid_scent_index]
            former_scents_list=former_scents.split(',')
            scents_list.append(former_scents_list)

            mid_scents= scents[mid_scent_index+3:last_scent_index]
            mid_scents_list=mid_scents.split(',')
            scents_list.append(mid_scents_list)
            
            last_scents= scents[last_scent_index+3:]
            last_scents_list=last_scents.split(',')
            scents_list.append(last_scents_list)
    return scents_list

filename1='nosetime.txt'
filename2='perfumer.txt'
f1=open(filename1)
f2=open(filename2)
f=open('nosetime-perfumer.txt','w')
lines2=f2.readlines()
lines1=f1.readlines()
print len(lines1)
print len(lines2)
perfumes1=[]
perfumes2=[]
for line in lines1:
  line=line.strip('\n')
  line=line.decode('utf-8','ignore')
  contents=line.split('\t')
  perfume=contents[1]
  if not (perfume in perfumes1):
    perfumes1.append(perfume)

for line in lines2:
  line=line.strip('\n')
  line=line.decode('utf-8','ignore')
  contents=line.split('\t')
  perfume=contents[1]
  if not (perfume in perfumes2):
    perfumes2.append(perfume)
  # if x.find(perfume):
    # cnt+=1
cnt=0
for perfume in perfumes1:
  if not (perfume in perfumes2):
    f.write(perfume+'\n')

f.close()
print  cnt
f1.close()
f2.close()
# print cnt

# print line
# # print contents
# name=contents[-1]
# url=contents[0]
# scents=contents[2]
# comments=contents[-2][:-2]
# rate=contents[-3][:-1]
# scents_list=get_scents(scents)
# print ','.join(scents_list)

    # tune=contents[-1]
    # url=contents[0]
    # name=contents[1]
    # brand=name.split(' ')[0]
    # scents=contents[2].strip()
    # scents_list=get_scents(scents)
    # comments=contents[-2][:-2]
    # rate=contents[-3][:-1]
    # if len(scents_list)==3:
    #     for i in scents_list[0]:
    #         print i
    # else:
    #     for i in scents_list:
    #         print i

# print url
# print brand
# print scents
# print name,comments,rate
# # print scents_list


# for i in get_scents(scents):
#     print i

