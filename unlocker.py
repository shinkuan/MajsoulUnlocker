import mitmproxy.addonmanager
import mitmproxy.http
import mitmproxy.log
import mitmproxy.tcp
import mitmproxy.websocket
from mitmproxy import ctx
from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster
from liqi import LiqiProto, MsgType
from rich.console import Console
import json
console = Console()

activated_flows = [] # store all flow.id ([-1] is the recently opened)
messages_dict = dict() # flow.id -> Queue[flow_msg]
unlock_avartar = False

class ClientWebSocket:

    def __init__(self):
        self.liqi: dict[str, LiqiProto]={}
        self.liqiModify: LiqiModify=LiqiModify(unlock_avartar=unlock_avartar)
        pass

    def websocket_start(self, flow: mitmproxy.http.HTTPFlow):
        assert isinstance(flow.websocket, mitmproxy.websocket.WebSocketData)
        global activated_flows,messages_dict
        
        activated_flows.append(flow.id)
        messages_dict[flow.id]=[]
        self.liqi[flow.id] = LiqiProto()

    def websocket_message(self, flow: mitmproxy.http.HTTPFlow):
        assert isinstance(flow.websocket, mitmproxy.websocket.WebSocketData)
        global activated_flows,messages_dict
        if flow.websocket.messages[-1].injected:
            # This message is injected by us, ignore it
            console.print("Injected!", style="bold red")
            return
        original_proto_msg = flow.websocket.messages[-1].content
        messages_dict[flow.id].append(original_proto_msg)
        original_liqi_msg = self.liqi[flow.id].parse(original_proto_msg)
        action, modified_liqi_msg = self.liqiModify.modify(original_liqi_msg)
        # Three kinds of action: drop, modify, fake_response | None
        if action == 'drop':
            console.print("Dropping Message!", style="bold red")
            console.log(original_liqi_msg)
            flow.websocket.messages[-1].drop()
        elif action == 'modify':
            modified_proto_msg = self.liqi[flow.id].compose(modified_liqi_msg, msg_id=original_liqi_msg['id'])
            flow.websocket.messages[-1].drop()
            # Refer to mitmproxy/addons/proxyserver.py:inject_websocket
            ctx.master.commands.call(
                "inject.websocket", flow, not flow.websocket.messages[-1].from_client, modified_proto_msg, False
            )
            console.log(original_liqi_msg)
        elif action == 'fake_response':
            console.print("Faking Server Response!", style="bold red")
            console.print(f"Target: {modified_liqi_msg['method']}", style="bold red")
            fake_response = modified_liqi_msg['fake_response']
            modified_liqi_msg.pop('fake_response')
            console.log(modified_liqi_msg)
            
            flow.websocket.messages[-1].drop()
            fake_proto_msg = self.liqi[flow.id].compose(fake_response, msg_id=fake_response['id'])
            ctx.master.commands.call(
                "inject.websocket", flow, True, fake_proto_msg, False
            )
            console.log(fake_response)
        else:
            console.log(original_liqi_msg)


    def websocket_end(self, flow: mitmproxy.http.HTTPFlow):
        global activated_flows,messages_dict
        activated_flows.remove(flow.id)
        messages_dict.pop(flow.id)


async def start_proxy(host, port):
    opts = options.Options(listen_host=host, listen_port=port)

    master = DumpMaster(
        opts,
        with_termlog=False,
        with_dumper=False,
    )
    master.addons.add(ClientWebSocket())
    
    await master.run()
    return master


