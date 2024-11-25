import traceback

from flask import Flask, render_template, request, make_response, jsonify
import dbQuery
import smtplib
from email.mime.text import MIMEText
from email.header import Header

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/components', methods=["GET", "POST"])
def components():
    response = dbQuery.listComponents()
    return render_template('component.html', response=response)


@app.route('/addComponent', methods=["GET", "POST"])
def addComponent():
    if (len(request.args) > 0):
        component_name = request.args.get('componentName')
        component_contact = request.args.get('componentContact')
        component_manufacturer = request.args.get('componentManufacturer')
        fail_rate = request.args.get('fail_rate')
        dbQuery.addComponents(component_name, component_contact, component_manufacturer, fail_rate)
        response = dbQuery.listComponents()
        return render_template('component.html', response=response)
    else:
        return render_template('addComponent.html')


@app.route('/removeComponent', methods=["GET", "POST"])
def removeComponent():
    component_id = request.args.get('id')
    msg = dbQuery.removeComponent(component_id)
    new_response = dbQuery.listComponents()
    return make_response(jsonify(component_id, 200))


@app.route('/updateComponent', methods=["GET", "POST"])
def updateComponent():
    if (len(request.args) > 0):
        component_id = request.args.get('componentID')
        component_name = request.args.get('componentName')
        component_contact = request.args.get('componentContact')
        component_manufacturer = request.args.get('componentManufacturer')
        fail_rate = request.args.get('fail_rate')
        dbQuery.updateComponent(component_id, component_name, component_contact, component_manufacturer, fail_rate)
        response = dbQuery.listComponents()
        return render_template('component.html', response=response)
    else:
        return render_template('updateComponent.html')


@app.route('/failmodes')
def failmodes():
    response = dbQuery.listFalmodes()
    return render_template('failmode.html', response=response)


@app.route('/addFailmode', methods=["GET", "POST"])
def addFailmode():
    if (len(request.args) > 0):
        failmode_name = request.args.get('failModeName')
        failmode_des = request.args.get('failModeDes')
        dbQuery.addFailMode(failmode_name, failmode_des)
        response = dbQuery.listFalmodes()
        return render_template('failmode.html', response=response)
    else:
        return render_template('addFailMode.html')

@app.route('/removeFailmode', methods=["GET", "POST"])
def removeFailmode():
    fm_id = request.args.get('id')
    msg = dbQuery.removeFailMode(fm_id)
    new_response = dbQuery.listFalmodes()
    return make_response(jsonify(fm_id, 200))


@app.route('/updateFailMode', methods=["GET", "POST"])
def updateFailMode():
    if (len(request.args) > 0):
        fm_id = request.args.get('failModeId')
        failmode_name = request.args.get('failModeName')
        failmode_des = request.args.get('failModeDes')
        dbQuery.updateFailMode(fm_id, failmode_name, failmode_des)
        response = dbQuery.listFalmodes()
        return render_template('failmode.html', response=response)
    else:
        return render_template('updateFailMode.html')


@app.route('/mappings')
def mappings():
    mp_response = dbQuery.listMappings()
    return render_template('mapping.html',
                           response=mp_response)

@app.route('/addMapping', methods=["GET", "POST"])
def addMapping():
    if (len(request.args) > 0):
        fail_code = request.args.get('failCode')
        component = request.args.get('component')
        fail_mode = request.args.get('failMode')
        dbQuery.addMapping(fail_code, component, fail_mode)
        response = dbQuery.listMappings()
        return render_template('mapping.html', response=response)
    else:
        mp_response = dbQuery.listMappings()
        fm_response = dbQuery.listFalmodes()
        co_response = dbQuery.listComponents()
        return render_template('addMapping.html', response={
            mappings: mp_response,
            components: co_response,
            failmodes: fm_response
        }, components=co_response, failmodes=fm_response)

@app.route('/removeMapping', methods=["GET", "POST"])
def removeMapping():
    mapping_id = request.args.get('id')
    msg = dbQuery.removeMapping(mapping_id)
    return make_response(jsonify(mapping_id, 200))


@app.route('/updateMapping', methods=["GET", "POST"])
def updateMapping():
    if (len(request.args) > 0):
        mapping_id = request.args.get('id')
        fail_code = request.args.get('failCode')
        component = request.args.get('component')
        fail_mode = request.args.get('failMode')
        dbQuery.updateMapping(mapping_id, fail_code, component, fail_mode)
        response = dbQuery.listMappings()
        return render_template('mapping.html', response=response)
    else:
        mp_response = dbQuery.listMappings()
        fm_response = dbQuery.listFalmodes()
        co_response = dbQuery.listComponents()
        return render_template('updateMapping.html', response={
            mappings: mp_response,
            components: co_response,
            failmodes: fm_response
        }, components=co_response, failmodes=fm_response)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/topFail')
def badComponent():
    db_response = dbQuery.bad_components()
    return render_template('top5_fail.html',
                           rows=db_response)


@app.route('/mostUsed')
def mostUsed():
    mu_response = dbQuery.mostUsed()
    return render_template('mostUsed.html',
                           rows=mu_response)


@app.route('/pfr')
def PFR():
    pfr_response = dbQuery.pfr()
    return render_template('pfr.html',
                           rows=pfr_response)


@app.route('/advice')
def ad():
    ad_response = dbQuery.ad()
    return render_template('ad.html',
                           rows=ad_response)


class SendEmail():
    def email(self,tracebac,exception=''):
        email_response = dbQuery.email()
        emailhost = "smtp.126.com"  # 服务器地址
        emailuser = "l15921958758zy@126.com"  # 用户名
        emailpass = "l231488z"  # 密码(如果126开了授权登录，则使用授权的密码)
        sender = 'l15921958758zy@126.com'  #发件邮箱跟与emailuser一致即可
        receivers = email_response  # 接收邮件邮箱   ,'wuweipeng@yunfustore.com'
        message = MIMEText(tracebac, 'plain', 'utf-8')  #设置正文为符合邮件格式的HTML内容 tracebac就是系统抛出来的堆栈异常信息
        message['From'] = 'l15921958758zy@126.com' # 必须与mail_user一致     Header("测试", 'utf-8')
        message['To'] = 'email_response' # 必须与receivers一致    Header("测试", 'utf-8')

        message['Subject'] = Header('Product Report', 'utf-8')  #设置邮件标题
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(emailhost, 25)  # 25 为 SMTP 端口号 pop3端口为
            smtpObj.login(emailuser, emailpass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            #logs.Logs().logs(tracebac,exception)
            #print("邮件发送成功")
        except smtplib.SMTPException as e:
            print('email not send')


@app.route('/email')
def email():
    mail_msg = 'Product Report\nAdvice to users: http://127.0.0.1:5000/advice'
    SendEmail.email(SendEmail, mail_msg)
    return render_template('email.html',
                           response='successfully sent')


if __name__ == '__main__':
    app.run()
