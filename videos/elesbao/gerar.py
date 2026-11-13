"""Gera o projeto HyperFrames do vídeo 'Elesbão' a partir de roteiro.json + cenas.
Uso: python3 gerar.py  (escreve em ../elesbao-hf)
"""
import json, os, re, subprocess, html

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "..", "elesbao-hf")
os.makedirs(os.path.join(OUT, "compositions"), exist_ok=True)

roteiro = {x["id"]: x["t"] for x in json.load(open(os.path.join(BASE, "roteiro.json")))}

def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())

LEAD = 0.5   # silêncio antes da voz em cada cena
TAIL = 0.9   # respiro depois da voz

# ---------------------------------------------------------------------------
# Cenas: camadas de imagem/vídeo e textos
# bg: lista de (tipo, arquivo, modo) ; modo: "cover" (Ken Burns) | "portrait" (à direita)
# txt: lista de (estilo, texto, t_ini_rel(0-1 da cena), t_fim_rel)
# ---------------------------------------------------------------------------
CENAS = {
 "s01": dict(bg=[("img","punicao_santana","cover")], extra_lead=1.2, txt=[
     ("kicker","Campinas · 9 de dezembro de 1835",0.02,0.42),
     ("rotulo","Ilustração: punição pública no Rio de Janeiro — J. M. Rugendas, c. 1835",0.44,0.6),
     ("titulo","ELESBÃO",0.62,1.0)]),
 "s02": dict(bg=[("img","debret_escravidao","cover")], txt=[
     ("kicker","Novembro · Mês da Consciência Negra",0.04,0.55),
     ("frase","Uma história que o Brasil tentou esquecer",0.5,1.0)]),
 "s03": dict(bg=[("img","mapa_cabinda","cover"),("img","mapa_congo_angola","cover")], txt=[
     ("kicker","África Central · Costa de Loango",0.03,0.5),
     ("rotulo","CABINDA — porto de embarque, ao norte do rio Congo",0.5,1.0)]),
 "s04": dict(bg=[("img","navio_negreiro","cover")], txt=[
     ("kicker","A travessia do Atlântico",0.03,0.45),
     ("numero","≈ 4,8 milhões|de africanos desembarcados no Brasil (estimativa)",0.62,1.0)]),
 "s05": dict(bg=[("img","mercado_escravos","cover"),("img","valongo_hoje","cover")], txt=[
     ("rotulo","Mercado de escravos, Rio de Janeiro — J.-B. Debret",0.05,0.48),
     ("rotulo","Cais do Valongo · Patrimônio Mundial da UNESCO (2017)",0.55,1.0)]),
 "s06": dict(bg=[("img","campinas_1880","cover"),("img","ferrez_cafe","cover")], txt=[
     ("kicker","Campinas · século XIX",0.03,0.45),
     ("rotulo","Escravizados numa fazenda de café — Marc Ferrez, c. 1885",0.55,1.0)]),
 "s07": dict(bg=[("img","feitores","portrait"),("img","colhendo_cafe","portrait")], txt=[
     ("bloco","ENGENHO ROMÃO|propriedade do capitão Luiz José de Oliveira",0.03,0.6),
     ("frase","E se eu fugir?",0.78,1.0)]),
 "s08": dict(bg=[("img","negros_novos","portrait"),("img","zumbi_parreiras","portrait")], txt=[
     ("bloco","QUILOMBO|Inquérito de 11 de agosto de 1831",0.05,0.5),
     ("bloco","PALMARES|Zumbi — Antônio Parreiras (pintura)",0.58,1.0)]),
 "s09": dict(bg=[], txt=[
     ("data","20 DE MAIO DE 1831",0.03,0.4),
     ("versus","A versão das autoridades|Elesbão e Narciso mataram o capitão|Elesbão|afirmou ser inocente",0.42,1.0)]),
 "s10": dict(bg=[("img","navio_negreiro","cover")], txt=[
     ("bloco","LEI DE 7 DE NOVEMBRO DE 1831|proíbe o tráfico de africanos para o Brasil",0.08,0.62),
     ("carimbo","“PARA INGLÊS VER”",0.45,1.0)]),
 "s11": dict(bg=[("img","punicao_fouet","portrait")], txt=[
     ("bloco","CONDENADOS À MORTE|a pedido da Câmara de Vereadores de Campinas",0.03,0.42),
     ("bloco","NARCISO|executado em São Paulo · 24 de maio de 1833",0.45,0.8),
     ("bloco","ELESBÃO|esperaria mais dois anos",0.8,1.0)]),
 "s12": dict(bg=[("img","punicao_publica","cover")], txt=[
     ("bloco","JANEIRO DE 1835|Revolta dos Malês · Salvador",0.1,0.5),
     ("bloco","LEI Nº 4, DE 10 DE JUNHO DE 1835|pena de morte para escravizados que matassem ou ferissem seus senhores",0.5,1.0)]),
 "s13": dict(bg=[("img","campinas_1880","cover"),("img","punicao_santana","cover")], txt=[
     ("data","9 DE DEZEMBRO DE 1835",0.0,0.18),
     ("lista","As autoridades|O vigário|O sacristão|O carrasco|A Guarda Nacional|A cavalaria|ELESBÃO",0.2,0.72),
     ("frase","Vários senhores mandaram seus escravizados assistirem.",0.75,1.0)]),
 "s14": dict(bg=[], txt=[
     ("sentenca","“Adendo a sentença, declaro que depois do réu sofrer a pena de morte cortar-se-ão as mãos e a cabeça, esta será remetida para a Vila de Jundiaí, e ali colocada num poste em lugar público…”|— Trecho da sentença, 1835",0.18,1.0)]),
 "s15": dict(bg=[("img","tronco","cover"),("img","punicao_fouet","portrait")], txt=[
     ("frase","O objetivo era o medo.",0.03,0.4),
     ("lista","O tronco.|O chicote.|O pelourinho.|A forca.",0.62,1.0)]),
 "s16": dict(bg=[("img","luiz_gama","portrait"),("img","zumbi_parreiras","portrait")], txt=[
     ("frase","Mas o medo não venceu.",0.02,0.3),
     ("bloco","LUIZ GAMA (1830–1882)|abolicionista negro · libertou centenas de pessoas nos tribunais",0.45,1.0)]),
 "s17": dict(bg=[("img","ferrez_cafe","cover")], txt=[
     ("data","13 DE MAIO DE 1888",0.03,0.5),
     ("rotulo","Último país das Américas a abolir a escravidão · sem terra, sem reparação",0.5,1.0)]),
 "s18": dict(bg=[("img","valongo_hoje","cover"),("img","zumbi_parreiras","portrait")], txt=[
     ("kicker","Memória e resistência",0.03,0.35),
     ("bloco","O AUTO DO ESCRAVIZADO ELESBÃO|o Extermínio da Juventude Negra · Campinas",0.3,0.66),
     ("bloco","ELESBÃO|livro de Valdir Oliveira · teatro: “Elesbão: um sonho de liberdade”, de Roberto Boni",0.68,1.0)]),
 "s19": dict(bg=[("img","punicao_santana","cover")], txt=[
     ("frase","O que mudou? E o que ainda não mudou?",0.25,0.62),
     ("titulo","ELESBÃO|† Campinas, 9 de dezembro de 1835",0.72,1.0)]),
 "s20": dict(bg=[], extra_tail=4.0, txt=[
     ("creditos","Pesquisa e produção|Professor de História|Paulo Shetara",0.0,1.0)]),
}

