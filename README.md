# WeatherApp
Livedoor APIを用いたMacメニューバー 常駐天気アプリ

Weather resident app for Mac menu bar using Livedoor API  

# Demo
<img src="https://user-images.githubusercontent.com/17289239/81445327-9bf63980-91b3-11ea-82f1-50a3c25fb3aa.gif" width="400px">

# Features
* Livedoorの気象データから現在の天気を天気アイコンで表示

  shows current weather icon with getting Livedoor weather data
* タイトルテキストのON,OFFを切り替える可能

  can switch title text on or off

# Dependencies
* python3
* rumps
* requests
* xml
* subprocess

# Create App
```bash
python3 setup.py py2app
```
