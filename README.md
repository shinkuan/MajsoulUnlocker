<br/>
<p align="center">
  <h1 align="center">雀魂全解鎖</h3>

  <p align="center">
Majsoul Unlocker<br>
基於MITM攻擊來解鎖全腳色、造型、物品<br>
    <br/>
    <br/>
    <br/>
    <br/>
    <a href="https://github.com/shinkuan/MajsoulUnlocker/issues">Report Bug</a>
    .
    <a href="https://github.com/shinkuan/MajsoulUnlocker/issues">Request Feature</a>
  </p>
</p>

# About The Project

https://github.com/shinkuan/RandomStuff/assets/35415788/e5371e99-7c43-479f-adb6-c950dbac6a4d

## Changelog

### 2024/1/12

___

- 新增了v10支持，也就是說Steam、iOS版本現在可以正常使用了。
- 修正了更改稱號後沒有被存檔的bug

### 2024/1/7

___

- 增加了Passthrough模式，在該模式下MITM不會更動任何數據，測試腳本問題時可使用
- 稱號以及頭像框現在可以正常使用了

# Usage

## Basic usage

- 目前適配雀魂版本：v10.x ~ v0.11.x
- 適用平台：全平台，只要你懂得如何將雀魂的連線導向到mitmproxy。
- v10的記得要使用unlocker_v10.py
- ~~！注意！Steam版客戶端還停留在v0.10.x 無法使用。~~ 已更新

- 在使用這個MITM腳本之前，你應該知道要如何透過類似Proxifier之類的工具，將雀魂的連線導向到mitmproxy。
- 如果你不知道該怎麼做，以下是簡短教學：
  - 下載並開啟Proxifier
  - 新增一個Proxy Server，IP: 127.0.0.1；PORT: 依你喜好
  - 新建一個Proxification Rule，選擇將Majsoul的連線導向到剛剛新建的Proxy Server

1. `git clone this`
2. `cd MajsoulUnlocker`
3. `python -m venv venv`
4. `venv\Scripts\activate.bat`
5. `pip install -r requirements.txt`
6. `mitmdump -s unlocker.py -p <PORT>`

## 聲明

本腳本僅供學習參考交流，請使用者於下載24小時內自行刪除，不得用於商業用途，否則後果自負。

此插件僅供學習參考交流，請使用者於下載24小時內自行刪除，不得用於商業用途，否則後果自負。

此插件僅供學習參考交流，請使用者於下載24小時內自行刪除，不得用於商業用途，否則後果自負。

### 警告：

雀魂遊戲官方可能會偵測並封號！

如產生任何後果與作者無關！

使用本腳本則表示同意此條款！


# TODO
 - [ ] 確保傳送到Server端的資料沒有使用Unlocker的跡象 (應該沒有吧
 - [ ] 還是有很多Bug

# Authors

* **Shinkuan** - [Shinkuan](https://github.com/shinkuan/)

## Support me

留個星星就可以啦
有問題可到 [Discord](https://discord.gg/Z2wjXUK8bN) 找我

# See Also

## [Akagi](https://github.com/shinkuan/Akagi)
![image](https://github.com/shinkuan/RandomStuff/assets/35415788/4f9b2e2f-059e-44a8-b11a-5b2ce28cb520)

## [Riichi City Unlocker](https://github.com/shinkuan/RiichiCityUnlocker)

https://github.com/shinkuan/RandomStuff/assets/35415788/2b364ad2-08ee-49c5-b67e-fce1aa862088

# Thanks

感謝[Majsoul Mod Plus](https://github.com/Avenshy/majsoul_mod_plus)作者，提供了獲取物品ID十分方便的腳本。

感謝[MahjongRepository/mahjong_soul_api](https://github.com/MahjongRepository/mahjong_soul_api)提供了讀取雀魂數據的方式。