def asset(kind, name):
    d = "img" if kind == "img" else "vid"
    for ext in (".jpg", ".mp4"):
        p = f"assets/{d}/{name}{ext}"
        if os.path.exists(os.path.join(OUT, p)):
            return p
    imgs=sorted(f for f in os.listdir(os.path.join(OUT,"assets/img")) if f.endswith(".jpg"))
    if not imgs: raise SystemExit(f"faltando: {kind} {name}")
    FALTANDO.add(name)
    return "assets/img/"+imgs[hash(name)%len(imgs)]

FALTANDO=set()
def kind_of(src):
    return "vid" if src.endswith(".mp4") else "img"

def esc(s):
    return html.escape(s, quote=True)

CSS_COMUM = """
#root{position:absolute;inset:0;overflow:hidden;background:#0b0907;font-family:'Inter',sans-serif;color:#f3eadb}
.bg{position:absolute;inset:0;overflow:hidden}
.bg img,.bg video{position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover}
.bg.portrait img{left:auto;right:120px;top:60px;width:820px;height:960px;object-fit:contain;object-position:center}
.vin{position:absolute;inset:0;background:radial-gradient(ellipse at center,rgba(0,0,0,.30) 30%,rgba(0,0,0,.82) 100%),linear-gradient(180deg,rgba(0,0,0,.35) 0%,rgba(0,0,0,0) 30%,rgba(0,0,0,0) 60%,rgba(0,0,0,.65) 100%)}
.sombra{position:absolute;inset:0;background:linear-gradient(90deg,rgba(11,9,7,.92) 0%,rgba(11,9,7,.75) 40%,rgba(11,9,7,0) 62%)}
.t{position:absolute;left:150px;right:150px;opacity:0}
.kicker{top:150px;text-shadow:0 2px 12px #000,0 0 30px #000;font-family:'Oswald',sans-serif;font-size:40px;letter-spacing:.32em;text-transform:uppercase;color:#d9a441}
.kicker:before{content:'';display:inline-block;width:70px;height:3px;background:#b8322a;vertical-align:middle;margin-right:24px}
.titulo{top:300px;text-align:center;font-family:'Playfair Display',serif;font-weight:900;font-size:220px;letter-spacing:.06em;color:#f3eadb;text-shadow:0 4px 0 rgba(0,0,0,.6),0 8px 40px rgba(0,0,0,.95),0 0 80px rgba(0,0,0,.9)}
.titulo small{display:block;font-family:'Oswald',sans-serif;font-weight:400;font-size:46px;text-shadow:0 2px 10px #000,0 0 30px #000;letter-spacing:.25em;color:#d9a441;margin-top:10px}
.frase{top:380px;text-align:center;font-family:'Playfair Display',serif;font-style:italic;font-size:84px;line-height:1.15;text-shadow:0 3px 0 rgba(0,0,0,.6),0 6px 30px #000,0 0 70px #000}
.rotulo{top:150px;font-family:'Oswald',sans-serif;font-size:36px;letter-spacing:.08em;color:#f3eadb;}
.rotulo span{background:rgba(11,9,7,.72);padding:12px 22px;border-left:5px solid #b8322a}
.numero{top:330px;text-align:center}
.numero b{display:block;font-family:'Playfair Display',serif;font-weight:900;font-size:190px;color:#d9a441;text-shadow:0 4px 0 rgba(0,0,0,.7),0 8px 40px #000,0 0 80px #000}
.numero span{background:rgba(11,9,7,.7);padding:8px 20px;font-family:'Oswald',sans-serif;font-size:46px;letter-spacing:.12em;text-transform:uppercase}
.bloco{top:300px;right:960px}
.bloco b{display:block;font-family:'Oswald',sans-serif;font-weight:700;font-size:74px;line-height:1.05;letter-spacing:.04em;color:#f3eadb}
.bloco span{display:block;margin-top:22px;font-family:'Playfair Display',serif;font-style:italic;font-size:44px;line-height:1.3;color:#d9a441}
.bloco:before{content:'';display:block;width:90px;height:5px;background:#b8322a;margin-bottom:30px}
.bloco.largo{right:700px;background:rgba(11,9,7,.72);padding:40px 50px;left:110px}
.data{top:420px;text-align:center;font-family:'Oswald',sans-serif;font-weight:700;font-size:120px;letter-spacing:.1em;color:#f3eadb;text-shadow:0 4px 0 rgba(0,0,0,.6),0 0 60px #000}
.carimbo{top:640px;left:auto;right:180px;width:auto;font-family:'Oswald',sans-serif;font-weight:700;font-size:80px;color:#e0443a;background:rgba(11,9,7,.82);border:8px solid #b8322a;padding:10px 40px;letter-spacing:.06em}
.versus{top:300px;display:flex;gap:80px}
.versus div{flex:1;padding:40px 50px;background:rgba(243,234,219,.06);border-top:6px solid #d9a441}
.versus div+div{border-top-color:#b8322a}
.versus b{display:block;font-family:'Oswald',sans-serif;font-size:44px;letter-spacing:.2em;text-transform:uppercase;color:#d9a441;margin-bottom:24px}
.versus div+div b{color:#b8322a}
.versus span{font-family:'Playfair Display',serif;font-size:62px;line-height:1.2}
.lista{top:200px}
.lista p{font-family:'Oswald',sans-serif;font-size:62px;letter-spacing:.06em;line-height:1.3;opacity:0;text-shadow:0 4px 20px rgba(0,0,0,.9)}
.lista p.forte{color:#d9a441;font-weight:700;font-size:80px}
.sentenca{top:170px;left:260px;right:260px;padding:70px 90px;background:#e8dcc3;color:#2a1d12;box-shadow:0 30px 80px rgba(0,0,0,.7)}
.sentenca p{font-family:'EB Garamond',serif;font-size:56px;line-height:1.35}
.sentenca em{display:block;margin-top:30px;font-family:'Oswald',sans-serif;font-style:normal;font-size:32px;letter-spacing:.15em;text-transform:uppercase;color:#7a2a20}
.creditos{top:300px;text-align:center}
.creditos i{display:block;font-family:'Oswald',sans-serif;font-style:normal;font-size:40px;letter-spacing:.35em;text-transform:uppercase;color:#d9a441}
.creditos span{display:block;margin-top:40px;font-family:'Playfair Display',serif;font-style:italic;font-size:60px}
.creditos b{display:block;font-family:'Playfair Display',serif;font-weight:900;font-size:130px;letter-spacing:.03em}
.creditos small{display:block;margin-top:70px;font-family:'Inter',sans-serif;font-size:28px;color:#a99a85}
"""

