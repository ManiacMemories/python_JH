
    
import requests as req


url = "https://finance.naver.com/sise/sise_market_sum.naver"
web = req.get(url)
html = web.text
# print(html)
def sam(jong='삼성전자'):
    f1 = html.find(jong)
    return(f'{jong} : ' +html[f1:f1+100][19:50].replace('<td class="number">',"").replace('</td>',"").replace('
',"") + "원")

def kia(jong='기아'):
    f2 = html.find(jong)
    return(f'{jong} : ' +html[f2:f2+100][17:50].replace('<td class="number">',"").replace('</td>',"").replace('
',"").replace('	',"") + "원")

if __name__=="__main__":
    name = input("종목을 입력하세요 : ")
    if name == "삼성전자":
        print(sam())
        print("전 파일로 실행이 되었어요.")
    elif name == "기아":
        print(kia())
        print("전 파일로 실행이 되었어요.")
else:
    print("전 모듈로 임포트 되었어요.")
    
    
    