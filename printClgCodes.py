import pickle

with open('Resources/collegeCodes','rb') as g:
    clgCodeList = pickle.load(g)

print('\n{0:65}  {1:^5}'.format('College Name','College Code'))
print('{0:65}  {1:^5}'.format('------------','------------'))
print()
for clg,code in clgCodeList.items():
    print('{0:-<65}  {1:^5}'.format(clg,code))
