"""
Errorbar plot of statistics of eddy heat flux extremes as a function
of hindcast lead time for S2S models. Reanalysis statistics are overlayed.  
"""

import numpy     as np
import xarray    as xr
from  l21        import dim_erai as dim
from l21.config  import dir_interim, dir_fig,model_names
from matplotlib  import pyplot as plt

# INPUT --------------------------------------------------
season          = 'NDJFM'
lev             = 100                # hPa                                                                                   
lats            = np.array([60,90]) # heat flux latitude averaging   
percentile_crit = 5                # percentile threshold
write2file      = 1
# --------------------------------------------------------

# define paths and dimensions
dir_in_s2s  = dir_interim + 's2s/'
dir_in_erai = dir_interim + 'erai/'
dir_out     = dir_fig

# read s2s data
var_string = 'zm.vt.' + str(lats[0]) + str(lats[-1]) + 'N.' + str(lev) + 'hpa'
filename   = var_string + '.stats.percentile.' + str(percentile_crit) + '.' + season + '.' + dim.timestamp + '.nc'
ds_s2s     = xr.open_dataset(dir_in_s2s + filename,decode_timedelta=False)
ds_erai    = xr.open_dataset(dir_in_erai + filename,decode_timedelta=False)

# plot
colors     = ['k','tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:brown','tab:pink','tab:olive','tab:cyan',[0.6,0.6,0.6]]
positions  = ds_s2s.lead_time_bin.values 
offset     = np.array([-0.3,-0.225,-0.15,-0.075,0,0.075,0.15,0.225,0.3,0.375])
fontsize   = 11
figsize    = np.array([9,10])
fig,axes   = plt.subplots(nrows=3,ncols=1,figsize=(figsize[0],figsize[1]),constrained_layout=True)

for var in range(0,3,1):
    
    for j in range(0,len(model_names),1): 
        x     = positions + offset[j]
        y     = ds_s2s.stats_median[var,j,:]
        yerr1 = ds_s2s.stats_error[var,j,:,0] 
        yerr2 = ds_s2s.stats_error[var,j,:,1]
        c     = colors[j]
        axes[var].errorbar(x=x,y=y,yerr=[yerr1,yerr2],fmt='o',c=c,elinewidth=2)
        
    axes[var].fill_between([0.5,12.5], ds_erai.stats_median[var] - ds_erai.stats_error[var,0], ds_erai.stats_error[var,1] + ds_erai.stats_median[var],color=[0.95,0.95,0.95])
    axes[var].hlines(y = ds_erai.stats_median[var], xmin = 0.5, xmax = 12.5,color=[0.6,0.6,0.6],linewidth=1.25)

    if var == 0:
        ylabelstring = r'$[V^*T^*]_{k1}$ ' + str(lats[0]) + '-' + str(lats[-1]) + 'N ' + str(lev) + ' hpa [Km/s]' 
    elif var == 1:
        ylabelstring = r'$[V^*T^*]_{k2}$ ' + str(lats[0]) + '-' + str(lats[-1]) + 'N ' + str(lev) + ' hpa [Km/s]' 
    elif var == 2:
        ylabelstring = r'$[V^*T^*]$ ' + str(lats[0]) + '-' + str(lats[-1]) + 'N ' + str(lev) + ' hpa [Km/s]'
        
    axes[var].set_ylabel(ylabelstring,fontsize=fontsize)
    axes[var].set_xticks([])
    axes[var].tick_params(axis='y', labelsize=fontsize)
    axes[var].set_xticklabels([])
    axes[var].set_xlim([0.5,12.5])

fig.suptitle(str(percentile_crit) + r'$^{th}$ percentile ' + season,fontsize=fontsize)
axes[2].set_xlabel('lead time [days]',fontsize=fontsize)
axes[2].set_xticks(positions[0:12])
axes[2].set_xticklabels(['1-5','6-10','11-15','16-20','21-25','26-30','31-35','36-40','41-45','46-50','51-55','56-60'],\
                          rotation=-20,fontsize=fontsize)

axes[0].errorbar([],[],fmt='o',c=colors[0],label=model_names[0])
axes[0].errorbar([],[],fmt='o',c=colors[1],label=model_names[1])
axes[0].errorbar([],[],fmt='o',c=colors[2],label=model_names[2])
axes[0].errorbar([],[],fmt='o',c=colors[3],label=model_names[3])
axes[0].errorbar([],[],fmt='o',c=colors[4],label=model_names[4])
axes[0].errorbar([],[],fmt='o',c=colors[5],label=model_names[5])
axes[0].errorbar([],[],fmt='o',c=colors[6],label=model_names[6])
axes[0].errorbar([],[],fmt='o',c=colors[7],label=model_names[7])
axes[0].errorbar([],[],fmt='o',c=colors[8],label=model_names[8])
axes[0].errorbar([],[],fmt='o',c=colors[9],label=model_names[9])
axes[0].errorbar([],[],fmt='o',c=[0.5,0.5,0.5],label='reanalysis')
leg = axes[0].legend(handletextpad=-2.0,markerscale=0,ncol=11,frameon=False,fontsize=10,loc='best')
for n, text in enumerate( leg.texts ):
    text.set_color( colors[n] )


if write2file == 1:
    var_string = 'zm.vt.' + str(lats[0]) + str(lats[-1]) + 'N.' + str(lev) + 'hpa'
    filename   = 'errorbar.' + var_string + '.stats.percentile.' + str(percentile_crit) + '.' + season + '.' + dim.timestamp 
    plt.savefig(dir_fig + filename + '.pdf')

plt.show()


