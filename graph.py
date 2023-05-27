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
for min in data:
    for h in data[min].keys():
        if not h in heroes:
            heroes[h] = []
        for ds in data[min][h]:
            if not ds in heroes[h]:
                heroes[h].append(ds)
            

# Time
x = data.keys()

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

# Vertical line at mouseX
mousexindicator = ax.axvline(x=0, linestyle='--', alpha=0.5) 
mousexindicator.set_visible(False)


# Add annotation
annot = ax.annotate("", xy=(0,0), xytext=(-20,20),textcoords="offset points",
                bbox=dict(boxstyle="round", fc="w"))
annot.get_bbox_patch().set_alpha(0.7)
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
    for min in data:
        for idx, dsource in enumerate(heroes[h]):
            val = 0
            try:
                val = data[min][h][dsource]
            except:
                pass
            if int(min) > 0:
                y[idx].append(val+y[idx][-1])
            else:
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
            annot.xy = (xpos, 0)

           
        ######### ANNOTATION FOR STACK
        else:
            for idx, plot in enumerate(stackplots):
                if selectedPlot == idx:                
                    text = ""
                    for aid, l in enumerate(ys[idx][::-1]):
                        text+=heroes[handledHeroes[idx]][-aid-1] + ": "
                        text+=str(l[xpos]) + "\n"
                        
                    annot.set_text(text)

                    annot.set_visible(True)
                    annot.xy = (xpos, 0)
            
        fig.canvas.draw_idle()
                
    else:
        toggle_plots(-1)
        annot.set_visible(False)
        mousexindicator.set_visible(False)
        ax.set_title("Total Damage")


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
## CHANGE TOGGLEGRAPH TO PICK INSTEAD OF HOVER