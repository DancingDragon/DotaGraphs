import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

# Import the data file
data = {}
import json
with open('data.json') as json_file:
    data = json.load(json_file)

# Hero names and damage source names
heroes = {}

# Go through data and collect damage sources
for minute in data:
    for h in data[minute].keys():
        if not h in heroes:
            heroes[h] = []
        for ds in data[minute][h]:
            if not ds in heroes[h]:
                heroes[h].append(ds)
            

# Time
x = data.keys()
title = "Total Damage"

# Set up the plots
fig, ax = plt.subplots(sharex=True, sharey=True)
stackplots = []
sumplots = []
ys = []

# Add Major+Minor Ticks
ax.yaxis.set_major_locator(MultipleLocator(10000))
ax.xaxis.set_major_locator(MultipleLocator(10))
ax.yaxis.set_minor_locator(AutoMinorLocator(2))
ax.xaxis.set_minor_locator(AutoMinorLocator(10))
ax.yaxis.tick_right()
ax.set_xmargin(0)
ax.set_title(title)

# Vertical line at mouseX
mousexindicator = ax.axvline(x=0, linestyle='--', alpha=0.5) 
mousexindicator.set_visible(False)


# Add annotation
annot = ax.annotate("", xy=(0,0), xytext=(-20,20),textcoords="offset points",
                bbox=dict(boxstyle="round", fc="w"))
annot.get_bbox_patch().set_alpha(0.5)
annot.set_visible(True)

# make sure i know which order the plots are handled
handledHeroes = []

selectedPlot = -1

# Handle data
for h in heroes:
    handledHeroes.append(h)
    # Total damage dealt for each damagesource
    y = []
    # Add empty list for each source
    for ds in heroes[h]:
        y.append([])
    
    # Go through the data and add to total damage
    for minute in data:
        for idx, dsource in enumerate(heroes[h]):
            val = 0
            try:
                val = data[minute][h][dsource]
            except:
                pass
            if int(minute) > 0:
                val = val+y[idx][-1]
            y[idx].append(val)
    
    # Lineplot of the total damage from each hero.
    sumplots.append(ax.plot(np.sum(y, axis=0), zorder=-5, picker=True, pickradius=4)[0])
    
    # Invisible Stackplot of the damagesources
    plots = ax.stackplot(x, y, zorder=-1)
    for p in plots:
        p.set_alpha(0.9)
        p.set_visible(False)
    stackplots.append(plots)
    
    ys.append(y)

# Handle picking
def onpick(event):
    for idx, plot in enumerate(sumplots):
        if event.artist==plot:
            toggle_plots(idx)

# Handle Hovering
def hover(event):
    if event.inaxes == ax:
        xpos = round(event.xdata)
        mousexindicator.set_xdata([xpos, xpos])
        mousexindicator.set_visible(True)
        
        # ANNOTATION FOR COMPARING PLAYERDAMAGE
        if selectedPlot == -1:
            text = ""
            # Sort the plots
            pairs = zip(handledHeroes, map(lambda plot: plot.get_ydata()[xpos], sumplots))
            sort_pairs = sorted(pairs, key=lambda o: o[1], reverse=True)
            for pair in sort_pairs:
                text+=pair[0] + ": " + str(pair[1]) + "\n"
                
            annot.set_text(text)

            annot.set_visible(True)
            annot.xy = (min(xpos+4, ax.get_xlim()[1]), 0)

           
        ######### ANNOTATION FOR STACK
        else:
            for idx, plot in enumerate(stackplots):
                if selectedPlot == idx:                
                    text = ""
                    for aid, l in enumerate(ys[idx][::-1]):
                        # Add name, damage, percentage to the annotation string
                        text+=heroes[handledHeroes[idx]][-aid-1] + ": "
                        # check total damage for percentage calculation
                        total = sumplots[idx].get_ydata()[xpos]
                        text+=str(l[xpos]) + " " + '%.1f' % (l[xpos]/total*100 if total >0 else 0) +"%\n"
                        
                    annot.set_text(text)

                    annot.set_visible(True)
                    annot.xy = (min(xpos+4, ax.get_xlim()[1]), 0)
            
        fig.canvas.draw_idle()
                
    else:
        toggle_plots(-1)
        annot.set_visible(False)
        mousexindicator.set_visible(False)
        ax.set_title(title)


# Event triggered at keypress
def keypress(event):
    try:
        i = int(event.key)
        toggle_plots(i)
    except:
        if event.key=="a":
            toggle_plots(-1)
        
# Function to toggle the visibility of plots
def toggle_plots(key):
    global selectedPlot
    selectedPlot = key
    if key == -1:
        for plots in stackplots:
            for plot in plots:
                plot.set_visible(False)
        ax.legend([],[]).remove()
    else:
        i = key
        for idx, plots in enumerate(stackplots):
            if i == idx:
                for plot in plots:
                    plot.set_visible(True)
                ax.legend(plots, heroes[handledHeroes[i]], loc='upper left')
                ax.set_title(handledHeroes[i])
                
            else:
                for idx, plot in enumerate(plots):
                    plot.set_visible(False)
    fig.canvas.draw_idle()
        
fig.canvas.mpl_connect('key_press_event', keypress)
fig.canvas.mpl_connect('pick_event', onpick)
fig.canvas.mpl_connect("motion_notify_event", hover)

# plot
plt.show()

# TODO
#### add pictures to annotations
## ReWRITE EVERYTHING to be integrated into a main app.
#### ADD buttons to toggle visiblity for each hero / team
## ADD DOTPLOT with images for each combined item on top of main hero graph
## add dotplot with deaths and images
## add dotplot with kills
