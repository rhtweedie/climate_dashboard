def retrieve_data(temp_res, experiment, variable, model, date):

    '''
    Function to retrieve data from the Copernicus Climate Data Store.
    temp_res: 'monthly'
    experiment: 'ssp5_8_5' / 'ssp1_2_6'
    variable: 'surface_temperature'
    model: 'hadgem3_gc31_ll'
    date: '2015-01-01/2099-12-31'
    '''

    import cdsapi
    import zipfile
    import os

    c = cdsapi.Client()

    file_name = f'./download_{model}_{experiment}.zip'

    c.retrieve(
        'projections-cmip6',
        {
            'format': 'zip',
            'temporal_resolution': temp_res,
            'experiment': experiment,
            'level': 'single_levels',
            'variable': variable,
            'model': model,
            'date': date,
        },
        file_name)

    with zipfile.ZipFile(file_name, 'r') as zip_ref:      
        zip_ref.extractall('data')
        print("Data files extracted")
    os.remove(file_name)
    print("Zipped file removed")

    dir = os.fsencode('data')
    for file in os.listdir(dir):
        filename = os.fsdecode(file)
        if filename.endswith('.nc'):
            os.rename(f'data/{filename}', f'{model}_{experiment}_data.nc')
        else:
            os.remove(f'data/{filename}')
    os.rmdir('data')

    data_fn = f'{model}_{experiment}_data.nc'
    return data_fn


if __name__ == "__main__":
    retrieve_data('monthly', 'ssp5_8_5', 'surface_temperature', 'hadgem3_gc31_ll', '2015-01-01/2099-12-31')
