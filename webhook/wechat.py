from flask import Flask, request
import requests
import datetime
import urllib.parse
from dateutil.parser import parse


SITE="xxxx.com"  # alertmanager 的url

app = Flask(__name__)

@app.route('/',methods=["GET","POST"])
def index():
    body = request.json
    print(body)
    send_webhook(body)
    return 'ok'


def parse_time(start,end=None):
    if end == "0001-01-01T00:00:00Z":
        return 0,0,0,0,""
    #ctime = datetime.datetime.strptime(end,"%Y-%m-%dT%H:%M:%S.%fZ") - datetime.datetime.strptime(start,"%Y-%m-%dT%H:%M:%S.%fZ")
    ctime = parse(end).replace(tzinfo=None) - parse(start).replace(tzinfo=None)
    days = ctime.days
    seconds = ctime.seconds % 3600 % 60
    minutes = int(ctime.seconds % 3600 / 60)
    hours = int(ctime.seconds / 3600)
    st = ""
    if days > 0:
        st += f"{days}天"
    if hours >0:
        st += f"{hours}时"
    if minutes >0:
        st += f"{minutes}分"
    st += f"{seconds}秒"
    return days,hours,minutes,seconds,st


info = '<font color="green">{}</font>'
error = '<font color="red">{}</font>'
comment = '<font color="comment">{}</font>'
warning = '<font color="warning">{}</font>'
bold = '**{}**'

def send_webhook(data):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxx'   # 企业微信webhook地址,这里更新
    content = ""

    if "msg" in data:
        pass
    else:
        groupStatus = data["status"]
        status = "🔥" if groupStatus.lower() == "firing" else "♻️"
        commonLabels = data.get("commonLabels",'')
        alerts = data.get('alerts')
        alertname = commonLabels.get("alertname",'')
        instance = commonLabels.get("instance",'')
        severity = commonLabels.get("severity",'')

        title = data.get('title','')
        if title:
            title = title.replace("FIRING","🔥").replace("RESOLVED", "♻️")
        else:
            title = f"{status} {len(alerts)}[{severity}] {alertname}\n"
        if data.get('status') == "firing":
            if severity.lower() == "criticle":
                msg_format = error
            else:
                msg_format = warning
            title = bold.format(title)
            content += msg_format.format(title)
        else:
            content += info.format(title)

    if "msg" in data:
        pass
    else:
        silenceURL = ""
        generatorURL = ""
        for item in data.get('alerts'):
            status = item.get('status')
            status = "🔥" if status == "firing" else "♻️"
            start = item.get('startsAt')
            end = item.get('endsAt')
            ctime = parse_time(start,end)[-1]

            silenceURL = item.get('silenceURL')
            if not silenceURL:
                sllist = []
                for k,v in item['labels'].items():
                    sllist.append(f'{k}="{v}"')
                sllist_str = ",".join(sllist)
                silenceURL = f"https://{SITE}/#/silences/new?filter=%s" % urllib.parse.quote("{"+sllist_str+"}")
           
            generatorURL = item.get('generatorURL')
            if not generatorURL and "panelURL" in item:
                generatorURL = item.get('panelURL')
       
            if end == "0001-01-01T00:00:00Z":
                if severity.lower() == "criticle":
                    msg_format = error
                else:
                    msg_format = warning
                content += f"- 🔥🆕 " + msg_format.format(item.get('annotations')["summary"])
                if "description" in item.get('annotations'):
                    content += "\n >" + item.get('annotations')["description"].replace('\\n','\n')
                    content  += f"  [👀]({generatorURL}) [💤]({silenceURL})"
                    content += '\n'
            else:
                summ = item.get('annotations')["summary"]+ f" 持续 {ctime} "
                if status == "♻️":
                    content +=  "- ♻️ <font color='green'>" + summ +"</font>"
                    content += '\n'

                else:
                    content =  "- 🔥 **<font color='red'>" + csumm+"</font>"
                    if "description" in item.get('annotations'):
                        content += "\n >" + item.get('annotations')["description"].replace('\\n','\n')
                        content  += f"  [👀]({generatorURL}) [💤]({silenceURL})"
                        content += '\n'

    msg  = {"msgtype": "markdown","markdown": {"content": content}}
    print(msg)
    resp = requests.post(url, json=msg)
    print(resp.status_code)
    print(resp.json())

if __name__ == "__main__":
    print('running......')
    app.run(host="0.0.0.0", port="3001")