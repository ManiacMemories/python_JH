
    
import requests as req

if __name__=="__main__":
    url = "https://finance.naver.com/sise/sise_market_sum.naver"
    web = req.get(url)
    html = web.text
    # print(html)
    f1 = html.find('삼성전자')
    print('삼성전자:'+html[f1:f1+100][19:50].replace('<td class="number">',"").replace('</td>',"").replace('\n',"") + "원")
    f2 = html.find('기아')
    print('기아:'+html[f2:f2+100][17:50].replace('<td class="number">',"").replace('</td>',"").replace('\n',"").replace('\t',"") + "원")
    print("전 파일로 실행이 되었어요.")
else:
    print("전 모듈로 임포트 되었어요.")
    
    