import itchat
import led

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    led.openLed()
    print(msg.text)
    return msg.text

itchat.auto_login()
itchat.run()
