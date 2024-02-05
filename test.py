import requests
import time
import json
import js2py
import re


def str_insert(str_obj,ops,str_add):
    str_list = list(str_obj)
    str_list.insert(ops,str_add)
    str_out = "".join(str_list)
    return str_out



#找到第一段cookie __jsluid_s
url = "https://www.cnvd.org.cn/flaw/list?flag=%5BLjava.lang.String%3B%405f8eddd9&number=%E8%AF%B7%E8%BE%93%E5%85%A5%E7%B2%BE%E7%A1%AE%E7%BC%96%E5%8F%B7&startDate=&endDate=&field=&order=&numPerPage=10&offset=30&max=10"

hh = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

req = requests.get(url=url,timeout=5,headers=hh)
h1 = req.headers.__getitem__('Set-Cookie')
print(h1)







s1 = req.text
# print(s1)
s1 = s1.replace('<script>document.cookie','var a').replace(';location.href=location.pathname+location.search</script>','')
# print(s1)
h2 = js2py.eval_js(s1)

hh = h1 + ";" + h2

header = {
    "Cookie":hh,
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}
# print(header)
s2 = requests.get(url=url,timeout=5,headers=header)
s2 = s2.text
# print(s2)


#拿到js代码 并做了一些复杂的修改
s2 = s2.replace('<script>','').replace('</script>','')
s2 = '''
        window = {
            navigator:{
                userAgent:'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        };
        document = {};
        location = {};
    '''  + s2
p = s2.split('var ')[len(s2.split('var '))-1]
p = p.split('=')[0]
# print(p)
ss = str_insert(s2,len(s2.split("'is'")[0])-14,';console.log({0})'.format(p))
# print(ss)
#保存到本地，然后执行
with open('fuck.js','w',encoding='utf-8') as f:
    f.write(ss)




#把js代码拿到node去渲染 获取到第二代cookie
import subprocess
proc = subprocess.Popen(
    r'node C:\Users\intC\Desktop\fuck.js',
    stdin=None,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=True)
out,err = proc.communicate()
if out != b'undefined\n':
    h3 = out.decode('utf-8')

    #两段cookie拼接，最后去访问页面
    hhh = h1 + ";" + h3
    hhh = hhh.replace('\n','').replace(' max-age=31536000; path=/; HttpOnly; SameSite=None; secure','').replace('Max-age=3600; path = /','')
    print(hhh)

    h4 = {
        "Cookie":hhh,
        "Referer":url,
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    print(h4)
    time.sleep(2)
    s4 = requests.get(url=url,timeout=30,headers=h4)
    print(s4.text)
