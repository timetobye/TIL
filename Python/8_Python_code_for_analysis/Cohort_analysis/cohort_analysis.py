import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from matplotlib import font_manager, rc
apple = font_manager.FontProperties(fname = '/Library/Fonts/AppleGothic.ttf').get_name()
rc('font', family = apple)

sns.set(style='white')


# 파일 읽기
def read_excel(file_path, sheet_name=None):
    # change sheet name when you use your dataset
    df = pd.read_excel(file_path, sheet_name='Purchase Data - Full Study')

    return df


def create_period_column(df):
    df['OrderPeriod'] = df.OrderDate.apply(lambda x: x.strftime('%Y-%m'))

    return df


def create_cohort_group_column(df):
    df.set_index('UserId', inplace=True)
    df['CohortGroup'] = df.groupby(level=0)['OrderDate'].min().apply(lambda x: x.strftime('%Y-%m'))
    df.reset_index(inplace=True)

    return df


def create_cohort_dataframe(df):
    grouped = df.groupby(['CohortGroup', 'OrderPeriod'])

    cohorts_df = grouped.agg({
        'UserId': pd.Series.nunique,
        'OrderId': pd.Series.nunique,
        'TotalCharges': np.sum
    })

    # make the column names more meaningful
    cohorts_df.rename(columns={'UserId': 'TotalUsers', 'OrderId': 'TotalOrders'}, inplace=True)

    return cohorts_df


def calc_cohort_period(df):
    df['CohortPeriod'] = np.arange(len(df)) + 1

    return df


def label_cohort_period(cohorts_dataframe):
    applied_cohort_period = cohorts_dataframe.groupby(level=0).apply(calc_cohort_period)

    return applied_cohort_period


def make_user_retention_table(cohort_df):
    # reindex the DataFrame
    cohort_df.reset_index(inplace=True)
    cohort_df.set_index(['CohortGroup', 'CohortPeriod'], inplace=True)

    # create a Series holding the total size of each CohortGroup
    cohort_group_size = cohort_df['TotalUsers'].groupby(level=0).first()

    user_retention_df = cohort_df['TotalUsers'].unstack(0).divide(cohort_group_size, axis=1)

    return user_retention_df


def draw_retention_graph(retention_table):
    plt.figure(figsize=(12, 8))
    plt.title('Cohorts: User Retention')
    sns.heatmap(
        retention_table.T,
        mask=retention_table.T.isnull(),
        annot=True,
        fmt='.0%',
        cmap="YlGnBu"
    )

    save_time = datetime.strftime(datetime.now(), '%Y-%m-%d')
    file_name = f'User_retention_graph_{save_time}'

    plt.savefig(file_name)

    plt.show()


def pre_process_cohort_data(df):
    added_period_column_df = create_period_column(df)
    added_cohort_group_column_df = create_cohort_group_column(added_period_column_df)
    cohort_df = create_cohort_dataframe(added_cohort_group_column_df)
    added_label_cohort_df = label_cohort_period(cohort_df)

    return added_label_cohort_df


def main():
    user_raw_data_df = read_excel('../Data_set/relay-foods.xlsx', sheet_name='Purchase Data - Full Study')
    pre_process_completed_cohort_df = pre_process_cohort_data(user_raw_data_df)
    user_retention_df = make_user_retention_table(pre_process_completed_cohort_df)

    draw_retention_graph(user_retention_df)


if __name__ == "__main__":
    main()


