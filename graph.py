import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

# Basic stacked area chart.
data = {}
import json
with open('data.json') as json_file:
    data = json.load(json_file)
   
heroes = {}

for min in data:
    for h in data[min].keys():
        if not h in heroes:
            heroes[h] = []
        for ds in data[min][h]:
            if not ds in heroes[h]:
                heroes[h].append(ds)
            

# Create data
x = data.keys()
# Basic stacked area chart.
fig, ax = plt.subplots(sharex=True, sharey=True)
stackplots = []
sumplots = []
handledHeroes = []

for h in heroes:
    # Handle data
    handledHeroes.append(h)
    y = []
    for a in heroes[h]:
        y.append([])
    for min in data:
        for idx, ability in enumerate(heroes[h]):
            val = 0
            try:
                val = data[min][h][ability]
            except:
                pass
            if int(min) > 0:
                y[idx].append(val+y[idx][-1])
            else:
                y[idx].append(val)
    
    plots = ax.stackplot(x, y)
    for p in plots:
        p.set_alpha(0.65)
        p.set_visible(False)
    stackplots.append(plots)
    # Add Major+Minor Ticks
    ax.yaxis.set_major_locator(MultipleLocator(10000))
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax.yaxis.tick_right()
    ax.set_xmargin(0)
    # Add annotation
    # annot = ax.annotate("", xy=(0,0), xytext=(-20,20),textcoords="offset points",
                    # bbox=dict(boxstyle="round", fc="w"))
    # annot.set_visible(True)
    
    ax.plot(np.sum(y, axis=0))
    
    
    # def hover(event):
        # try:
            # xpos = round(event.xdata)
            # text = ""
            # for l in y[::-1]:
                # text+=str(l[xpos]) + "\n"
                
            # annot.set_text(text)

            # annot.set_visible(True)
            # annot.get_bbox_patch().set_alpha(0.4)
            # annot.xy = (xpos, 0)


        # except:
            # annot.set_visible(False)
        # finally:
            # fig.canvas.draw_idle()
        
    
    # fig.canvas.mpl_connect("motion_notify_event", hover)
    
# Function to toggle the visibility of plots
def toggle_plots(event):
    try:
        i = int(event.key)
        for idx, plots in enumerate(stackplots):
            if i == idx:
                for plot in plots:
                    plot.set_visible(True)
                ax.legend(plots, heroes[handledHeroes[i]], loc='upper left')
                ax.set_title(handledHeroes[i])
                
            else:
                for idx, plot in enumerate(plots):
                    plot.set_visible(False)
    except:
        if event.key=="a":
            for plots in stackplots:
                for plot in plots:
                    plot.set_visible(False)
            ax.legend([],[]).remove()
    finally:
        fig.canvas.draw_idle()
        
fig.canvas.mpl_connect('key_press_event', toggle_plots)

# plot
plt.show()

# TODO
## ADD TOGGLE ON HOVER
## ADD ANNOTATION