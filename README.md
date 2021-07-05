# Permission Bot
디스코드 내에 있는 [message-components](https://discord.com/developers/docs/interactions/message-components) 를 연구하기 위하여 제작된 봇입니다.
![Support_the_Companion_quickly_at_discord.py](https://user-images.githubusercontent.com/16767890/124504287-1e06e000-de02-11eb-9c07-1988b7182aec.gif)

### Setup
1. `/config/config_example.ini` 파일을 `/config/config.ini`으로 변환합니다.
config 파일의 기본 양식은 아래와 같습니다.
```editorconfig
[DEFAULT]
AutoShard = False
token = YOUR_DISCORD_BOT_TOKEN
prefix = !
```
2. Discord Developers 에서 발급 받은 디스코드 봇의 토큰을 `token`에 대입해줍니다.
3. python 을 통하여 `main.py`를 실행합니다.

### Structure
해당 봇의 주요 코드는 아래 3곳에 포함되어 있습니다.
* [cog.general](cogs/general.py): 명령어를 처리합니다.
* [cog.socket](cogs/socket.py): `Button` 혹은 `Selection`에 대한 상호작용이 발생했을 떄에 대한 코드가 작성되어 있습니다.
* [module.components](module/components.py): `Discord Components` 에 대한 주요 클래스가 작성되어 있습니다.
