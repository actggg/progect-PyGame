data = open('regist.csv', encoding='utf-8').read()
for row in data.split('\n')[:10]:
    print(row.split(';'))