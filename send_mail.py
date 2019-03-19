# coding = utf-8

import os
from django.core.mail import EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

if __name__ == "__main__":

    subject, from_email, to = '来自understandTA的测试邮件','korosue@sina.com','2772354227@qq.com'
    text_content = '欢迎访问www.understandTA.com,这里是您宠物的乐园'
    html_content = '<p>欢迎访问<a href="http://127.0.0.1:8000/index" target=blank>www.understangta.com</a>,这里是您宠物的乐园,专注给您更好的服务体验~</p>'
    msg = EmailMultiAlternatives(subject,text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()