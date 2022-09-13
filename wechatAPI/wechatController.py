#coding:utf-8
'''
function:
  公众号消息回复 
authon:
  luoaoxue(906464981@qq.com)
refer:
  微信接口介绍：
https://blog.csdn.net/MAO_TOU/article/details/98480894
  tornado框架介绍
https://blog.csdn.net/xc_zhou/article/details/80637714
'''


import tornado.web
import tornado.ioloop

import hashlib
import xmltodict
import time


WECHAT_TOKEN = 'luoaoxue'
#class WechatControlHandler(WebBaseHandler):
class WechatControlHandler(tornado.web.RequestHandler):
    def get(self):
        nonce = self.get_argument("nonce")
        echostr = self.get_argument("echostr")
        signature = self.get_argument("signature")
        timestamp = self.get_argument("timestamp")
        # 校验参数是否有空值
        if not all([signature, timestamp, nonce, echostr]):
            return self.render("error.html", error_msg="参数校验失败!")
        # 按照文档提供的方式进行计算签名值,进行比对
        sign_list = [WECHAT_TOKEN, timestamp, nonce]
        sign_list.sort()
        # 拼接字符串
        sign_temp_str = "".join(sign_list)
        # sha1加密,获取签名值
        sign_str = hashlib.sha1(sign_temp_str).hexdigest()
        # 验证请求是否来自微信服务器,比较自己生成的签名与微信签名,若相同则表示请求来自微信服务器
        if signature == sign_str:
            # 微信要求校验成功返回之前发送过来的echostr,原样返回即可, 接入成功
            return self.write(echostr)
        else:
            # 校验失败
            return self.render("error.html", error_msg="错误请求!")
    def post(self):
        # 验证请求是否来自微信服务器
        nonce = self.get_argument("nonce")
        signature = self.get_argument("signature")
        timestamp = self.get_argument("timestamp")
        sign_list = [WECHAT_TOKEN, timestamp, nonce]
        sign_list.sort()
        sign_temp_str = "".join(sign_list)
        sign_str = hashlib.sha1(sign_temp_str.encode('utf-8')).hexdigest()
        if signature == sign_str:
            # 请求来自微信服务器, 获取消息, 根据微信公众平台提示, 微信用户发送消息到公众号之后, 不管该消息
            # 是否是我们需要处理的, 都要在5秒内进行处理并回复, 否则微信将会给用户发送错误提示, 并且重新进行
            # 校验上述服务器URL是否可用, 所以对于我们不需要处理的消息, 可以直接回复 "success"(微信推荐) 或者 "", 
            # 这样微信服务器将不会发送错误提示到微信, 也不会去重新校验服务器URL
            
            msg_xml_str = self.request.body
            if not msg_xml_str:
                return self.write("success")
            # 解析消息
            msg_xml_dict_all = xmltodict.parse(msg_xml_str)
            msg_xml_dict = msg_xml_dict_all["xml"]
            # 获取消息类型, 消息内容等信息
            msg_type = msg_xml_dict["MsgType"]
            user_open_id = msg_xml_dict["FromUserName"]
            # 需要回复的信息
            response_dict = {
                "xml": {
                    "ToUserName": msg_xml_dict["FromUserName"],
                    "FromUserName": msg_xml_dict["ToUserName"],
                    "CreateTime": int(time.time()),
                    "MsgType": "text",
                }
            }
            # 当msg_type消息类型的值为event时, 表示该消息类型为推送消息, 例如微信用户 关注公众号(subscribe),取消关注(unsubscribe)
            if msg_type == "event":
                # 事件推送消息
                msg_event = msg_xml_dict["Event"]
                if msg_event == "subscribe":
                    # 用户关注公众号, 回复感谢信息
                    response_dict["xml"]["Content"] = "罗今天休假不定期更新。读书分享，故事分享，电影分享也或者不可避免的互联网相关分享吧。我很渺小，其实希望更多的听这个世界的声音。现在坐标深圳，希望你们有享可以分我点!"
                    response_xml_str = xmltodict.unparse(response_dict)
                    return self.write(response_xml_str)
            elif msg_type == "text":
                # 文本消息, 获取消息内容, 用户发送 哈哈, 回复 呵
                '''
                1. 用户发送含有可转债字样，返回近期日历提醒
                2. aoxueluoluo 发送 可转债分析＋可转债名称＋链接，则插入数据到数据库（aoxueluoluo为管理员账户）
                '''
                msg_body = msg_xml_dict["Content"]
                print(msg_body)
                if msg_body == "哈哈":
                    response_dict["xml"]["Content"] = "呵呵"
                    response_xml_str = xmltodict.unparse(response_dict)
                    return self.write(response_xml_str)
                if  "可转债" in msg_body:
                    response_content="-----今明两天可转债操作提醒------\n"
                    response_content += "今日申购：\n"
                    response_content += "今日其它：\n"
                    response_content += "明日申购：\n"
                    response_content += "明日其它：\n"
                    response_content += "     PS.输入转债名称，返回申购分析参考"
                    response_dict["xml"]["Content"] = response_content
                    response_xml_str = xmltodict.unparse(response_dict)
                    return self.write(response_xml_str)
            # 其他一律回复 success
            return self.write("我是罗罗呀，欢迎留言，回复肯定不及时，有问题邮件906464981@qq.com")


from tornado.web import Application,RequestHandler
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer

if __name__ == '__main__':
    #创建一个应用对象
    app = tornado.web.Application([(r'/api/wechat',WechatControlHandler)])
    http_server = HTTPServer(app)
    #最原始的方式
    http_server.bind(80)
    http_server.start(1)
    #启动ioloop轮询监听 
    IOLoop.current().start()
