"""Busca arquivos no Wikimedia Commons: python3 busca.py 'termo' [n]"""
import sys, json, urllib.request, urllib.parse
q=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 8
u="https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(dict(action="query",format="json",generator="search",gsrsearch=q,gsrnamespace=6,gsrlimit=n,prop="imageinfo",iiprop="size|extmetadata",iiextmetadatafilter="LicenseShortName"))
r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"canal-historia-video-bot/1.0 (https://github.com/pauloshetara-coder/pauloshetara)"})))
for p in sorted(r.get("query",{}).get("pages",{}).values(),key=lambda p:p.get("index",0)):
    ii=p["imageinfo"][0]; lic=ii.get("extmetadata",{}).get("LicenseShortName",{}).get("value","?")
    print(f'{ii["width"]}x{ii["height"]} [{lic}] {p["title"][5:]}')
