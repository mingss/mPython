import requests as rq
import json
import socket
import sys
'''
http://1.255.153.177:9200/_cat/indices?v
http://1.255.153.177:9200/_cat/allocation?v

curl -u logadmin -X DELETE "localhost:9200/skb-infralog-2020.09.01?pretty"
curl -u "logadmin:!SKqmfhemqosem04%" -X DELETE "1.255.153.177:9200/skb-infralog-2020.11.0*?pretty"
curl -u logadmin -X POST "localhost:9200/_forcemerge?pretty"
'''


''' //11.12 17:05
금번부터 구성원 업무집중도를 고려하여, 매주 진행하던 우회접속 소명 절차를 격주로 변경하여 진행하오니 적극적인 회신 부탁드립니다.
12        541gb   594.3gb    388.9gb    983.3gb           60 1.255.153.177 1.255.153.177 SKB-INFRALOG-FRONT
    17      613.6gb     665gb    318.2gb    983.3gb           67 1.255.153.175 1.255.153.175 SKB-INFRALOG-DATA001
     7      776.9gb   828.1gb      156gb    984.1gb           84 1.255.153.202 1.255.153.202 SKB-INFRALOG-DATA003
    32      640.6gb   715.6gb    268.5gb    984.1gb           72 1.255.153.92  1.255.153.92  SKB-INFRALOG-DATA002

//11.12 14:00
shards disk.indices disk.used disk.avail disk.total disk.percent host          ip            node
     7       47.9gb    99.4gb    884.7gb    984.1gb           10 1.255.153.202 1.255.153.202 SKB-INFRALOG-DATA003
    13         49gb   102.5gb    880.7gb    983.3gb           10 1.255.153.177 1.255.153.177 SKB-INFRALOG-FRONT
    23      940.9mb      95gb      889gb    984.1gb            9 1.255.153.92  1.255.153.92  SKB-INFRALOG-DATA002
    12      474.9mb    51.1gb    932.1gb    983.3gb            5 1.255.153.175 1.255.153.175 SKB-INFRALOG-DATA001
     9                                                                                       UNASSIGNED
index=nw_server_syslog "remote.automated_access"=NON_AUTOMATED_ACCESS NOT (team=unidentified OR team=보안기술CoE OR team=보안기획CoE)

shards disk.indices disk.used disk.avail disk.total disk.percent host          ip            node
    11      101.1gb   152.6gb    831.5gb    984.1gb           15 1.255.153.202 1.255.153.202 SKB-INFRALOG-DATA003
    15       94.1gb   147.7gb    835.5gb    983.3gb           15 1.255.153.177 1.255.153.177 SKB-INFRALOG-FRONT
    19      488.8mb    82.4gb    901.7gb    984.1gb            8 1.255.153.92  1.255.153.92  SKB-INFRALOG-DATA002
    15      497.9mb    51.2gb    932.1gb    983.3gb            5 1.255.153.175 1.255.153.175 SKB-INFRALOG-DATA001
     6                                                                                       UNASSIGNE

'''


searchlist = [ #0 - ipn, 1 - L2L3
    {},
] #searchlist[0]: IPN, searchlist[1]: L2L3
# splunk 검색 쿼리 내 ("Accepted" OR "login on") 를 추가하여 현재 ELK에서 보고 있는 데이터에 대해서만 추출하는 형태로 변경
# 향후 확장을 위해서는 splunk쪽에 기 수집되고 있는 항목을 활용하는 것이 합당.
auths = [
    ()
]



def url_call(http_method, url, params, site_auth):
    if http_method == "POST":
        res = rq.post(url, data=params, verify=False, auth=site_auth)
    elif http_method == "GET":
        res = rq.get(url, params=params, verify=False, auth=site_auth)
    else:
        res = rq.get(url, params=params, verify=False, auth=site_auth)
    return res

def logstash_call(call_type):
    urls = [
        'http://1.255.153.177:9200/_cat/indices?pretty&v&s=index',
        'http://1.255.153.177:9200/_cat/allocation?pretty&v',
    ]
    if call_type == "indices":
        return url_call("GET", urls[0], None, auths[1])
    elif call_type == "allocation":
        return url_call("GET", urls[1], None, auths[1])
    else:
        exit(0)

def adams_call(url, mode): #GET method는 data가 아닌 params 사용
    return url_call("GET", url, searchlist[mode], auths[0])

def adams_restapi_processing():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        sys.stderr.write("[ERROR] %s\n" % msg[1])
        sys.exit(1)

    dHOST = "127.0.0.1"
    #dHOST = "syslog.skbroadband.com"
    dPORT = 1515
    durl = 'http://1.255.90.51:8089/servicesNS/test/SKB_PROFETA/search/jobs/export'

    dest = (dHOST, dPORT)
    res = adams_call(durl, 1) #0, 1 only
    if res.status_code ==200:
        for res_line in res.text.splitlines():
            jsonString = json.loads(res_line)
            #sock.sendto(json.dumps(jsonString['result']), dest)
            print(json.dumps(jsonString['result']))
        sock.close()

def print_response(res):
    #print(res.status_code)
    print(res.url)
    print(res.text)
    #print(res.content)
    print(res.encoding)
    #print(res.headers)

def test():
    f = open('iplist.txt', 'r')
    line = f.read() # read, readline, readlines 테스트
    print(line)
    f.close()

if __name__ == '__main__':
    #adams_restapi_processing()
    a = logstash_call("indices")
    print_response(a)
    b = logstash_call("allocation")
    print_response(b)

    #test()