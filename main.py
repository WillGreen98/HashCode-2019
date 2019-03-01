#!/usr/local/bin/env python3

import os
import sys
import math
import random as rand
from util import *
from image import *

TAGS = []
REPEATED = []

vertical = 'v'
horizontal = 'h'

global slideshow
slideshow = []

class Slide():
    numberOfImages = 0

    def __init__(self,img1, img2=None):
        self.img1 = img1
        if img2 == None:
            self.numberOfImages = 1
        else:
            self.img2 = img2
            self.numberOfImages = 2
            self.sameTags = set()

    def allTags(self):
        if self.numberOfImages == 2:
            return self.img1.tags + self.img2.tags
        else:
            return self.img1.tags

def check_for_unique(tags1,tags2):
    unique_tags = set(tags1) - set(tags2)
    return unique_tags

def check_for_same(tags1,tags2):
    all_tags = list(set(tags1)) + list(set(tags2))
    sameTags = set(all_tags)
    return len(all_tags) - len(sameTags)

def scoreTransition(slide1,slide2):
    tags1 = slide1.allTags()
    tags2 = slide2.allTags()

    sameScore = check_for_same(tags1,tags2)
    unique1 = len(check_for_unique(tags1,tags2))
    unique2 = len(check_for_unique(tags2,tags1))

   #print(f"slide1: {tags1}")
   #print(f"slide2: {tags2}")
   #print(f"same: {sameScore}")
   #print(f"unique slide1: {unique1}")
   #print(f"unique slide2: {unique2}")

    return min(unique1, sameScore, unique2)

def main():
    print("Successful Run")
    arr_imgs = open_single_file(files_list[0])

    img_to_test_1 = arr_imgs[0]
    img_to_test_2 = arr_imgs[1]
    slide1 = Slide(img_to_test_1, img_to_test_2)

    img_to_test_1 = arr_imgs[2]
    img_to_test_2 = arr_imgs[3]
    slide2 = Slide(img_to_test_1, img_to_test_2)

    slideshow.append(slide1)
    slideshow.append(slide2)

    #print(scoreTransition(slide1,slide2))


arr_imgs = []
def generator(file_name):
    arr_imgs = open_single_file(file_name)
    slideshow = []
    ##algo
    arr_imgs = sorted_by_value(arr_imgs)

    while len(arr_imgs) > 0:
        img1 = arr_imgs.pop()
        if img1.orientation == "V":
            if len(arr_imgs) > 0:
                if arr_imgs[-1].orientation == "V":
                    img2 = arr_imgs.pop()
                    slide = Slide(img1, img2)
                else:
                    continue
            else:
                continue
        elif img1.orientation == "H":
            slide = Slide(img1)
        else:
            print("ERROR WHILE BUILDING DATA")

        slideshow.append(slide)

    for i in range(len(slideshow) -2):
        slide1 = slideshow[i-1]
        slide2 = slideshow[i]
        score = scoreTransition(slide1,slide2)
        #print(f"score {score}")

    return slideshow


totalNumImages = 0
def generatorV2(file_name):
    global slideshow
    slideshow = []
    imgs = open_single_file(file_name)
    global totalNumImages
    totalNumImages = len(imgs)

    ##algo
    imgs_sorted_by_tags = sorted_by_value(imgs)

    score = 0

    img1 = imgs_sorted_by_tags.pop()
    if img1.orientation == "H":
        slide1 = Slide(img1)
    else:
        i = len(imgs_sorted_by_tags) - 1
        while imgs_sorted_by_tags[i].orientation == "H":
            i -= 1
        slide1 = Slide(img1,imgs_sorted_by_tags.pop(i))

    slideshow.append(slide1)
    imgs_left = imgs_sorted_by_tags

    findBestSlide2(slide1,imgs_left)
    return slideshow


counter = 0
def findBestSlide2(slide1,imgs):

    global counter
    counter += 1
    global totalNumImages
    print(f"{counter}/{totalNumImages}")
    global slideshow
    slide2 = None
    best_score = 0
    best_slide = None
    targetScore = int(len(slide1.allTags())/2)
    #try to find best slide 2
    for img1 in imgs:
        if img1.orientation == "H":
            slide2 = Slide(img1)
            current_score = scoreTransition(slide1,slide2)
            if current_score > best_score:
                best_score = current_score
                best_slide =  slide2

            #print(f"{current_score}:{targetScore}")
            if current_score == targetScore:
                best_score = current_score
                best_slide =  slide2

                if slide2:
                    slideshow.append(slide2)
                    print(scoreTransition(slide1,slide2))
                    for img in imgs:
                        if img == slide2.img1:
                            imgs.remove(img)
                        if slide2.numberOfImages == 2:
                            if img == slide2.img2:
                                imgs.remove(img)


                    if len(imgs) == 0:
                        return slide2
                    findBestSlide2(slide2, imgs)
                return None


        elif img1.orientation == "V":
            #find best image 2 to then find best slide
            for img2 in imgs:
                if img2.id == img1.id:
                    pass
                elif img2.orientation == "V":
                    slide2 = Slide(img1,img2)
                    current_score = scoreTransition(slide1,slide2)
                    if current_score > best_score:
                        best_score = current_score
                        best_slide =  slide2

                    if current_score == targetScore:
                        best_score = current_score
                        best_slide =  slide2

                        if slide2:
                            print(scoreTransition(slide1,slide2))
                            slideshow.append(slide2)
                            for img in imgs:
                                if img == slide2.img1:
                                    imgs.remove(img)
                                if slide2.numberOfImages == 2:
                                    if img == slide2.img2:
                                        imgs.remove(img)


                            if len(imgs) == 0:
                                return slide2
                            findBestSlide2(slide2, imgs)
                        return None




    if slide2:
        slideshow.append(slide2)
        print(scoreTransition(slide1,slide2))
        for img in imgs:
            if img == slide2.img1:
                imgs.remove(img)
            if slide2.numberOfImages == 2:
                if img == slide2.img2:
                    imgs.remove(img)


        if len(imgs) == 0:
            return slide2
        print("Not optimal")
        findBestSlide2(slide2, imgs)
    return None




def generateOutput(slideShow):
    out = ""
    amount = f"{len(slideShow)}\n"
    out += amount
    for slide in slideShow:
        if slide.numberOfImages == 1:
            slideContent = f"{slide.img1.id}\n"
        else:
            slideContent = f"{slide.img1.id} {slide.img2.id}\n"
        out += slideContent
    return out[:-1]


def sorted_by_value(array):
    return sorted(array,key=sortingFunction)

def sortingFunction(a):
    return len(a.tags)

def submit():
    for file_name in files_list:
        slideShow = generator(file_name)
        out = generateOutput(slideShow)
        file_name = file_name + ".out"
        write_file(file_name,out)

def test():
    file_name = files_list[0]
    slideShow = generatorV2(file_name)
    out = generateOutput(slideShow)
    write_file(file_name,out)
    print(out)
import sys

if __name__ == '__main__':
    test()
