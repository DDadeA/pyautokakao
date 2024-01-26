# pyautokakao
KakaoTalk automation tool for Windows

# Installation
```
pip install pyautokakao
```

# Usage
You should start kakaotalk before.
`Chat room name` should be exactly the same. (Unexpected behavior)
```python
import pyautokakao

# Read Chat
log = pyautokakao.read("Chat room name")
print(log)

# Send Chat
pyautokakao.send("Chat room name", "message")

# Add to friends
pyautokakao.add_friend("friend name(you determine)", "phone number")

# Invite friend to existing room
pyautokakao.invite("Chat room name", ["friend name 1","friend name 2",])

# Make new chat room
pyautokakao.make_room("Chat room name", ["friend name 1","friend name 2",])

```