#!/usr/bin/env python3
import rumps
import requests
import xml.etree.ElementTree as et
from subprocess import check_output


# Livedoor weather api
URL = 'http://weather.livedoor.com/forecast/webservice/json/v1'

# Livedoor weather area xml
XML = "primary_area.xml"

# Network command
CMD = "/System/Library/PrivateFrameworks/Apple80211.framework/"\
      "Versions/Current/Resources/airport"

# Network command option
CMDOPT = "-I"

# tempfile
TEMP = "data.tmp"


class WeatherApp(rumps.App):
    def __init__(self, name):
        self.set_area()
        self.net_flag = 0
        super(WeatherApp, self).__init__(
            "",
            menu=[
                self._build_area_submenu(),
                "No Title Text",
                "Quit Weather App",
            ],
            quit_button=None,
        )
        self.load_setted()
        self.mark_default_area()
        self.payload = {'city': self.area[(self.setted)]}

    def _build_area_submenu(self):
        menu = rumps.MenuItem("Area")
        for (pref, area), code in self.area.items():
            def checkbox(sender):
                cd = sender.code
                for p in menu.values():
                    p.state = False
                    for a in p.values():
                        a.state = False
                sender.state = True
                for (p, a), c in self.area.items():
                    if cd == c:
                        menu[p].state = True
                        menu.title = "Area ({} {})".format(p, a)
                        self.setted = (p, a)
                self.payload = {'city': cd}
                self.show_logo()
            menu[pref] = rumps.MenuItem(pref)
            mi = rumps.MenuItem(area, callback=checkbox)
            mi.code = code
            menu[pref][area] = mi
        return menu

    def set_area(self):
        self.area = {}
        src = et.parse(XML).getroot()[0]
        root = src.find("{http://weather.livedoor.com/%5C/ns/rss/2.0}source")
        for c in root.findall("pref"):
            for cc in c.findall("city"):
                key = (c.attrib["title"], cc.attrib["title"])
                self.area[key] = cc.attrib["id"]

    def mark_default_area(self):
        for (pref, area), code in self.area.items():
            if code == self.area[(self.setted)]:
                self.menu["Area"][pref].state = True
                self.menu["Area"][pref][area].state = True
                self.menu["Area"].title = "Area ({} {})".format(pref, area)
                break

    @rumps.clicked("No Title Text")
    def change_title_text(self, sender):
        sender.state = not sender.state
        self.title = "Weather App" if self.title == "" else ""

    def load_setted(self):
        with open(TEMP, 'r', encoding='utf-8') as f:
            tmp = f.read().rstrip().split(",")
            self.title = tmp[0]
            self.setted = (tmp[1], tmp[2]) if len(tmp) == 3 else ()
        if self.title == "":
            self.menu["No Title Text"].state = True

    def save_setted(self):
        with open(TEMP, 'w', encoding='utf-8') as f:
            f.write(
                "{},{},{}".format(
                    self.title,
                    self.setted[0],
                    self.setted[1]
                )
            )

    @rumps.clicked('Quit Weather App')
    def quit(self, _):
        self.save_setted()
        rumps.quit_application()

    @rumps.timer(3600)
    def update(self, _):
        self.show_logo()

    def show_logo(self):
        data = requests.get(URL, params=self.payload).json()
        tenki = data['forecasts'][0]['telop']
        if tenki == "晴れ":
            self.icon = "icon/sunny.png"
        elif tenki == "曇り":
            self.icon = "icon/cloudy.png"
        elif tenki == "雨":
            self.icon = "icon/rainny.png"
        elif tenki == "暴風雨":
            self.icon = "icon/rainny.png"
        elif tenki == "雪":
            self.icon = "icon/snowy.png"
        elif tenki == "暴風雪":
            self.icon = "icon/snowy.png"
        elif tenki == "晴時々曇":
            self.icon = "icon/sunny_cloudy.png"
        elif tenki == "晴時々雨":
            self.icon = "icon/sunny_rainny.png"
        elif tenki == "晴時々雪":
            self.icon = "icon/sunny_snowy.png"
        elif tenki == "曇時々晴":
            self.icon = "icon/cloudy_sunny.png"
        elif tenki == "曇時々雨":
            self.icon = "icon/cloudy_rainny.png"
        elif tenki == "曇時々雪":
            self.icon = "icon/cloudy_snowy.png"
        elif tenki == "雨時々晴":
            self.icon = "icon/rainny_sunny.png"
        elif tenki == "雨時々曇":
            self.icon = "icon/rainny_cloudy.png"
        elif tenki == "雨時々雪":
            self.icon = "icon/rainny_snowy.png"
        elif tenki == "雪時々晴":
            self.icon = "icon/snowy_sunny.png"
        elif tenki == "雪時々曇":
            self.icon = "icon/snowy_cloudy.png"
        elif tenki == "雪時々雨":
            self.icon = "icon/snowy_sunny.png"
        elif tenki == "晴のち曇":
            self.icon = "icon/sunny_then_cloudy.png"
        elif tenki == "晴のち雨":
            self.icon = "icon/sunny_then_rainny.png"
        elif tenki == "晴のち雪":
            self.icon = "icon/sunny_then_snowy.png"
        elif tenki == "曇のち晴":
            self.icon = "icon/cloudy_then_sunny.png"
        elif tenki == "曇のち雨":
            self.icon = "icon/cloudy_then_rainny.png"
        elif tenki == "曇のち雪":
            self.icon = "icon/cloudy_then_snowy.png"
        elif tenki == "雨のち晴":
            self.icon = "icon/rainny_then_sunny.png"
        elif tenki == "雨のち曇":
            self.icon = "icon/rainny_then_cloudy.png"
        elif tenki == "雨のち雪":
            self.icon = "icon/rainny_then_snowy.png"
        elif tenki == "雪のち晴":
            self.icon = "icon/snowy_then_sunny.png"
        elif tenki == "雪のち曇":
            self.icon = "icon/snowy_then_cloudy.png"
        elif tenki == "雪のち雨":
            self.icon = "icon/snowy_then_rainny.png"

    @rumps.timer(2)
    def check_network(self, _):
        wifi = check_output([CMD, CMDOPT])
        result = wifi.decode().replace(" ", "").split("\n")
        if result[0] == "AirPort:Off" or result[4] == "state:init":
            self.icon = "icon/gray_cloudy_then_sunny.png"
            self.net_flag = 1
        elif result[4] == "state:running":
            if self.net_flag == 1:
                self.show_logo()
            self.net_flag = 0


if __name__ == "__main__":
    WeatherApp("Weather App").run()
