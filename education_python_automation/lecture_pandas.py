import pandas as pd

data = {
    'Movie Title' : ['His House', 'How to Train Your Dragon', 'The Forty-Year-Old Version',
                     'Under the Shadow', 'Monty Python and the Holy Grail'],
    'Year' : [2020, 2010, 2020, 2016, 1975],
    'Score' : [100, 98, 95, 89, 86],
    'Director' : ['Remi Weekes', 'Christopher Sanders', 'Radha Blank', 'Babak Anvari', 'Terry Gilliam'],
    'Cast' : ['Wunmi Mosaku, Sope Dirisu', 'Jay Baruchel, Gerard Butler', 'Welker White, Reed Birney',
              'Narges Rashidi, Avin Manshadi', 'Graham Chapman, John Cleese']
}

df = pd.DataFrame(data)
idx_lst = ['100','200','300','400','500']
df = pd.DataFrame(data, index=idx_lst)

df = pd.DataFrame(data , columns=['movie','title','score'])


'series'
score = [100,90,59,39,80]
s = pd.Series(score, index=['1st','2nd','4th','5th','3rd'])
s.index
s.name= 'score'
s.index.name='score_index'

df = pd.DataFrame(data, index=idx_lst)
df.index
df.index.name= 'rank'
df = df.reset_index()

df.reset_index(drop=True)
df.reset_index(drop=True)


df.sort_index(ascending=False)
df.rename(columns={'Year':'Releas', 'Cast':'Actor'})
df = df.rename(index={'His Houes':'My House'})

