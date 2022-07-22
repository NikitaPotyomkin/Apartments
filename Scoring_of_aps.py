import pandas as pd
pd.set_option('display.max_columns', 500)

class DataframeToScore():
    def __init__(self,df_to_score):
        self.df_to_score = pd.read_excel(df_to_score,engine='openpyxl')

    def show_df(self):
        print(self.df_to_score)

    def score_df(self):
        df = self.df_to_score
        columns_list = [["Цена за метр",True],["Площадь",False],["Удаленность_от_метро",True]]
        # df = df.drop(df[(df.Удаленность_от_метро ==10)].index)
        i = 0
        for x in columns_list:
            column_to_score = x[0]
            new_column = "Расч. " +column_to_score
            column = df[column_to_score]
            max_value = column.max()
            min_value = column.min()
            dependency_straight = x[1]
            coeff = (max_value - column) / (max_value - min_value)
            if dependency_straight ==True:
                df[new_column] = 100*coeff
            else:
                df[new_column] = 100*(1 - coeff)
            i+=1
        df['Итоговый балл'] = df.loc[:,df.columns[-i:]].sum(1)
        df['Комментарий'] = "Тут будет комментарий"
        df = df.sort_values('Итоговый балл',ascending=False)
        df.to_excel("scored_offers.xlsx",index = False)

our_data_frame = DataframeToScore('Подходящие предложения.xlsx')
our_data_frame.score_df()


