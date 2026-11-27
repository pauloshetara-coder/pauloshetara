"""Baixa imagens (Commons via lista.json, AIC via aic.txt) para assets/img, com pausas e novas tentativas."""
import json, os, time, urllib.request, urllib.parse
H={"User-Agent":"canal-historia-video-bot/1.0"}
OUT="assets/img"
def get(u, tries=6):
    for i in range(tries):
        try: return urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=60).read()
        except Exception as e:
            print("  tentativa",i+1,e); time.sleep(10*(i+1))
    return None
for n,f in json.load(open("lista.json")).items():
    p=f"{OUT}/{n}.orig"
    if os.path.exists(p): continue
    info=get("https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(dict(action="query",format="json",titles="File:"+f,prop="imageinfo",iiprop="url")))
    d=None
    if info:
        pg=list(json.loads(info)["query"]["pages"].values())[0]
        if "imageinfo" in pg:
            ii=pg["imageinfo"][0]; time.sleep(3); time.sleep(12); d=get(ii["url"])
        else: print("  nao existe:",f)
    if d: open(p,"wb").write(d); print("ok",n,len(d))
    else: print("FALHOU",n)
    time.sleep(20)
for l in open("aic.txt"):
    n,i=l.strip().split("|"); p=f"{OUT}/{n}.orig"
    if os.path.exists(p): continue
    m=json.loads(get(f"https://api.artic.edu/api/v1/artworks/{i}?fields=image_id,title"))["data"]
    d=get(f"https://www.artic.edu/iiif/2/{m['image_id']}/full/1686,/0/default.jpg")
    if d: open(p,"wb").write(d); print("ok",n,len(d),m["title"])
    else: print("FALHOU",n)