class LiqiModify:
    def __init__(self, unlock_avartar: bool = False):
        self.unlock_avartar = True
        self.accountId = -1
        self.current_character = -1
        self.current_skin = -1
        with open('./settings.json', 'r', encoding='utf-8') as f:
            settings = json.load(f)
            self.current_character = settings['main_character']
        with open('./id/CharacterId.json', 'r', encoding='utf-8') as f:
            characterId = json.load(f)
            self.current_skin = characterId[str(self.current_character)]['init_skin']
        pass

    def modify(self, msg: dict):
        if msg is None:
            return None, None
        action = None
        modify_msg = msg
        if 'error' in msg['data']:
            if msg['data']['error']['code'] != 0:
                console.print("===Error==="*10, style="bold red")
                console.log(msg, style="bold red")
                console.print("===Error==="*10, style="bold red")
        if self.unlock_avartar:
            # Response from server, modify it
            if msg['type'] == MsgType.Res:
                if msg['method'] == '.lq.Lobby.login':
                    action = 'modify'
                    self.accountId = msg['data']['account']['accountId']
                    modify_msg['data']['account']['avatarId'] = self.current_skin
                    # modify_msg['data']['account']['level'] = {'id': 10720, 'score': 0}
                    # modify_msg['data']['account']['level3'] = {'id': 20720, 'score': 0}
                if msg['method'] == '.lq.Lobby.oauth2Login':
                    action = 'modify'
                    self.accountId = msg['data']['account']['accountId']
                    modify_msg['data']['account']['avatarId'] = self.current_skin
                    # modify_msg['data']['account']['level'] = {'id': 10720, 'score': 0}
                    # modify_msg['data']['account']['level3'] = {'id': 20720, 'score': 0}

                if msg['method'] == '.lq.Lobby.fetchInfo':
                    action = 'modify'
                    # Title
                    modify_msg['data']['titleList']['titleList'] = []
                    with open('./id/TitleId.json', 'r', encoding='utf-8') as f:
                        titleId = json.load(f)
                        for id in titleId:
                            modify_msg['data']['titleList']['titleList'].append(titleId[id]['id'])
                    # Items
                    modify_msg['data']['bagInfo']['bag']['items'] = []
                    with open('./id/ItemId.json', 'r', encoding='utf-8') as f:
                        itemId = json.load(f)
                        for id in itemId:
                            if itemId[id]['is_unique'] == 1:
                                modify_msg['data']['bagInfo']['bag']['items'].append({
                                    "itemId": itemId[id]['id'],
                                    "stack": 1
                                })
                            else:
                                modify_msg['data']['bagInfo']['bag']['items'].append({
                                    "itemId": itemId[id]['id'],
                                    "stack": 999
                                })
                    # Achievements
                    # for achievement in modify_msg['data']['achievement']['progresses']:
                    #     if achievement['achieved'] is False:
                    #         achievement['achieved'] = True
                    #         achievement['achievedTime'] = 1704067200
                    # Characters
                    modify_msg['data']['characterInfo']['characters'] = []
                    modify_msg['data']['characterInfo']['characterSort'] = []
                    with open('./id/CharacterId.json', 'r', encoding='utf-8') as f:
                        characterId = json.load(f)
                        for id in characterId:
                            modify_msg['data']['characterInfo']['characters'].append({
                                "charid": characterId[id]['id'],
                                "level": 5,
                                "exp": 0,
                                "skin": characterId[id]['init_skin'],
                                "views": [],
                                "isUpgraded": True,
                                "extraEmoji": [],
                                "rewardedLevel": []
                            })
                            modify_msg['data']['characterInfo']['characterSort'].append(characterId[id]['id'])
                    # Skins
                    modify_msg['data']['characterInfo']['skins'] = []
                    with open('./id/SkinId.json', 'r', encoding='utf-8') as f:
                        skinId = json.load(f)
                        for id in skinId:
                            if id in ['400000', '400001']:
                                continue
                            modify_msg['data']['characterInfo']['skins'].append(skinId[id]['id'])
                    modify_msg['data']['characterInfo']['mainCharacterId'] = self.current_character

                    # Views
                    with open('./settings.json', 'r', encoding='utf-8') as f:
                        settings = json.load(f)
                        modify_msg['data']['allCommonViews']['views'] = [{
                            'values': settings['views'],
                            "index": 0
                        }]
                        modify_msg['data']['allCommonViews']['use'] = 0
                if msg['method'] == '.lq.Lobby.createRoom':
                    action = 'modify'
                    for person in modify_msg['data']['room']['persons']:
                        if person['accountId'] == self.accountId:
                            person['avatarId'] = self.current_skin
                            person['character']['charid'] = self.current_character
                            person['character']['skin'] = self.current_skin
                            person['character']['level'] = 5
                            person['character']['exp'] = 0
                            person['character']['isUpgraded'] = True
                if msg['method'] == '.lq.Lobby.fetchAccountInfo':
                    action = 'modify'
                    if modify_msg['data']['account']['accountId'] == self.accountId:
                        modify_msg['data']['account']['avatarId'] = self.current_skin
                if msg['method'] == '.lq.FastTest.authGame':
                    action = 'modify'
                    for person in modify_msg['data']['players']:
                        if person['accountId'] == self.accountId:
                            person['avatarId'] = self.current_skin
                            person['character']['charid'] = self.current_character
                            person['character']['skin'] = self.current_skin
                            person['character']['level'] = 5
                            person['character']['exp'] = 0
                            person['character']['isUpgraded'] = True
                if msg['method'] == '.lq.Lobby.fetchRoom':
                    action = 'modify'
                    for person in modify_msg['data']['persons']:
                        if person['accountId'] == self.accountId:
                            person['avatarId'] = self.current_skin
                            person['character']['charid'] = self.current_character
                            person['character']['skin'] = self.current_skin
                            person['character']['level'] = 5
                            person['character']['exp'] = 0
                            person['character']['isUpgraded'] = True

            # Request from client, drop it or fake a response to avoid Majsoul found we cheat
            if msg['type'] == MsgType.Req:
                if msg['method'] == '.lq.Lobby.changeMainCharacter':
                    action = 'drop'
                    with open('./settings.json', 'r', encoding='utf-8') as f:
                        settings = json.load(f)
                        settings['main_character'] = msg['data']['characterId']
                    with open('./settings.json', 'w', encoding='utf-8') as f:
                        json.dump(settings, f, indent=4)
                    self.current_character = msg['data']['characterId']
                if msg['method'] == '.lq.Lobby.changeCharacterSkin':
                    action = 'drop'
                    with open('./id/CharacterId.json', 'r', encoding='utf-8') as f:
                        characterId = json.load(f)
                        characterId[str(msg['data']['characterId'])]['init_skin'] = msg['data']['skin']
                    with open('./id/CharacterId.json', 'w', encoding='utf-8') as f:
                        json.dump(characterId, f, indent=4)
                    self.current_skin = msg['data']['skin']
                if msg['method'] == '.lq.Lobby.saveCommonViews':
                    action = 'fake_response'
                    modify_msg['fake_response'] = {
                        'id': msg['id'],
                        'type': MsgType.Res,
                        'method': '.lq.Lobby.saveCommonViews',
                        'data': {}
                    }
                    with open('./settings.json', 'r', encoding='utf-8') as f:
                        settings = json.load(f)
                        settings['views'] = modify_msg['data']['views']
                    with open('./settings.json', 'w', encoding='utf-8') as f:
                        json.dump(settings, f, indent=4)
                if msg['method'] == '.lq.Lobby.openAllRewardItem':
                    action = 'drop'

            if msg['type'] == MsgType.Notify:
                if msg['method'] == '.lq.NotifyRoomPlayerUpdate':
                    action = 'modify'
                    for person in modify_msg['data']['updateList']:
                        if person['accountId'] == self.accountId:
                            person['avatarId'] = self.current_skin
                    for person in modify_msg['data']['playerList']:
                        if person['accountId'] == self.accountId:
                            person['avatarId'] = self.current_skin
                    
        return action, modify_msg

    def parse(self, msg: dict):
        pass


addons = [
    ClientWebSocket()
]


if __name__ == '__main__':
    import asyncio
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='127.0.0.1')
    parser.add_argument('--port', type=int, default=7878)
    parser.add_argument('--unlock_avartar', action='store_true')
    args = parser.parse_args()
    unlock_avartar = args.unlock_avartar
    # start proxy
    asyncio.run(start_proxy('127.0.0.1', 7878))
