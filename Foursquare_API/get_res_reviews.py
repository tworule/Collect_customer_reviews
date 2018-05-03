# -*- coding: utf8 -*-
import json, requests
import datetime

train_text=""
final_count = 0
near_list = ['Chicago', 'Manchester', 'London', 'Liverpool', 'Oxford']


for k in range(len(near_list)):
  
  # 버거 키워드로 검색 시 추천 식당받기
  
  params = dict(
    client_id='',
    client_secret='',
    v='20170801',
    near = near_list[k],
    #near='Chicago',
    #section = 'food',
    query='meal',
    limit=50
  )

  #EXPLORE = get venue recommendations
  url = 'https://api.foursquare.com/v2/venues/explore'
  resp = requests.get(url=url, params=params)
  data = json.loads(resp.text)

  res_id = []
  res_name = []
  for i in range(len(data['response']['groups'][0]['items'])):
    res_id.append(data['response']['groups'][0]['items'][i]['venue']['id'])
    res_name.append(data['response']['groups'][0]['items'][i]['venue']['name'])


  count = 0
  url1 = 'https://api.foursquare.com/v2/venues/'
  url3 = '/tips'
  for i in range(len(res_name)):
    url2 = str(res_id[i])
    url = url1+url2+url3
    params2 = dict(
      venue_id = url2,
      client_id='FN5PS1FYKITOSMYDRGMK3UGQVAVZD5GNTCPGBDTFDHJLMC42',
      client_secret='PXPLYT5M23203GXN4ABRCZEKC5ETYJX3EU3SQZKDF20FNSXC',
      sort = 'popular', #popular , recent 가능
      limit= 1000,
      offset=1,
      v='20170101'
    )


    resp = requests.get(url = url, params=params2)
    data = json.loads(resp.text)
    print('----------------------------------------')
    print(res_name[i], '식당의 리뷰 수집')
    print('----------------------------------------')
    print('리뷰 수 : ',data['response']['tips']['count'])
    for j in range(len(data['response']['tips']['items'])):
      print(j+1, " ",data['response']['tips']['items'][j]['text'])
      
      train_text = train_text + str(data['response']['tips']['items'][j]['text'])
      train_text = train_text + " :flag: "
      count += 1
      when = data['response']['tips']['items'][j]['createdAt']
      when = datetime.datetime.fromtimestamp(when)
      print('   의 리뷰 작성일 :  ',when)

  print('---------------------------------------------')
  print(near_list[k], '지역의 수집 리뷰 : ',count, '개')
  print('---------------------------------------------')
  final_count += count

print('최종 수집 리뷰 : ', final_count,'개')


# SAVE REVIEW
f = open('./train_reviews.txt','w')
f.write(train_text)
f.close()