def texto_html(sid, i, estilo, txt):
    tid = f"{sid}-t{i}"
    parts = txt.split("|")
    if estilo == "titulo":
        inner = esc(parts[0]) + (f"<small>{esc(parts[1])}</small>" if len(parts) > 1 else "")
    elif estilo == "numero":
        inner = f"<b>{esc(parts[0])}</b><span>{esc(parts[1])}</span>"
    elif estilo == "bloco":
        inner = f"<b>{esc(parts[0])}</b><span>{esc(parts[1])}</span>"
    elif estilo == "rotulo":
        inner = f"<span>{esc(parts[0])}</span>"
    elif estilo == "versus":
        inner = f"<div><b>{esc(parts[0])}</b><span>{esc(parts[1])}</span></div><div><b>{esc(parts[2])}</b><span>{esc(parts[3])}</span></div>"
    elif estilo == "lista":
        inner = "".join(f'<p id="{tid}-l{k}"' + (' class="forte"' if p.isupper() and len(parts) > 4 else "") + f">{esc(p)}</p>" for k, p in enumerate(parts))
    elif estilo == "sentenca":
        inner = f"<p>{esc(parts[0])}</p><em>{esc(parts[1])}</em>"
    elif estilo == "creditos":
        inner = (f"<i>{esc(parts[0])}</i><span>{esc(parts[1])}</span><b>{esc(parts[2])}</b>"
                 "<small>Imagens: Wikimedia Commons (domínio público — ver descrição) · Narração sintética</small>")
    else:
        inner = esc(parts[0])
    return tid, f'<div id="{tid}" class="t {estilo}">{inner}</div>'

