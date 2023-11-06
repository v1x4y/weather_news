import requests,json
from bs4 import BeautifulSoup

latitude = "35.681236"
longitude = "139.767125"
lang = "ja"
url=f"https://weathernews.jp/onebox/{latitude}/{longitude}/lang={lang}"
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, "html.parser")
loc=soup.find("h1", class_="index__tit").text
res=soup.find("div", class_="switchPcArea")
content=res.find("div", class_="switchContent__item act")
head=content.find("div", class_="wTable__head")
h_day=head.find("div",class_="wTable__row").find("p",class_="wTable__item day").text
h_time=head.find("div",class_="wTable__row").find("p",class_="wTable__item time").text
h_weather=head.find("div",class_="wTable__row").find("p",class_="wTable__item weather").text
h_r=head.find("div",class_="wTable__row").find("p",class_="wTable__item r").text
h_temp=head.find("div",class_="wTable__row").find("p",class_="wTable__item t").text
h_wind=head.find("div",class_="wTable__row").find("p",class_="wTable__item w").text
body=content.find("div", class_="wTable__body")
days=body.find_all("div", class_="wTable__group")
data={
  loc:{
    
  }
}
js=data[loc]
with open("weather.json","r",encoding="utf-8") as f:
  w_js=json.load(f)
with open("direction.json","r",encoding="utf-8") as f:
  w_di=json.load(f)
for day in days:
  day_name=day.find("div", class_="wTable__day").text.replace("\n","")
  day_data=day.find("div", class_="wTable__content").find_all("div", class_="wTable__row")
  for dd in day_data:
    js[day_name]={
      dd.find("p", class_="wTable__item time").text+f"{h_time}":{
        h_weather:{
          w_js[dd.find("p", class_="wTable__item weather").find("img")["src"].split("/wxicon/")[1].split(".")[0]]["meaning"]:w_js[dd.find("p", class_="wTable__item weather").find("img")["src"].split("/wxicon/")[1].split(".")[0]]["detail"]
        },
        h_r:dd.find("p", class_="wTable__item r").text,
        h_temp:dd.find("p", class_="wTable__item t").text,
        h_wind:{
          w_di[dd.find("p", class_="wTable__item w").find("img")["src"].split("wind_")[1].split(".png")[0].split("_")[1]]:dd.find("p", class_="wTable__item w").find("img")["src"].split("wind_")[1].split(".png")[0].split("_")[0]+"m/s"
        }
      }
    }
print(data)
