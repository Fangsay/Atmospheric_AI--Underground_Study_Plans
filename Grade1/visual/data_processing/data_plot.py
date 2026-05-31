import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import cmocean as cmo

def data_process(file_path : str,season : str = None):
    ds = xr.open_dataset(file_path)
    var = ds.attrs['variable_id']
    clim = ds[var]
    if season != None:
        clim = clim.groupby('time.season').mean(dim='time',keep_attrs=True)
        clim = clim.sel(season=season)
    else:
        clim = clim.mean(dim='time',keep_attrs=True)
    clim.attrs['units'] = 'mm/day'
    clim.data = clim.data * 86400
    clim.attrs['source_id'] = ds.attrs['source_id']
    return clim

def plot_func(data,ax : plt.Axes):
    ch = data.plot.contourf(
        ax=ax,
        levels=np.arange(0,13.5,1.5),
        transform=ccrs.PlateCarree(),
        cmap=cmo.cm.haline_r,
        add_colorbar=False
    )
    ax.set_title(data.attrs['source_id'])
    ax.coastlines()
    return ch

def data_visual(*data):
    n = len(data)
    cols = int(np.ceil(np.sqrt(n)))
    rows = int(np.ceil(n/cols))
    fig = plt.figure(1,[14,6])
    fig.suptitle('Precipitation Climatology (JJA)',fontweight='bold',fontsize=15)
    axes = []
    chs = []
    for i in range(1,n+1):
        ax = fig.add_subplot(rows,cols,i,projection=ccrs.PlateCarree(central_longitude=180))
        axes.append(ax)
    for i in range(n):
        ch = plot_func(data[i],ax=axes[i])
        chs.append(ch)
    plt.tight_layout()
    cbar = fig.colorbar(
        chs[0],
        ax=axes,
        orientation='horizontal',
        shrink=0.6,
        pad=0.1,
        extend='max',
        location='bottom'
    )
    cbar.set_label('mm/day',labelpad=10,fontsize=10,loc='right')
    plt.show()

def main():
    path1 = 'data/pr_Amon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_201001-201412.nc'
    path2 = 'data/pr_Amon_ACCESS-CM2_historical_r1i1p1f1_gn_201001-201412.nc'
    data1 = data_process(path1,season='JJA')
    data2 = data_process(path2,season='JJA')
    data_visual(data1,data2)

if __name__ == '__main__':
    main()