def cena_html(sid, D, spec):
    bg = spec["bg"]
    n = len(bg)
    camadas, js = [], []
    seg = D / n if n else D
    for k, (kind, name, modo) in enumerate(bg):
        lid = f"{sid}-bg{k}"
        src = asset(kind, name); kind = kind_of(src)
        start = k * seg
        d = seg + (0.8 if k < n - 1 else 0)
        d = min(d, D - start)
        if kind == "img":
            media = f'<img id="{lid}-m" src="{src}" alt="">'
        else:
            media = f'<video id="{lid}-m" src="{src}" muted playsinline class="clip" data-start="{start:.2f}" data-duration="{d:.2f}" data-track-index="{k}"></video>'
        camadas.append(f'<div id="{lid}" class="bg {modo}" style="z-index:{k+1}">{media}</div>')
        # fade in (exceto primeira) + Ken Burns
        if k > 0:
            js.append(f'tl.fromTo("#{lid}",{{opacity:0}},{{opacity:1,duration:0.8,ease:"sine.inOut"}},{start:.2f});')
        else:
            js.append(f'tl.set("#{lid}",{{opacity:1}},0);')
        if k < n - 1:
            js.append(f'tl.set("#{lid}",{{opacity:0}},{start + d:.2f});')
        if kind == "img":
            if modo == "cover":
                dirx = [-40, 40][k % 2]
                js.append(f'tl.fromTo("#{lid}-m",{{scale:1.06,x:{-dirx}}},{{scale:1.18,x:{dirx},duration:{d:.2f},ease:"none"}},{start:.2f});')
            else:
                js.append(f'tl.fromTo("#{lid}-m",{{scale:1.0,y:10}},{{scale:1.07,y:-10,duration:{d:.2f},ease:"none"}},{start:.2f});')
    portrait = any(m == "portrait" for _, _, m in bg)
    camadas.append(f'<div id="{sid}-vin" class="vin" style="z-index:20"></div>')
    if portrait:
        camadas.append(f'<div id="{sid}-sombra" class="sombra" style="z-index:21"></div>')
    textos = []
    for i, (estilo, txt, a, b) in enumerate(spec["txt"]):
        tid, h = texto_html(sid, i, estilo, txt)
        textos.append(h)
        t0, t1 = a * D, b * D
        t1 = min(t1, D - 0.05)
        if estilo == "lista":
            itens = txt.split("|")
            js.append(f'tl.set("#{tid}",{{opacity:1}},{t0:.2f});')
            passo = (t1 - t0 - 0.6) / max(1, len(itens))
            for k in range(len(itens)):
                js.append(f'tl.fromTo("#{tid}-l{k}",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:0.45,ease:"power3.out"}},{t0 + k*passo:.2f});')
            js.append(f'tl.to("#{tid}",{{opacity:0,duration:0.4,ease:"power2.in"}},{t1-0.4:.2f});')
        elif estilo in ("titulo", "data", "carimbo"):
            js.append(f'tl.fromTo("#{tid}",{{opacity:0,scale:1.12}},{{opacity:1,scale:1,duration:1.2,ease:"power3.out"}},{t0:.2f});')
            if b < 1.0 or sid != "s19":
                js.append(f'tl.to("#{tid}",{{opacity:0,duration:0.4,ease:"power2.in"}},{t1-0.4:.2f});')
        else:
            js.append(f'tl.fromTo("#{tid}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.8,ease:"power3.out"}},{t0:.2f});')
            if sid != "s20":
                js.append(f'tl.to("#{tid}",{{opacity:0,duration:0.4,ease:"power2.in"}},{t1-0.4:.2f});')
    cls = ""
    if not portrait:
        textos = [h.replace('class="t bloco"','class="t bloco largo"') for h in textos]
    return f"""<template>
<style>{CSS_COMUM.replace('#root', f'#{sid}')}</style>
<div id="{sid}" class="{cls.strip()}" data-composition-id="{sid}" data-width="1920" data-height="1080" data-layout-allow-overlap>
{chr(10).join(camadas)}
<div id="{sid}-txt" style="position:absolute;inset:0;z-index:30">
{chr(10).join(textos)}
</div>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
tl.set({{}}, {{}}, {D:.2f});
window.__timelines["{sid}"] = tl;
</script>
</template>
""".replace(f"#{sid}{{position:absolute", f"#{sid}{{position:absolute")

