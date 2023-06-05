# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 17:04:44 2020

@author: rahul
"""
import cv2, numpy as np, argparse, time, glob, os, sys, subprocess, pandas, random, Update_Model, math
from tkinter import *
import tkinter.messagebox
from pygame import mixer
from tkinter import filedialog
import os
import sys
from mutagen.mp3 import MP3
import time
import threading
from tkinter import ttk
from emotion_recognition import main

paused=FALSE
muted=FALSE
playlist=[]
lst=[]
index=0
filename=""
refresh=FALSE

def about_us():
    tkinter.messagebox.showinfo('About BoomBox','This is a program for a music player that can suggest music based on the emotion it detects.')
    
def browse_file():
    global filename
    filename=filedialog.askopenfilename()
    add_to_playlist(filename)
    
def add_to_playlist(f):
    global index
    f=os.path.basename(f)
    playlistbox.insert(index,f)
    playlist.insert(index,filename)
    index+=1
    
def del_song():
    selected_song=playlistbox.curselection()
    selected_song=int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)
    
def show_details(cur_song):
    file_data=os.path.splitext(cur_song)
    
    if file_data[1]=='.mp3':
        audio=MP3(cur_song)
        totlength=audio.info.length
    else:
        a=mixer.Sound(cur_song)
        totlength=a.get_length
        
    mins,secs=divmod(totlength,60)
    mins=round(mins)
    secs=round(secs)
    timeformat='{:02d}:{:02d}'.format(mins,secs)
    lengthlabel['text']='Total length- '+timeformat
    
    t1=threading.Thread(target=start_count,args=(totlength,))
    t1.start()
    
def start_count(t):
    global paused
    while t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins,secs=divmod(t,60)
            mins=round(mins)
            secs=round(secs)
            timeformat='{:02d}:{:02d}'.format(mins,secs)
            timelabel['text']=timeformat
            time.sleep(1)
            t-=1
    
def  play_music():
    try:
        stop_music()
        time.sleep(1)
        selected_song=playlistbox.curselection()
        selected_song=int(selected_song[0])
        play_it=playlist[selected_song]
        mixer.music.load(play_it)
        mixer.music.play()
        statusbar['text']="Playing music : "+os.path.basename(play_it)
        show_details(play_it)
    except:
        tkinter.messagebox.showerror('File not found.','BoomBox could not find the file. Please check again.')
        
def stop_music():
    mixer.music.stop()
    statusbar['text']="stopped"
        
def pause_music():
    global paused
    if(paused==TRUE):
        mixer.music.unpause()
        paused=FALSE
        statusbar['text']="Playing music : "+os.path.basename(filename)
    else:
        paused=TRUE
        mixer.music.pause()
        statusbar['text']=os.path.basename(filename)+' paused'

def set_vol(val):
    volume=float(val)/100
    mixer.music.set_volume(volume)
    
def mute_music():
    global muted
    if(muted==TRUE):
        mixer.music.set_volume(0.5)
        volumebtn.configure(image=volumephoto)
        volcontrol.set(50)
        muted=FALSE
    else:
        mixer.music.set_volume(0)
        volumebtn.configure(image=mutephoto)
        volcontrol.set(0)
        muted=TRUE

def fersuggest():
    global filename
    global refresh
    playlistbox.delete(0,END)
    playlist.clear()
    lst=[]
    lst=main()
    for filename in lst:
        add_to_playlist(filename)
    emodetect=lst[0]
    if(emodetect[6]=='H'):
        emotion='Happy'
    elif(emodetect[6]=='N'):
        emotion='Neutral'
    elif(emodetect[6]=='S'):
        emotion='Sad'
    else:
        emotion='Angry'
    statusbar['text']=emotion+" emotion detected"
    refresh=TRUE

def on_closing():
    stop_music()
    root.destroy()
    

root=Tk()
#creating blank menubar
menubar=Menu(root)
root.config(menu=menubar)
#creating submenus
subMenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=subMenu)
subMenu.add_command(label='Open',command=browse_file)
subMenu.add_command(label='Exit',command=on_closing)

subMenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=subMenu)
subMenu.add_command(label='About Us', command=about_us)

mixer.init()
root.title("BoomBox")
root.iconbitmap(r'boombox.ico')

statusbar=ttk.Label(root,text='',relief=SUNKEN,anchor=W,)
statusbar.pack(side=BOTTOM,fill=X)

leftframe=Frame(root)
leftframe.pack(side=LEFT,padx=20)

playlistbox=Listbox(leftframe,width=50,height=30)
playlistbox.pack()

addbtn=ttk.Button(leftframe,text="+ Add",command=browse_file)
addbtn.pack(side=LEFT)

delbtn=ttk.Button(leftframe,text="- Delete",command=del_song)
delbtn.pack(side=LEFT)

rightframe=Frame(root)
rightframe.pack()

topframe=Frame(rightframe)
topframe.pack()

lengthlabel=ttk.Label(topframe,text='Total length- --:--')
lengthlabel.grid(row=0,column=0,pady=10)

timelabel=ttk.Label(topframe,text='--:--',relief=GROOVE)
timelabel.grid(row=1,column=0)

ferphoto=PhotoImage(file='fer.png')
ferbtn=ttk.Button(topframe,text='music suggestion',image=ferphoto,command=fersuggest,compound=TOP)
ferbtn.grid(row=0,rowspan=2,column=2,pady=10,padx=20)

middleframe=Frame(rightframe)
middleframe.pack()

playphoto= PhotoImage(file='play.png')
pausephoto= PhotoImage(file='pause.png')
stopphoto=PhotoImage(file='stop.png')

playbtn= ttk.Button(middleframe,image=playphoto,command=play_music)
playbtn.grid(row=0,column=1,padx=10,pady=10)

pausebtn= ttk.Button(middleframe,image=pausephoto,command=pause_music)
pausebtn.grid(row=0,column=0,padx=10,pady=10)

stopbtn= ttk.Button(middleframe,image=stopphoto,command=stop_music)
stopbtn.grid(row=0,column=2,padx=10,pady=10)

bottomframe=Frame(rightframe)
bottomframe.pack()

volumephoto=PhotoImage(file='volume.png')
mutephoto=PhotoImage(file='mute.png')

volumebtn=ttk.Button(bottomframe,image=volumephoto,command=mute_music)
volumebtn.grid(row=0,column=0,padx=20)

volcontrol=ttk.Scale(bottomframe,from_=0,to=100,orient=HORIZONTAL,command=set_vol)
volcontrol.set(50)
mixer.music.set_volume(0.5)
volcontrol.grid(row=0,column=1,pady=15)

root.protocol("WM_DELETE_WINDOW",on_closing)
    
root.mainloop()