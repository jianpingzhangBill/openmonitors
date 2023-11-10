from flask import Flask, request
import requests
import datetime
import urllib.parse
from dateutil.parser import parse

SITE = "xxx.com"  # 更新这里为你alertmanager的地址.
app = Flask(__name__) 

@app.route('/',methods=["GET","POST"])
def index():
    body = request.json
    send_webhook(body)
    return 'ok'


def parse_time(start,end=None):
    if end == "0001-01-01T00:00:00Z":
        return 0,0,0,0,""
#    ctime = datetime.datetime.strptime(end,"%Y-%m-%dT%H:%M:%S.%fZ") - datetime.datetime.strptime(start,"%Y-%m-%dT%H:%M:%S.%fZ")
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


def send_webhook(data):
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxx"   # 更新这里飞书的webhook url
    if "msg" in data:
        title = data.get('msg')
        template = "orange" if data.get('action') == "stop" else "green"

    else:
        groupStatus = data["status"]
        status = "🔥" if groupStatus.lower() == "firing" else "♻️"
        commonLabels = data.get("commonLabels")
        alerts = data.get('alerts')
        alertname = commonLabels.get("alertname")
        instance = commonLabels.get("instance")
        severity = commonLabels.get("severity")
        title = data.get('title')
        if title:
            title = title.replace("FIRING","🔥").replace("RESOLVED", "♻️")
        else:
            title = f"{status}{len(alerts)}[{severity}] {alertname}"
        if data.get('status') == "firing":
            template = "red"
            if severity.lower() == "warning":
                template = "orange"
        else:
            template = "green"

    elements = []
    msg = {"msg_type": "interactive","card": {"elements": elements, "header": { "title": {"content":title,"tag": "plain_text"}, "template": template}}}

    if "msg" in data:
        text = {"tag": "markdown","content": data.get("content",data.get("msg"))}
        elements.append(text)
    else:
        silenceURL = ""
        generatorURL = ""
        for item in data.get('alerts')[0:5]:
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
                silenceURL = f"http://{SITE}:9093/#/silences/new?filter=%s" % urllib.parse.quote("{"+sllist_str+"}")

            generatorURL = item.get('generatorURL')
            if end == "0001-01-01T00:00:00Z":
                content = f"🔥🆕 <font color='red'>" + item.get('annotations')["summary"] +"</font>"
                if "description" in item.get('annotations'):
                    content += "\n " + item.get('annotations')["description"].replace('\\n','\n')
                    content  += f"  [👀]({generatorURL}) [💤]({silenceURL})"
            else:
                content = item.get('annotations')["summary"]+ f" 持续 {ctime} "
                if status == "♻️":
                    content =  "♻️ <font color='green'>" + content +"</font>"

                else:
                    content =  "🔥 **<font color='red'>" + content +"</font>"
                    if "description" in item.get('annotations'):
                        content += "\n " + item.get('annotations')["description"].replace('\\n','\n')
                        content  += f"  [👀]({generatorURL}) [💤]({silenceURL})"
            # content += "- *Labels: *"
            # for l in item.get('labels',dict()).keys():

            #     if l in ("job", "instance", "severity", "hostname", "stack","service"):
            #         content += "{}: {}, ".format(l, item["labels"][l])

            text = {"tag": "markdown","content": content}

            elements.append(text)
    resp = requests.post(url, json=msg)
    print(resp.status_code)
    print(resp.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="3001")