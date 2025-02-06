import requests
import json
url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=V6nLvpItarPinUqXxkMz40yEICS7bHgt&data=AP01'
res = requests.get(url).text
data = json.loads(res)
result = (data[-1]['deal_bas_r'])
print('='*40)
print(f'오늘의 환율은 1달러($)에 {result}원 입니다.')
print('='*40)