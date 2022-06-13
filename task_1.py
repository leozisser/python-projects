import pandas as pd
pd.set_option('display.max_colwidth', None)
df = pd.read_csv('ranking_dataset.csv')
df['org_name'] = df['address'].str.replace(r'\,.+','', regex=True).str.strip()
reg = '(\w+)(?=\.)'
df['country'] = df['address'].str.extract(reg)
#1.1.counting Russia(n)
df_id = df.drop_duplicates('id')
df_rus = df_id[df_id['title'].str.contains('Russia')]
print('\'Russia\' or \'Russian\' occured in ',len(df_rus),' publications')
#1.2 ranking organisations by authors
df_org_auth = df.drop_duplicates(['org_name', 'authour_name'])
# print(df_org_auth['org_name'].value_counts())
#1.3.ranking most productive authors by publications
df_auth_pub = df.drop_duplicates(['id', 'authour_name'])
# print(df_auth_pub['authour_name'].value_counts())
#1.4 ranking organisations by publications
df_org_pub = df.drop_duplicates(['id','org_name'])
print(df_org_pub['org_name'].value_counts()[:20])
#1.5 rating journals by publications
df_journ_id = df.drop_duplicates(['id','journal'])
# print(df_org_auth['journal'].value_counts()[:20])
