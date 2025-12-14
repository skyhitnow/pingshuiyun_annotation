import re,json
dic={}
templine=""
with open("yun.txt","r",encoding="utf8") as f:
    for line in f:
        if re.match(r"^[一二三四五六七八九十].*",line):
            if templine!="":
                templine = re.sub(r'\[.*?\]', '', templine)
                parts=templine.split()
                # print(templine)
                # print(parts)
                print(parts[0])
                print(parts[1])
                dic[parts[1]]=parts[0]
                templine=""
            templine=line.strip()
            continue
        else:
            templine+=line.strip()



with open("dicmap.json","w",encoding="utf8") as f:
    json.dump(dic,f,ensure_ascii=False,indent=4)
