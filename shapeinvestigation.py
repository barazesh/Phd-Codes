import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def main():
    step_range = [2**-p for p in range(13)]
    period_range = [1, 6, 12, 24]
    # investigatePeriod(period_range, step_range[7])
    investigateBoth(step_range=step_range,period_range=period_range)


def investigatePeriod(period_range, step):
    price = {}
    for p in period_range:
        price[p] = pd.read_csv(f'./Outputs/period_{p}_timestep_{step}.csv', usecols=[
            'TIME', 'Electricity Tariff'], squeeze=True, index_col=0, dtype='float64')

    # fig_v, ax_v = plt.subplots(len(period_range), 1)
    # fig_v.set_size_inches(5, len(period_range)*5)
    # for i, p in enumerate(period_range):
    #     ax_v[i].plot(price[p])
    #     ax_v[i].grid(True, linestyle='--')
    #     ax_v[i].title.set_text(f'Period={p}')

    # fig_h, ax_h = plt.subplots(1,len(period_range))
    # fig_h.set_size_inches(len(period_range)*5,5)
    # for i, p in enumerate(period_range):
    #     ax_h[i].plot(price[p])
    #     ax_h[i].grid(True, linestyle='--')
    #     ax_h[i].title.set_text(f'Period={p}')

    fig_c, ax_c = plt.subplots()
    fig_c.set_size_inches(16, 9)
    for i, p in enumerate(period_range):
        ax_c.plot(price[p], label=str(p))
    ax_c.title.set_text(f'Time Step={step}')
    ax_c.grid(True, linestyle='--')
    ax_c.legend(title='Tariff correction period (months)')
    plt.show()


def investigateTimeStep(step_range, period):
    price = {}
    for s in step_range:
        price[s] = pd.read_csv(f'./Outputs/period_{period}_timestep_{s}.csv', usecols=[
                               'TIME', 'Electricity Tariff'], squeeze=True, index_col=0, dtype='float64')
    fig, ax = plt.subplots(len(step_range), 1)
    fig.set_size_inches(18, len(step_range)*5)
    for i, s in enumerate(step_range):
        ax[i].plot(price[s])
        ax[i].grid(True, linestyle='--')
        ax[i].title.set_text(f'Time Step={s}')


def investigateBoth(step_range, period_range):
    price = {}
    for p in period_range:
        price[p] = {}
        for s in step_range:
            price[p][s] = pd.read_csv(f'./Outputs/period_{p}_timestep_{s}.csv', usecols=[
                                    'TIME', 'Electricity Tariff'], squeeze=True, index_col=0, dtype='float64')
    fig_max,ax_max=plt.subplots(len(period_range)//2,2)

    fig,ax = plt.subplots(len(step_range),len(period_range))
    fig.set_size_inches(len(period_range)*5,len(step_range)*5)
    plt.tight_layout()

    fig_d,ax_d = plt.subplots(len(step_range),len(period_range))
    fig_d.set_size_inches(len(period_range)*5,len(step_range)*5)
    for i,p in enumerate(period_range):
        max_price=[]
        for j,s in enumerate(step_range):
            max_price.append(max(price[p][s]))
            ax[j,i].plot(price[p][s])
            ax[j,i].grid(True,linestyle='--')
            y=price[p][s].to_numpy()
            dif=[]
            for k,sex in enumerate(y):
                if (k-1)%(p/s)==0:
                    dif.append(y[k]-y[k-1])
            ax_d[j,i].plot(dif)
            ax_d[j,i].grid(True,linestyle='--')
            # ax[j,i].title.set_text(f'Time Step:{s}---tariff corr period:{p}')
        ax_max[i//2,i%2].plot(max_price)
        ax_max[i//2,i%2].grid(True,linestyle='--')
        ax_max[i//2,i%2].title.set_text(f'Tariff correction period:{p}')

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
