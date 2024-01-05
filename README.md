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

# Usage

## Basic usage

- 在使用這個MITM腳本之前，你應該知道要如何透過類似Proxifier之類的工具，將麻魂的連線導向到mitmproxy。
- 如果你不知道該怎麼做，以下是簡短教學：
  - 下載並開啟Proxifier
  - 新增一個Proxy Server，IP: 127.0.0.1；PORT: 依你喜好
  - 新建一個Proxification Rule，選擇將Riichi City應用的連線導向到剛剛新建的Proxy Server

1. `git clone this`
2. `cd MajsoulUnlocker`
3. `python -m venv venv`
4. `venv\Scripts\activate.bat`
5. `pip install -r requirements.txt`
6. `mitmdump -s unlocker.py -p <PORT>`

# TODO
 - [ ] 確保傳送到Server端的資料沒有使用Unlocker的跡象
 - [ ] 還是有很多Bug

# Authors

* **Shinkuan** - [Shinkuan](https://github.com/shinkuan/)

# Thanks

感謝[Majsoul Mod Plus](https://github.com/Avenshy/majsoul_mod_plus)作者，提供了獲取物品ID十分方便的腳本。