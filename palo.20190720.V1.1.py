#!/bin/python3
import sys
import re
import getpass
import requests
import xml.etree.ElementTree as ET
import urllib3
import urllib.parse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


IPlists = ['10.40.194.253', #KR
           '10.42.255.106', #JP
           '10.41.255.240', #CN
           '10.212.8.31', #SG
           '10.20.253.6', #UK
           '10.10.253.6', #USDB 2
           '10.10.253.5', #USDB 1
           '10.11.223.5', #USSC
           ]

#API key = LUFRPT1BQU9Zcm1ybVRtcnBvNU9MbUN5cXJSLy9QN2M9a2QrbzdodjFqZm5jVUgyb2pXMEYrNWxpWUdZWVZYM3ZhaHU3MHhjcjRyRT0=

def draft():
    for pAddr in IPlists:
        # show system
        params = {'type': 'op', 'cmd': '<show><system><info></info></system></show>', 'key': pApikey}
        url = 'https://%s/api/' % pAddr

        #print(url)
        response = requests.get(url, params=params, verify=False)
        xmlStr = response.text
        #print(xmlStr)
        root = ET.fromstring(xmlStr)
        #print(root)
        break



def getAPIkey():
    for ip in IPlists:
        pAddr = ip
        pUser = 'minsu.kim2'
        pPass = '0510Alstn1@'


        # API KEY URL 생성
        params = {'type': 'keygen', 'user': pUser, 'password': pPass}
        url = 'https://%s/api/' % pAddr
        response = requests.get(url, params=params, verify=False)

        # API KEY 추출
        xmlStr = response.text
        root = ET.fromstring(xmlStr)
        #print(xmlStr)
        for x in root.findall('result'):
            pApikey = x.find('key').text
            #print(pApikey)
            return pApikey

def runAudit(pApikey):
    # filter date
    fSday = '2019/01/01'
    fEday = '2019/12/01'
    fTime = '00:00:00'
    fGeq = 'receive_time geq'
    fLeq = 'receive_time leq'

    # query config log (max line 5000)
    params = {'type': 'log', 'log-type': 'config',
              'query': '(%s \'%s %s\') and (%s \'%s %s\')' % (fGeq, fSday, fTime, fLeq, fEday, fTime), 'nlogs': '5000',
              'key': pApikey}
    for pAddr in IPlists:
        url = 'https://%s/api/' % pAddr
        response = requests.get(url, params=params, verify=False)
        print(urllib.parse.unquote(response.url))
        xmlStr = response.text
        print(xmlStr)
        job = 1
        root = ET.fromstring(xmlStr)
        for x in root.findall('result'):
            job = x.find('job').text
            print(job)
            params = {'type': 'log', 'action': 'get', 'job-id': job, 'key': pApikey}
            url = 'https://%s/api/' % pAddr
            response = requests.get(url, params=params, verify=False)
            urllib.parse.unquote(response.url)
            xmlStr = response.text
            root = ET.fromstring(xmlStr)
            print('receive_time\t', 'type\t', 'host\t', 'cmd\t', 'admin\t', 'client\t', 'result\t',
                  'before-change-preview\t', 'after-change-preview\t', 'full-path\t')
            for x in root.findall('result/log/logs/entry'):
                rev = x.find('receive_time').text
                typ = x.find('type').text
                hos = x.find('host').text
                cmd = x.find('cmd').text
                adm = x.find('admin').text
                cli = x.find('client').text
                res = x.find('result').text
                node1 = x.find('before-change-preview')
                node2 = x.find('after-change-preview')
                node3 = x.find('full-path')
                if node1 is not None:
                    bef = x.find('before-change-preview').text
                else:
                    bef = None
                if node2 is not None:
                    aft = x.find('after-change-preview').text
                else:
                    aft = None
                if node3 is not None:
                    ful = x.find('full-path').text
                else:
                    ful = None

                print(rev, '\t', typ, '\t', hos, '\t', cmd, '\t', adm, '\t', cli, '\t', res, '\t', bef, '\t', aft, '\t',ful)
            return ""