def frases(t):
    # quebra em grupos de até ~7 palavras, respeitando pontuação
    sent = re.split(r"(?<=[.!?:])\s+", t.strip())
    grupos = []
    for s in sent:
        w = s.split()
        while w:
            n = len(w)
            if n <= 8:
                grupos.append(" ".join(w)); break
            cut = 7
            for j in range(4, min(9, n - 2)):
                if w[j - 1].endswith(","):
                    cut = j
            grupos.append(" ".join(w[:cut])); w = w[cut:]
    return grupos

# --------------------------- montagem ---------------------------
hosts, audios, caps, cap_js = [], [], [], []
t = 0.0
import sys
ordem = sorted(CENAS)
if len(sys.argv) > 1: ordem = [x for x in ordem if x in sys.argv[1].split(",")]
for idx, sid in enumerate(ordem):
    spec = CENAS[sid]
    voz = f"assets/voz/{sid}.wav"
    vd = dur(os.path.join(OUT, voz))
    lead = LEAD + spec.get("extra_lead", 0)
    D = round(lead + vd + TAIL + spec.get("extra_tail", 0), 2)
    open(os.path.join(OUT, "compositions", f"{sid}.html"), "w").write(cena_html(sid, D, spec))
    hosts.append(f'<div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{t:.2f}" data-duration="{D:.2f}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>')
    audios.append(f'<audio id="voz-{sid}" class="clip" src="{voz}" data-start="{t+lead:.2f}" data-duration="{vd:.2f}" data-track-index="3" data-volume="1"></audio>')
    # legendas proporcionais por caracteres
    if sid != "s20":
        marcas = json.load(open(os.path.join(OUT, f"assets/voz/{sid}.json")))
        lista = []
        for frase, a, b in marcas:
            gs = frases(frase); tot = sum(len(g) + 4 for g in gs); c0 = a
            for g in gs:
                gd = (b - a) * (len(g) + 4) / tot; lista.append((g, t + lead + c0, gd + (0.25 if g is gs[-1] else 0))); c0 += gd
        for gi, (g, c, gd) in enumerate(lista):
            cid = f"cap-{sid}-{gi}"
            caps.append(f'<div id="{cid}" class="cap"><span>{esc(g)}</span></div>')
            cap_js.append(f'tl.fromTo("#{cid}",{{opacity:0}},{{opacity:1,duration:0.12}},{c:.2f});')
            cap_js.append(f'tl.to("#{cid}",{{opacity:0,duration:0.1}},{c+gd-0.1:.2f});')
            cap_js.append(f'tl.set("#{cid}",{{visibility:"hidden"}},{c+gd:.2f});')
    t += D
