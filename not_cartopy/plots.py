from matplotlib import pyplot as plt


def plot_monthly_trends(ds, datevar):
    '''plot monthly trends'''

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 3, figsize=(19, 15))
    fig.subplots_adjust(hspace=0.3, wspace=0.1)
    list_months=['January','February','March','April','May','June','July','August','September','October','November','December']

    for i in range(3):
        ax=ax1[i]
        (ds.ts.isel(time=i+40*12)-ds.ts.isel(time=i)).plot(ax=ax, vmin=-3, vmax=3, extend='both', zorder=-3)
        ax.set_title(list_months[i])

    for i in range(3):
        ax=ax2[i]
        (ds.ts.isel(time=i+3+40*12)-ds.ts.isel(time=i+3)).plot(ax = ax2[i], vmin=-3, vmax=3, extend='both', zorder=-3)
        ax.set_title(list_months[i+3])

    for i in range(3):
        ax=ax3[i]
        (ds.ts.isel(time=i+6+40*12)-ds.ts.isel(time=i+6)).plot(ax = ax, vmin=-3, vmax=3, extend='both', zorder=-3)
        ax.set_title(list_months[i+6])

    for i in range(3):
        ax=ax4[i]
        (ds.ts.isel(time=i+9+40*12)-ds.ts.isel(time=i+9)).plot(ax = ax4[i], vmin=-3, vmax=3, extend='both', zorder=-3)
        ax.set_title(list_months[i+9])

    fig.suptitle('Monthly trends: '+str(datevar[0])+' to '+str(datevar[-1]))
