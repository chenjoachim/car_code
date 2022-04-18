from remote import Scoreboard

# 連線，第三個參數不給的話預設是http://192.168.50.163:3000
# 請幫我改連到http://140.112.175.15:3000
# 第一個參數是為了配合sample code，理論上不會用到
myScoreboard = Scoreboard('','202204181306',"http://140.112.175.15:3000")

# 傳UID
# myScoreboard.add_UID("ABCDEF01")   # example
# 大小寫都可以，記得補0
myScoreboard.add_UID("C5F875CF") # 記得補0

# 拿分數
# 方法1: 直接打開網址http://192.168.50.165:3000
# 方法2
print( myScoreboard.getCurrentScore() )