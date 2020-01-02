# -*- coding: utf-8 -*-
import json
import requests
from colorama import init, Fore
from prettytable import PrettyTable
from train.src.stationinfo import chezhan_code, chezhan_names

init(autoreset=False)


class Colored(object):
    def yeah(self, s):
        return Fore.LIGHTCYAN_EX + s + Fore.RESET

    def green(self, s):
        return Fore.LIGHTGREEN_EX + s + Fore.RESET

    def yellow(self, s):
        return Fore.LIGHTYELLOW_EX + s + Fore.RESET

    def white(self, s):
        return Fore.LIGHTWHITE_EX + s + Fore.RESET

    def blue(self, s):
        return Fore.LIGHTBLUE_EX + s + Fore.RESET


def showTicket(html):
    html = json.loads(
        """{"httpstatus":200,"data":{"result":["jIbxyApurE35k79nblgVqGI58pVuqpbYrUQE3beseaRtj6bWy0fZRM5XTapIx741bZC7lL6HVMw%2F%0A1658ba3dxP%2Fh3wKV6rsYLJ%2FKq0ZrnL5OlUGsD7n6oQkIXG6iPWfDCsdQyuQPbWWTFzl2GAB3EaVn%0ASAUjZgbzgbRcNOxF2%2FRugHAzZO4TyIqUb1D%2FEjqyD9FbJRh9ftzkjAi7JsYXgXnaCTR%2Fl4mtYtNU%0AGEtfWbuJrPO7yyFOvCKmhFR4LFO%2BxFz4ROlQ7W%2FmZBaeuRykibvGrP3q6e1wOXh0aZHYnVTHHXnw%0ACN8QFg%3D%3D|预订|55000K218609|K2186|SHH|XNO|SHH|KFF|11:03|00:10|13:07|Y|%2Fh3fVnO9%2FYZ1DDSNV6GG35be1jEEYYa6MFK6AixawbqjvC5q06bi3FOpy9k%3D|20191226|3|H6|01|19|0|0||||14|||有||有|有|||||10401030|1413|1|0||||||||","3Gf%2BDwKHGXwnPZcvxHlSeLp1vN2s3rj4n048o1FFaUMUOEte%2FGmnA8o7Lf7nbrwgWVcvjErPc9cq%0AwLUoBwYI2CpAa12xQ8cjvPzmSeYBqrEo5uysJCTMlvl%2BVGFWLIN%2BBrtRK8OOJESLe14Dzgm7dNgE%0AEb3lRnaHFHzBIQSLi5T0xCg896HMe%2BWiR4uiHY4eys2PbyXU3ZBk%2BdeFLCOk7lo8ezvfuHVLWNm6%0AcfTp%2B05NrZcRdf2iWFO5EQexMQWj0bV%2BEug%2BJv7mj5jj3BxHIo%2FYYA7QU%2FUEkY%2F1wN6PyfW18T1G%0A%2FJLE%2Bw%3D%3D|预订|550000K23430|K234|SHH|SJP|SHH|KFF|11:09|23:55|12:46|Y|R2s1tlHGUwioCv%2BonLZG3RhSyyUKT9EVRXr9ankSNuZPai2mBm78OvqEAGs%3D|20191226|3|HY|01|13|0|0||||13|||有||5|有|||||10401030|1413|1|0||||||||","JNdvKvYGF7ZFH8ayxIyEV0%2BJWWQBxPzDRbaCH7Ei%2F2edv9kGXZZE4RKunEEOOur7es9hQMPEzeYn%0AoouJd8CRUtdCvybUSN2sXT0p2ZO70qp3zXCVyrs191ACbjoUD20aUFI3YPvtYGV4wXisTKAABcMb%0AAt6%2FPUfxdaZDjMtxss8WRMTTgWjAd6j%2FpP9gmSUhAq8TYx1Ybe%2BSU%2B2eIFO4%2BbiIrZ3Jgej4kRfY%0AiGw8r8MioWuQ%2FYmmPzCXEO%2BNFO%2B7JDbAoNl5A1HzPfjHQOzvbXjGVQa3%2BEkLWgP9y7xVVUsS5ZyB%0ADpzC1Q%3D%3D|预订|5l000G192430|G1924|AOH|EAY|AOH|KBF|11:40|16:20|04:40|Y|pLneRbMf%2FOW5Bs9Ezmxk5vI8mtDVp18Pew6o7DkDXbrlZ%2Fss|20191226|3|H6|01|11|1|0|||||||||||无|1|无||O0M090|OM9|0|1||||||||","pver7QnKq3Wf5IpH28n%2FYtE3zc7Uay2C5H%2BoVdTDwAV9GRSjjVfmi%2BWmJImOkv9O3OMhMc9b%2BcAK%0Amyrb2gpAx%2FBJ%2FrR6HIkeMq2vVW%2FC2ti6IBM7u%2F393QP%2BCrIv5XKaiU9R2cD6MNTx5vXpB62go1a4%0AEuZrPUOJdPi9Z%2F8pX1FMIwG1izpLxXwkcFB6RPJWCNFprpNE8x9jQ7HgTL4SbrydSPW4DuVslpOC%0ApvaLH0M5KHFTSYi%2BsoqGkZipIr2aNglHfHELcdMZUrFsM%2F97LNUJckdIM5jr4AVr3c8DmX9MooD7%0AVjq4vw%3D%3D|预订|550000T20470|T204|SHH|YMR|SHH|KFF|12:04|22:28|10:24|Y|W37hlyUgp3a6ZRwMisXE02LkzYQFEV5SoFgVY%2FvRX3Cbkk0bmfS6KoFd4Po%3D|20191226|3|H2|01|14|0|0||||无|||有||无|无|||||10401030|1413|0|1||||||||","bp%2FBqFDC861ug8iNpt36K%2BK4S6gpU2HjYjdye7rbBa8YKziABxfLT6sovm3t4Bg9G1tGzuK7BOkq%0AtqdR80r7RPboX6uFs79viEBNg91F6aC%2FqKhJZg%2FsXf8ldMlNhKLeloNtLu%2FSrQPddhrnr%2FUVYqAG%0At2BIt4vcR%2F1BnbySrEM%2Bx8hUWh%2Fte2IS5G5MojjCW0izt6S8o5JJncY3dwNdYd%2Bri%2FTkKdNIH7iS%0A1dW5kRiU6xXYRjRyl7iMsN%2BpaD%2BBI7YdcCXbr9sgGJcX2aYPT6QUl8zORb3wbNO9NYqyxxPY%2FxyR%0AFVaw1A%3D%3D|预订|55000K110251|K1102|SHH|AYF|SHH|KFF|13:44|02:05|12:21|Y|eg0CBxkUEOGf1bg9mbGJ0ZPLmjNMGYL5Wn6%2BnRvGV4IDXrzp1pJR%2BYHhW%2F0%3D|20191226|3|H2|01|14|0|0||||3|||有||无|有|||||10401030|1413|0|1||||||||","11ZXU5noh3S84yBp2JLSSqmh%2BDK%2FKOR0gRw30zJ0R4qOAGNWlvGBk5U5WbU%2FwGaVccAnWKjTOb2R%0AV4GVyAiguHn6QlU6je9huypOIVjXR3cnffkHeQ68tolIgpL18UIB2NAykAIr%2FncGAYkWGOEualUu%0Ar0USogU35IQ4fwF09cv7g46ArwhEG7Tl0zue8iidyU58bJ0VUJxVVSZEQAkO7dM8MvDJ86MaD2En%0AAzdZVnAlfNRkClrEe3rp4dRPrnGvF505hdIGxyQpTZJ7poZgdV2%2FWgbeYb0qFhArKzJlii9tbejs%0AsLG8ag%3D%3D|预订|550000K73802|K738|SHH|LYF|SHH|KFF|14:04|03:39|13:35|Y|FfKrYbJQPUUWj5NFanPtm76th6vKbdAQOUBdUk7rDWlc78hCL5hMp3fJUHg%3D|20191226|3|H3|01|14|0|0||||有|||有||有|有|||||10401030|1413|1|0||||||||","HrdR%2BbOs4qww0pdOJYmaIV3miyUMfpEwkcx%2F%2BkykFUBE%2FamwWmJKuEnkbM3wYFPVTSiMLBauParJ%0A628i18W7ohRbseRrAvx21Nb60%2BJGzfLbO6u3YoQyb2deAUqK7tYS8yMgEqI18tlXUbvOVNCKXhPE%0A%2BaCDNGZ3V70vcN9u4UxpRSSwxmb%2BzkqxSCsyOculbtQwIZf0VhdN1jTbhjzEJwpszXWiEiv2iicx%0AqfG5xPu5AUc%2FDz9%2BeMo%2FlTrWgJ%2Fp26Y3hlQ5zrKZpNE%2Fik7LuaX1g9JfHRppTgcIhHG%2FAPo%2Fjuqa%0AQs8lNQ%3D%3D|预订|550000K56006|K560|SHH|YWY|SHH|KFF|14:48|03:15|12:27|Y|C03Y51YLHF40LlCaxEGfLp1MlFAZQzaDFGh9htuMuVcjgDbKu4EDo8m8G80%3D|20191226|3|H6|01|13|0|0||||7|||有||无|有|||||10401030|1413|1|1||||||||","Ee8Vfu%2F1Pd%2FLMeeeZ3c4yQ5sHKwj5ZsUvmDY%2FNbQrptvRhED0enZHuyZdZqyNj1YqaNEqkchkLtW%0AiQSFz%2B7t2Rxo6CFB065aOL7HN%2Fw7r%2F7xEDlrGDNsz50mQGWXfgx7eCGeH7113ypPzztZdAXcoE7%2F%0AtwbhuPTuP49B1NVgnDCJn7jAFo8Ord8cHqsYO2YNYoYH1wokWtaibGobIZNP24yuz2FvknKalEdg%0AeMMdGU2eag4FdPgtP4eg%2FTP2De5Wu7oqKx6jS4V1dMTzO%2FG7mBMJvtQQmQ8cKSLretUlZ%2BhaDJXV%0AxFyiyw%3D%3D|预订|550000Z25202|Z252|SHH|XAY|SHH|KFF|15:52|00:58|09:06|Y|%2FYYO6oQtoZrggByC4KVYA2LKahR0sPJqXUqVU1Onk%2B%2BeFgmS0L7tUkfwjOM%3D|20191226|3|H3|01|09|0|0||||4|||有||无|有|||||10401030|1413|1|1||||||||","gkHkSit43ZC8EvupUOd9qBWreiEdczlI%2Bz8JpgME5bUCl7f0I9YfZYsDShLMZH1sTm%2B849ynvIEc%0AI3DZZZsyW%2FycDgEcO3rd0iL6vmVLHkAQtXheI5WGWVTHCCUC3Zl%2B95qddadRgVyJabWSAtVskfXU%0AK7PvQ27LZxVWamclO%2BuO51CcM8fWljz5QOmLxDLQr5B%2BDespbkEKaRM%2BgvF4s%2Bz8OnX%2BSpkd5gxr%0AaxuL3WxK8R7hIPqey0%2FkdhLQwtLHLoNnzCNWB7sidwR7fN6UkgQZaxvfj%2Fhms4UXlrCiFdzZESDo%0ARQEZug%3D%3D|预订|5l000G193630|G1936|AOH|EAY|AOH|KBF|16:12|20:29|04:17|Y|1h1ADnsuNvUrfGNi3CbD%2BZjZgjn9MbDN8XpvwII439Fru3Xw|20191226|3|H6|01|08|1|0|||||||||||有|7|6||O0M090|OM9|0|0||||||||","OCM2HOtSRR9xVv6snhDasnfK4BIJjxEZ8b9pSvqoBYyIt3f24hylw%2FhSvGvLQakuVwgo3m4gEYUd%0A3MEi%2FlufEwjubsH4vsMlZF%2FAVnaEfxrEAz5DV38PCwcuVvEeGNmBQ68RicAk0XNy7pqcUR20xRAF%0AKFJJFl2IOBZeDE0JtZaWwliQ4dizEkM9IP37LVPnVUDfSIl%2Fh5ipXQUqMKJpcJPp8kPN768dirKh%0A2vnoOY9oUmH3bzeIL4bX4ixXu6Xo0FLyiGIPcikpm0yt31ezB38stDOla%2B7y2KBpVe9Mibw5hS%2Fc%0AeRhrPw%3D%3D|预订|5l000G281250|G2812|AOH|SJP|AOH|KBF|16:26|20:59|04:33|Y|4FOR%2F0XGhi31Lv3OhRs3hQZycrqhIC1fEd5oLgMI6lVe028L|20191226|3|H2|01|08|1|0|||||||||||有|6|5||O0M090|OM9|0|0||||||||","bk7AhRQjQ8VFN%2Fl9AzCwAgQyVdObYxE5jUrHbwPnrXybw0K%2BOCR%2F47UPFde2CKzHHGF6skMWDsv8%0Ad2gDpr3jFssO2DSoPnsGZA%2Bb5b48N9oylOaBzIbUb7C6%2BOCFWI3xp36CxxQrYwNZW7h5ptzbC0sn%0A30PsLfhIv1hDye2w7ErvynKcRXjFzlcgn%2Fc1hHD6wbwNMsDpOrNnMWbLNBHSfZ2v%2BPd41tzXA6zR%0Ajsxh5V3%2FtpseGFiO7%2BegX7OJKYmgekhY7w51q0A7Tv9SpeFqB03zSLUQyNQDMxvh5sGub%2Fyd69jS%0ACZtfag%3D%3D|预订|550000K15270|K152|SHH|ZZF|SHH|KFF|16:31|06:17|13:46|Y|z8pxmwr0ZSvOQfskuixXSSGcouNuBsjDRGdV8hNx20sC1QYNbDmlARttCWM%3D|20191226|3|H3|01|13|0|0||||无|||有||无|无|||||10401030|1413|0|1||||||||","0v6ASMLsS7ebZTGZfVIYZhuzdyVtYIQzuo05fWzb5GLxvDsQkv1NtHGx8y7prp8hC00DyVwVjsds%0A4TFGc1PPZDoicT%2FQyGV7uEHzrJ05hooSbMBM4McKwCTUHDbSh%2B0Sh0IvhL7aiRnbUCFaHpRoj%2FUU%0AtJhd%2BPrtsliLarP0y1Ti9EObcNqVuEJlm3B6nnWrXJS35Bsrd%2B3%2Bi3PX%2FBt%2FrhnPZ%2BZiMrdgCddy%0AcDKSOCz9y4JOLsL3tYm805JOnc2XKEJVZlbET4EDOWN6Frb%2B0wq0Cy7cnU%2FOSsoWqUyS4umqDDGQ%0AFzOfbw%3D%3D|预订|550000K282C0|K282|SHH|CDW|SHH|KFF|20:28|08:19|11:51|Y|nazJOO%2B1EVbAnn4HnDnbdhgSMwz%2BP762MiaUTuH%2FItescbQmJkkxBOocb0M%3D|20191226|3|H3|01|11|0|0||||无|||有||无|无|||||10401030|1413|0|1||||||||"],"flag":"1","map":{"SHH":"上海","KFF":"开封","AOH":"上海虹桥","KBF":"开封北"}},"messages":"","status":true}""")
    table = PrettyTable(
        ["  车次  ", "出发车站", "到达车站", "出发时间", "到达时间", " 历时 ", "商务座", " 一等座", "二等座", "高级软卧", "软卧", "动卧", "硬卧", "软座", "硬座",
         "无座", "其他", "备注"])
    for i in html['data']['result']:
        name = [
            "station_train_code",
            "from_station_name",
            "to_station_name",
            "start_time",
            "arrive_time",
            "lishi",
            "swz_num",
            "zy_num",
            "ze_num",
            "dw_num",
            "gr_num",
            "rw_num",
            "yw_num",
            "rz_num",
            "yz_num",
            "wz_num",
            "qt_num",
            "note_num"
        ]

        data = {
            "station_train_code": '',
            "from_station_name": '',
            "to_station_name": '',
            "start_time": '',
            "arrive_time": '',
            "lishi": '',
            "swz_num": '',
            "zy_num": '',
            "ze_num": '',
            "dw_num": '',
            "gr_num": '',
            "rw_num": '',
            "yw_num": '',
            "rz_num": '',
            "yz_num": '',
            "wz_num": '',
            "qt_num": '',
            "note_num": ''
        }
        # 将各项信息提取并赋值
        item = i.split('|')  # 使用“|”进行分割
        data["station_train_code"] = item[3]  # 获取车次信息，在3号位置
        data["from_station_name"] = item[6]  # 始发站信息在6号位置
        data["to_station_name"] = item[7]  # 终点站信息在7号位置
        data["start_time"] = item[8]  # 出发时间在8号位置
        data["arrive_time"] = item[9]  # 抵达时间在9号位置
        data["lishi"] = item[10]  # 经历时间在10号位置
        data["swz_num"] = item[32] or item[25]  # 特别注意，商务座在32或25位置
        data["zy_num"] = item[31]  # 一等座信息在31号位置
        data["ze_num"] = item[30]  # 二等座信息在30号位置
        data["gr_num"] = item[21]  # 高级软卧信息在21号位置
        data["rw_num"] = item[23]  # 软卧信息在23号位置
        data["dw_num"] = item[27]  # 动卧信息在27号位置
        data["yw_num"] = item[28]  # 硬卧信息在28号位置
        data["rz_num"] = item[24]  # 软座信息在24号位置
        data["yz_num"] = item[29]  # 硬座信息在29号位置
        data["wz_num"] = item[26]  # 无座信息在26号位置
        data["qt_num"] = item[22]  # 其他信息在22号位置
        data["note_num"] = item[1]  # 备注信息在1号位置

        color = Colored()
        data["note_num"] = color.white(item[1])
        # 如果没有信息，那么就用“-”代替
        for pos in name:
            if data[pos] == "":
                data[pos] = "-"

        tickets = []
        cont = []
        cont.append(data)
        for x in cont:
            tmp = []
            for y in name:
                if y == "from_station_name":
                    s = color.green(chezhan_names[data["from_station_name"]])
                    tmp.append(s)
                elif y == "to_station_name":
                    s = color.yeah(chezhan_names[data["to_station_name"]])
                    tmp.append(s)
                elif y == "start_time":
                    s = color.green(data["start_time"])
                    tmp.append(s)
                elif y == "arrive_time":
                    s = color.yeah(data["arrive_time"])
                    tmp.append(s)
                elif y == "station_train_code":
                    s = color.yellow(data["station_train_code"])
                    tmp.append(s)
                else:
                    tmp.append(data[y])
            tickets.append(tmp)
        for ticket in tickets:
            table.add_row(ticket)
    print(table)


def main():
    # date = input("请输入时间：\n")
    # from_station = chezhan_code[input("请输入起始站点：\n")]
    # to_station = chezhan_code[input("请输入目的站点：\n")]
    date = "2019-12-26"
    from_station = "上海"
    to_station = "开封"
    url = "https://kyfw.12306.cn/otn/leftTicket/queryZ?"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5702.400 QQBrowser/10.2.1893.400"
    }
    url = url + "leftTicketDTO.train_date=" + date + "&leftTicketDTO.from_station=" + from_station + "&leftTicketDTO.to_station=" + to_station + "&purpose_codes=ADULT"
    print(url)  # 已经检查过生成的URL是正确的
    # request请求获取主页
    r = requests.get(url, headers=headers)
    r.raise_for_status()  # 如果发送了一个错误的请求，会抛出异常
    r.encoding = r.apparent_encoding
    print(r.text)
    showTicket(r.text)


if __name__ == '__main__':
    main()
