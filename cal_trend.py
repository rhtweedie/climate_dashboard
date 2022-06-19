def cal_trend(start_year, num_years, start_month, num_months, nx, ny, var):

    import numpy as np
    import scipy.stats as stats

    '''
    Function to calculate the spatial mean of one field and write the trends in .dat files
    returns
            ---> trend_time[year]
            ---> trend_space[x,y]
    Similar code by Alek Petty
    '''

    # Initialize
    x = nx
    y = ny

    ##################
    # Maps of trends
    ##################

    # Monthly averaged
    num_years
    years = np.arange(num_years)
    trend_ym = np.zeros((num_months, x, y))
    sig_a_ym = np.zeros((num_months, x, y))
    r_a_ym = np.zeros((num_months, x, y))
    int_a_ym = np.zeros((num_months, x, y))

    for month in range(num_months):
            print (month)
            var_y = np.mean(var,1)
            for i in range(x):
                    for j in range(y):
                            slope, intercept, r, prob, stderr = stats.linregress(years,var[start_year:start_year+num_years, month, i, j])
                            trend_ym[month, i, j] = slope
                            sig_a_ym[month, i, j] = 100*(1-prob)
                            r_a_ym[month, i, j] = r
                            int_a_ym[month, i, j] = intercept

    # Yearly averaged
    years = np.arange(num_years)
    trend = np.zeros((x, y))
    sig_a = np.zeros((x, y))
    r_a = np.zeros((x, y))
    int_a = np.zeros((x, y))

    for i in range(x):
            for j in range(y):
                    slope, intercept, r, prob, stderr = stats.linregress(years,var_y[start_year:start_year+num_years, i, j])
                    trend[i, j] = slope
                    sig_a[i, j] = 100*(1-prob)
                    r_a[i, j] = r
                    int_a[i, j] = intercept

    return trend, trend_ym, sig_a, sig_a_ym, r_a, r_a_ym, int_a, int_a_ym
