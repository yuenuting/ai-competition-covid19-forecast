def show(X1, Y1, X2, Y2):
    import matplotlib.pyplot as plt
    plt.figure()
    plt.get_current_fig_manager().window.showMaximized()
    plt.ticklabel_format(style='plain')
    plt.plot([x[5:] for x in X1], Y1, label='global confirmed cases, historical', color='r', marker='o')
    plt.plot([x[5:] for x in X2], Y2, label='global confirmed cases, forecasted', color='b', marker='o')
    plt.title('YUE-NuTing: AI Covid-19 Forcasting')
    plt.legend(loc='upper left')
    plt.savefig('covid19-forcast.png')
    plt.show()

def data(makeHosts=0, downData=0, tidyData=0, pickData=0):
    if makeHosts:  #构造hosts，处理长城防火墙对raw.githubusercontent.com的DNS污染
        hosts = open(r'C:\WINDOWS\system32\drivers\etc\hosts', 'w')
        hosts.write('151.101.184.133 raw.githubusercontent.com')
        hosts.close()

    import pandas as pd
    if downData:  #下载数据
        url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
        dataFrame = pd.read_csv(url)
        dataFrame.to_csv('covid19-0-raw.csv', index=False)

    if tidyData:  #整理数据
        import time
        dataFrame = pd.read_csv('covid19-0-raw.csv')
        dataFrame = dataFrame.drop(['Lat', 'Long'], axis=1)
        dataFrame = dataFrame.groupby('Country/Region').sum()  #重要
        dataFrame = dataFrame.sort_values(dataFrame.columns[-1], ascending=False)
        dataFrame.rename(columns=lambda x: time.strftime('%Y-%m-%d', time.strptime(x,'%m/%d/%y')), inplace=True)
        dataFrame.to_csv('covid19-1-own.csv', index=True)

    if pickData:  #选择数据
        dataFrame = pd.read_csv('covid19-1-own.csv')
        dataFrame = dataFrame.loc[:, dataFrame.columns[-7*1:]]
        dataFrame.to_csv('covid19-2-few.csv', index=False)

    if 1:  #汇总数据
        dataFrame = pd.read_csv('covid19-2-few.csv')
        dataFrame = dataFrame.sum()
        dataFrame.to_csv('covid19-3-sum.csv', index=True)
        X = []
        Y = []
        for i,v in dataFrame.items():
            X.append(i)
            Y.append(int(v))
        return X, Y

def forecast(X1, Y1, X2):   #last date of Y1 is 2020-08-19
    total = 0
    for i in range(1, 7):
        total += Y1[i] - Y1[i-1]
    average = total / 6  
    Y2 = []
    for i in range(0,len(X2)):  #skip 08-20
        Y2.append(Y1[-1] + (average*(i+1)))
    return Y2

if __name__ == '__main__':
    X1,Y1 = data(makeHosts=0, downData=0, tidyData=0, pickData=0)
    Xa = []  #提前天
    Xt = ['2020-08-20']  #时差天
    X2 = Xa + Xt + ['2020-08-21', '2020-08-22','2020-08-23', '2020-08-24','2020-08-25', '2020-08-26','2020-08-27']
    Y2 = forecast(X1, Y1, X2)
    if 1:
        for y in Y2[len(Xt)+len(Xa):]:
            print(int(y))
    else:
        for x,y in zip(X2[len(Xt)+len(Xa):],Y2[len(Xt)+len(Xa):]):
            print(x,' ',int(y))
    show(X1,Y1, X2, Y2)