def getSysinfo(pApikey):
    for pAddr in IPlists:
        # show system
        params = {'type': 'op', 'cmd': '<show><system><info></info></system></show>', 'key': pApikey}
        url = 'https://%s/api/' % pAddr

        print(url)
        response = requests.get(url, params=params, verify=False)
        xmlStr = response.text
        # print(xmlStr)
        #print('시스템정보')
        root = ET.fromstring(xmlStr)
        for x in root.findall('result/system'):
            hostName = x.find('hostname').text
            upTime = x.find('uptime').text
            ipAddr = x.find('ip-address').text
            dModel = x.find('model').text
            dSerial = x.find('serial').text
            swVer = x.find('sw-version').text
            appVer = x.find('app-version').text
            appDate = x.find('app-release-date').text
            avVer = x.find('av-version').text
            avDate = x.find('av-release-date').text
            thVer = x.find('threat-version').text
            thDate = x.find('threat-release-date').text
            wfVer = x.find('wildfire-version').text
            wfDate = x.find('wildfire-release-date').text

            print('점검대상:', ipAddr, )
            print('점검모델:', dModel)
            print('시리얼번호:', dSerial)
            print('SW 버전:', swVer)
            print('가동시간:', upTime, )
            print('\n버전관리')
            print('Application:\t', appVer, '\tDate:', appDate)
            print('Anti-virus:\t', avVer, '\tDate:', avDate)
            print('Threat:\t\t', thVer, '\tDate:', thDate)
            print('Wildfire:\t', wfVer, '\tDate:', wfDate)

            # show mp
            params = {'type': 'op', 'cmd': '<show><system><resources></resources></system></show>', 'key': pApikey}
            url = 'https://%s/api/' % pAddr
            response = requests.get(url, params=params, verify=False)
            xmlStr = response.text
            root = ET.fromstring(xmlStr)
            M = re.compile("Mem:\s*\d*\w\s*\w*,\s*\d*\w\s*\w*,\s*\d*\w\s*\w*,\s*\d*\w\s*\w*")
            S = re.compile("Swap:\s*\d*\w\s*\w*,\s*\d*\w\s*\w*,\s*\d*\w\s*\w*,\s*\d*\w\s*\w*")
            L = re.compile("load\s*average:\s*\d*.\d*,\s*\d*.\d*,\s*\d*.\d*")
            print('\nMP RESOUCE')
            print(L.findall(xmlStr))
            print(M.findall(xmlStr))
            print(S.findall(xmlStr))

            # show dp
            params = {'type': 'op',
                      'cmd': '<show><running><resource-monitor><week><last>1</last></week></resource-monitor></running></show>',
                      'key': pApikey}
            url = 'https://%s/api/' % pAddr
            response = requests.get(url, params=params, verify=False)
            xmlStr = response.text
            root = ET.fromstring(xmlStr)
            print('dp\n',xmlStr)
            print('\nDP RESOURCE')
            for x in root.findall('result/resource-monitor/data-processors/dp0/week/cpu-load-average/entry'):
                dpCoreid = x.find('coreid').text
                dpCoreav = x.find('value').text
                print('Coreid:', dpCoreid, 'Average:', dpCoreav)

            # show session
            params = {'type': 'op', 'cmd': '<show><session><info></info></session></show>', 'key': pApikey}
            url = 'https://%s/api/' % pAddr
            response = requests.get(url, params=params, verify=False)
            xmlStr = response.text
            # print('session',xmlStr)
            print('\nSESSIONS')
            root = ET.fromstring(xmlStr)
            for x in root.findall('result'):
                sMax = x.find('num-max').text
                sActive = x.find('num-active').text
                sTcp = x.find('num-tcp').text
                sUdp = x.find('num-udp').text
                sKbps = x.find('kbps').text
                print('MaxSession:', sMax, )
                print('ActiveSession:', sActive)
                print('TCP:', sTcp)
                print('UDP:', sUdp)
                print('Troughput:', sKbps, 'Kbps')

            # show support
            params = {'type': 'op', 'cmd': '<request><support><info></info></support></request>', 'key': pApikey}
            url = 'https://%s/api/' % pAddr
            response = requests.get(url, params=params, verify=False)
            xmlStr = response.text
            root = ET.fromstring(xmlStr)
            # print(xmlStr)
            print('\nSUPPORT')
            for x in root.findall('result/SupportInfoResponse/Support'):
                supDate = x.find('ExpiryDate').text
                supLevel = x.find('SupportLevel').text
                print('SupportLevel:', supLevel, 'ExpiryDate:', supDate)

            # show license
            params = {'type': 'op', 'cmd': '<request><license><info></info></license></request>', 'key': pApikey}
            url = 'https://%s/api/' % pAddr
            response = requests.get(url, params=params, verify=False)
            xmlStr = response.text
            root = ET.fromstring(xmlStr)
            print('\nLICENSES')
            for x in root.findall('result/licenses/entry'):
                liFeature = x.find('feature').text
                liExpires = x.find('expires').text
                print('Feature:', liFeature, '\tExpires:', liExpires)

if __name__ == '__main__':
    #getAPIkey()
    key= getAPIkey()
    print(key)
    runAudit(key)
    #getSysinfo(key)
    #draft()