import requests
url = 'https://www.vg.no'
url = 'https://www.nrk.no'

headers = {
    'Accept-Charset':'utf-8'
}
#r = requests.Request('GET',url, header=header)
r = requests.get(url)#,headers=headers,)
r.encoding = 'utf-8'
with open('utf8-nrk.txt', 'w',encoding='utf-8') as file:
    file.write(r.text)
print(r.text)


print(r.encoding)