TOTAL = round(t, 2)

captions = f"""<template>
<style>
#legendas{{position:absolute;inset:0}}
#legendas .cap{{position:absolute;left:0;right:0;bottom:96px;text-align:center;opacity:0;overflow:visible}}
#legendas .cap span{{display:inline-block;max-width:1500px;padding:10px 26px;background:rgba(8,6,5,.62);border-radius:6px;font-family:'Inter',sans-serif;font-weight:700;font-size:44px;line-height:1.25;color:#fff}}
</style>
<div id="legendas" data-composition-id="legendas" data-width="1920" data-height="1080">
{chr(10).join(caps)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(cap_js)}
tl.set({{}}, {{}}, {TOTAL:.2f});
window.__timelines["legendas"] = tl;
</script>
</template>
"""
open(os.path.join(OUT, "compositions", "legendas.html"), "w").write(captions)

index = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<script src="assets/gsap.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1920px;height:1080px;overflow:hidden;background:#0b0907}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.2f}" data-width="1920" data-height="1080">
{chr(10).join(hosts)}
<div id="legendas" data-composition-id="legendas" data-composition-src="compositions/legendas.html" data-start="0" data-duration="{TOTAL:.2f}" data-track-index="2" data-track-kind="captions" data-width="1920" data-height="1080" style="z-index:50"></div>
{chr(10).join(audios)}
<audio id="trilha" class="clip" src="assets/trilha.m4a" data-start="0" data-duration="{TOTAL:.2f}" data-track-index="4" data-volume="0.3" data-fade-in="2" data-fade-out="5"></audio>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
open(os.path.join(OUT, "index.html"), "w").write(index)
print("duração total:", TOTAL, "s"); print("imagens provisórias:", sorted(FALTANDO))
