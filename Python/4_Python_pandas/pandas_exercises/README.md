# Pandas Exercises

Fed up with a ton of tutorials but no easy way to find exercises I decided to create a repo just with exercises to practice pandas.
Don't get me wrong, tutorials are great resources, but to learn is to do. So unless you practice you won't learn.

There will be three different types of files:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. Exercise instructions  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. Solutions without code  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3. Solutions with code and comments

My suggestion is that you learn a topic in a tutorial or video and then do exercises.
Learn one more topic and do exercises. If you got the answer wrong, don't go directly to the solution with code.

Suggestions and collaborations are more than welcome. Please open an issue or make a PR. :)

# pandas - 100 progress
pandas 100문제를 풀면서 pandas의 여러 기능들을 익혀봅니다.
- [pandas_exercises](https://github.com/guipsamora/pandas_exercises)
  - [x] 01_Getting_&_Knowing_Your_Data
  - [x] 02_Filtering_&_Sorting
  - [x] 03_Grouping
  - [x] 04_Apply
  - [x] 05_Merge
  - [x] 06_Stats
  - [x] 07_Visualization
  - [ ] 08_Creating_Series_and_DataFrames
  - [ ] 09_Time_Series
  - [ ] 10_Deleting
  - [ ] 11_Indexing

# Lessons

|				                                  |				                                   |                   |
|:-----------------------------------------------:|:----------------------------------------------:|:-----------------:|
|[Getting and knowing](#getting-and-knowing)      | [Merge](#merge)                                |[Time Series](#time-series)|
|[Filtering and Sorting](#filtering-and-sorting)  | [Stats](#stats)                                |[Deleting](#deleting)       |
|[Grouping](#grouping)							  | [Visualization](#visualization)                |Indexing           |
|[Apply](#apply)							      | [Creating Series and DataFrames](#creating-series-and-dataframes) 		            |Exporting|

## Getting and knowing

### Chipotle
- df.head()
- df.shape
- df.columns
- df.index
- df.groupby & sort_values
- df.value_counts()

### Occupation
- df.head, df.tail
- df.dtypes
- df.'column_name' or df['column_name']
- df.nunique()
- df.describe(include='all')

### World Food Facts
- df.info()

## Filtering and Sorting

### Chipotle  
- preprocessing

```python
def price(x):
    res = float(x[1:-1])
    
    return res

chipo['price'] = chipo['item_price'].apply(lambda x : price(x))
```
- df.drop_duplicates(['item_name','quantity'])
- df.sort_values(by = 'price', ascending=False)

### Euro12  
- multiple sort in pandas dataframe
  - 괄호로 처리하는 것 잊지 말 

```python
discipline.sort_values(by = ['Red Cards', 'Yellow Cards'], ascending=False)
```
- df['column'].str.startwith(str_value)
  - 지정된 문자열로 시작되는 경우를 리턴
```python
Dataframe['column'].str.startswith()

euro12[euro12.Team.str.startswith('G')]
```

- df.iloc[row, col]
```python
euro12.iloc[:, :7]

euro12.iloc[:, :-3]
```

- df.isin
  - isin을 사용하면 특정 컬럼 내 존재하는 값을 가지는 row를 리턴한다.
  - https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.isin.html

```python
euro12[euro12.Team.isin(['England', "Italy", "Russia"])][['Team', 'Shooting Accuracy']]
```

```bash
Team	Shooting Accuracy
3	England	50.0%
7	Italy	43.0%
12	Russia	22.5%
```


```python
euro12.loc[euro12.Team.isin(['England', 'Italy', 'Russia']), ['Team','Shooting Accuracy']]
```

```bash
Team	Shooting Accuracy
3	England	50.0%
7	Italy	43.0%
12	Russia	22.5%
```

### Fictional Army

- dict to pandas dataframe

````python
# Create an example dataframe about a fictional army
raw_data = {'regiment': ['Nighthawks', 'Nighthawks', 'Nighthawks', 'Nighthawks', 'Dragoons', 'Dragoons', 'Dragoons', 'Dragoons', 'Scouts', 'Scouts', 'Scouts', 'Scouts'],
            'company': ['1st', '1st', '2nd', '2nd', '1st', '1st', '2nd', '2nd','1st', '1st', '2nd', '2nd'],
            'deaths': [523, 52, 25, 616, 43, 234, 523, 62, 62, 73, 37, 35],
            'battles': [5, 42, 2, 2, 4, 7, 8, 3, 4, 7, 8, 9],
            'size': [1045, 957, 1099, 1400, 1592, 1006, 987, 849, 973, 1005, 1099, 1523],
            'veterans': [1, 5, 62, 26, 73, 37, 949, 48, 48, 435, 63, 345],
            'readiness': [1, 2, 3, 3, 2, 1, 2, 3, 2, 1, 2, 3],
            'armored': [1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1],
            'deserters': [4, 24, 31, 2, 3, 4, 24, 31, 2, 3, 2, 3],
            'origin': ['Arizona', 'California', 'Texas', 'Florida', 'Maine', 'Iowa', 'Alaska', 'Washington', 'Oregon', 'Wyoming', 'Louisana', 'Georgia']}

army = pd.DataFrame(
    raw_data, 
    columns = [
        'regiment', 
        'company', 
        'deaths', 
        'battles', 
        'size', 
        'veterans', 
        'readiness', 
        'armored', 
        'deserters', 
        'origin']
)

army = pd.DataFrame.from_dict(raw_data)
````

- df.set_index('origin')

```bash
	regiment	company	deaths	battles	size	veterans	readiness	armored	deserters
origin									
Arizona	Nighthawks	1st	523	5	1045	1	1	1	4
California	Nighthawks	1st	52	42	957	5	2	0	24
Texas	Nighthawks	2nd	25	2	1099	62	3	1	31
Florida	Nighthawks	2nd	616	2	1400	26	3	1	2
Maine	Dragoons	1st	43	4	1592	73	2	0	3
Iowa	Dragoons	1st	234	7	1006	37	1	1	4
Alaska	Dragoons	2nd	523	8	987	949	2	0	24
Washington	Dragoons	2nd	62	3	849	48	3	1	31
Oregon	Scouts	1st	62	4	973	48	2	0	2
Wyoming	Scouts	1st	73	7	1005	435	1	0	3
Louisana	Scouts	2nd	37	8	1099	63	2	1	2
Georgia	Scouts	2nd	35	9	1523	345	3	1	3
```

- df.loc
  - https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html
  - .loc[] is primarily label based, but may also be used with a boolean array.

- df.columns.get_loc['column']
  - https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Index.get_loc.html
  - 특정 컬럼의 인덱스 값을 리턴한다.
  
## Grouping


### Alcohol Consumption  
- df.groupby['column']['column'].describe()
```python
drinks.groupby('continent')['wine_servings'].describe()
```

- df.groupby('column').agg(function)

```python
df = pd.DataFrame({
        'A': [1, 1, 2, 2],
        'B': [1, 2, 3, 4],
        'C': np.random.randn(4)}
)


df.groupby('A').agg('min')
   B         C
A
1  1  0.227877
2  3 -0.562860

df.groupby('A').agg(['min', 'max'])
    B             C
  min max       min       max
A
1   1   2  0.227877  0.362838
2   3   4 -0.562860  1.267767

df.groupby('A').B.agg(['min', 'max'])
   min  max
A
1    1    2
2    3    4

df.groupby('A').agg({'B': ['min', 'max'], 'C': 'sum'})
    B             C
  min max       sum
A
1   1   2  0.590716
2   3   4  0.704907
```

### Occupation  
- 직접 볼 것

### Regiment
- df.unstack
```python
index = pd.MultiIndex.from_tuples([('one', 'a'), ('one', 'b'),
                                   ('two', 'a'), ('two', 'b')])
s = pd.Series(np.arange(1.0, 5.0), index=index)
s
one  a   1.0
     b   2.0
two  a   3.0
     b   4.0
     
     
s.unstack(level=-1)
     a   b
one  1.0  2.0
two  3.0  4.0


s.unstack(level=0)
   one  two
a  1.0   3.0
b  2.0   4.0


df = s.unstack(level=0)
df.unstack()
one  a  1.0
     b  2.0
two  a  3.0
     b  4.0
```


### [Apply](https://github.com/guipsamora/pandas_exercises/tree/master/04_Apply)
[Students Alcohol Consumption](https://github.com/guipsamora/pandas_exercises/tree/master/04_Apply/Students_Alcohol_Consumption)  
[US_Crime_Rates](https://github.com/guipsamora/pandas_exercises/tree/master/04_Apply/US_Crime_Rates)     

### [Merge](https://github.com/guipsamora/pandas_exercises/tree/master/05_Merge)
[Auto_MPG](https://github.com/guipsamora/pandas_exercises/tree/master/05_Merge/Auto_MPG)  
[Fictitious Names](https://github.com/guipsamora/pandas_exercises/tree/master/05_Merge/Fictitous%20Names)  
[House Market](https://github.com/guipsamora/pandas_exercises/tree/master/05_Merge/Housing%20Market)  

### [Stats](https://github.com/guipsamora/pandas_exercises/tree/master/06_Stats)
[US_Baby_Names](https://github.com/guipsamora/pandas_exercises/tree/master/06_Stats/US_Baby_Names)  
[Wind_Stats](https://github.com/guipsamora/pandas_exercises/tree/master/06_Stats/Wind_Stats)

### [Visualization](https://github.com/guipsamora/pandas_exercises/tree/master/07_Visualization)
[Chipotle](https://github.com/guipsamora/pandas_exercises/tree/master/07_Visualization/Chipotle)  
[Titanic Disaster](https://github.com/guipsamora/pandas_exercises/tree/master/07_Visualization/Titanic_Desaster)  
[Scores](https://github.com/guipsamora/pandas_exercises/tree/master/07_Visualization/Scores)  
[Online Retail](https://github.com/guipsamora/pandas_exercises/tree/master/07_Visualization/Online_Retail)  
[Tips](https://github.com/guipsamora/pandas_exercises/tree/master/07_Visualization/Tips)  

### [Creating Series and DataFrames](https://github.com/guipsamora/pandas_exercises/tree/master/08_Creating_Series_and_DataFrames)  
[Pokemon](https://github.com/guipsamora/pandas_exercises/tree/master/08_Creating_Series_and_DataFrames/Pokemon)  

### [Time Series](https://github.com/guipsamora/pandas_exercises/tree/master/09_Time_Series)  
[Apple_Stock](https://github.com/guipsamora/pandas_exercises/tree/master/09_Time_Series/Apple_Stock)  
[Getting_Financial_Data](https://github.com/guipsamora/pandas_exercises/tree/master/09_Time_Series/Getting_Financial_Data)  
[Investor_Flow_of_Funds_US](https://github.com/guipsamora/pandas_exercises/tree/master/09_Time_Series/Getting_Financial_Data)  

### [Deleting](https://github.com/guipsamora/pandas_exercises/tree/master/10_Deleting)  
[Iris](https://github.com/guipsamora/pandas_exercises/tree/master/10_Deleting/Iris)  
[Wine](https://github.com/guipsamora/pandas_exercises/tree/master/10_Deleting/Wine)  

