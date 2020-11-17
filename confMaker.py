import pandas as pd

output_files_list =[
    "skb_infralog_dict_dept.yml",
    "skb_infralog_dict_group.yml",
    "skb_infralog_dict_hostname.yml",
    "skb_infralog_dict_location.yml",
    "skb_infralog_dict_service.yml",
    "skb_infralog_dict_whitelist.yml", #ony for send_assets_update_for_whitelist
]

output_files_dict ={
    "skb_infralog_dict_dept.yml": 5,
    "skb_infralog_dict_group.yml": 0,
    "skb_infralog_dict_hostname.yml": 1,
    "skb_infralog_dict_location.yml": 4,
    "skb_infralog_dict_service.yml": 3,
#    "skb_infralog_dict_whitelist_20200607.yml", //manual
}

def sens_assets_update(filename):
    print("sens_assets_update start")

    for output_file in output_files_dict:
        df = pd.read_excel(filename, usecols=[output_files_dict[output_file], 2])
        f = open(output_file, "w", encoding='UTF-8')
        for index, row in df.iterrows():
            if(output_file == output_files_list[1] or output_file == output_files_list[2]):
                str = '\"{}\": \"{}\"\n'.format(row[1], row[0])
            else:
                str = '\"{}\": \"{}\"\n'.format(row[0], row[1])
            print(str)
            f.write(str)
        f.close()


def send_assets_update_for_whitelist(filename):
    print("send_assets_update_for_whitelist start")

    df = pd.read_excel(filename, usecols=[0, 1])
    f = open(output_files_list[5], "w", encoding='UTF-8')
    for index, row in df.iterrows():
        str = '\"{}\": \"{}\"\n'.format(row[0], row[1])
        print(str)
        f.write(str)
    f.close()

def sens_assets_iplist(filename):
    print("sens_assets_iplist start")

    for output_file in output_files_dict:
        df = pd.read_excel(filename, usecols= [1,2])
        f = open('iplist.txt', "w", encoding='UTF-8')
        for index, row in df.iterrows():
            str = '{}\n'.format(row[1])
            print(str)
            f.write(str)
        f.close()

if __name__ == '__main__':
    #test(False)
    #sens_assets_update('SENS_장비리스트_관할부서__201102.xlsx')
    #send_assets_update_for_whitelist('IP별 장비접속타입(whitelist).xlsx')
    sens_assets_iplist('SENS_장비리스트_관할부서__201102.xlsx')