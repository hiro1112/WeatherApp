#!/usr/bin/env python3
import unittest
import weather
import rumps


class TestWeatherApp(unittest.TestCase):
    def setUp(self):
        self.weather = weather.WeatherApp("Weather App")
        self.area = {
                ('道北', '稚内'): '011000',
                ('道北', '旭川'): '012010',
                ('道北', '留萌'): '012020',
                ('千葉県', '千葉'): '120010',
                ('千葉県', '銚子'): '120020',
                ('千葉県', '館山'): '120030',
                ('東京都', '東京'): '130010',
                ('東京都', '大島'): '130020',
                ('東京都', '八丈島'): '130030',
                ('東京都', '父島'): '130040',
                ('神奈川県', '横浜'): '140010',
                ('神奈川県', '小田原'): '140020',
                ('沖縄県', '那覇'): '471010',
                ('沖縄県', '名護'): '471020',
                ('沖縄県', '久米島'): '471030',
                ('沖縄県', '南大東'): '472000',
                ('沖縄県', '宮古島'): '473000',
                ('沖縄県', '石垣島'): '474010',
                ('沖縄県', '与那国島'): '474020',
        }

    def test_build_area_submenu(self):
        self.weather._build_area_submenu()
        data = rumps.MenuItem("Area")
        for (pref, area), code in self.area.items():
            data[pref] = rumps.MenuItem(pref)
            data[pref][area] = rumps.MenuItem(area)
        self.assertEqual(self.weather.menu["Area"]["東京都"], data["東京都"])
        self.assertEqual(self.weather.menu["Area"]["東京都"]["東京"], data["東京都"]["東京"])
        self.assertEqual(self.weather.menu["Area"]["道北"], data["道北"])
        self.assertEqual(self.weather.menu["Area"]["道北"]["稚内"], data["道北"]["稚内"])
        self.assertEqual(self.weather.menu["Area"]["沖縄県"], data["沖縄県"])
        self.assertEqual(self.weather.menu["Area"]["沖縄県"]["与那国島"], data["沖縄県"]["与那国島"])
        self.assertEqual(self.weather.menu["Area"]["千葉県"], data["千葉県"])
        self.assertEqual(self.weather.menu["Area"]["千葉県"]["館山"], data["千葉県"]["館山"])
        self.assertEqual(self.weather.menu["Area"]["東京都"]["大島"], data["東京都"]["大島"])
        self.assertEqual(self.weather.menu["Area"]["東京都"]["東京"].code, self.area[("東京都", "東京")])
        self.assertEqual(self.weather.menu["Area"]["道北"]["稚内"].code, self.area[("道北", "稚内")])
        self.assertEqual(self.weather.menu["Area"]["沖縄県"]["与那国島"].code, self.area[("沖縄県", "与那国島")])
        self.assertEqual(self.weather.menu["Area"]["千葉県"]["館山"].code, self.area[("千葉県", "館山")])
        self.assertEqual(self.weather.menu["Area"]["東京都"]["大島"].code, self.area[("東京都", "大島")])

    def test_mark_default_area(self):
        self.assertTrue(self.weather.menu["Area"]["東京都"]["東京"].state)
        self.assertFalse(self.weather.menu["Area"]["道北"]["稚内"].state)
        self.assertFalse(self.weather.menu["Area"]["沖縄県"]["与那国島"].state)
        self.assertFalse(self.weather.menu["Area"]["千葉県"]["館山"].state)
        self.assertFalse(self.weather.menu["Area"]["東京都"]["大島"].state)

    def test_change_title_text(self):
        self.assertFalse(self.weather.menu["No Title Text"].state)
        self.weather.change_title_text(self.weather.menu["No Title Text"])
        self.assertTrue(self.weather.menu["No Title Text"].state)
        self.weather.change_title_text(self.weather.menu["No Title Text"])
        self.assertFalse(self.weather.menu["No Title Text"].state)
