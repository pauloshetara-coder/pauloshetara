"""Narração emotiva: frase a frase, mais lenta e com pausas maiores nas cenas tristes."""
import json, re, os, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
C="/root/.cache/hyperframes/tts"
k=Kokoro(f"{C}/models/kokoro-v1.0.onnx", f"{C}/voices/voices-v1.0.bin")
BASE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(BASE,"..","elesbao-hf","assets","voz")
os.makedirs(OUT,exist_ok=True)
# humor por cena: (velocidade, pausa entre frases)
TRISTE={"s01","s04","s09","s11","s13","s14","s15","s17","s19"}
SOLENE={"s02","s08","s16","s18","s20"}
def humor(sid):
    if sid in TRISTE: return 0.84, 0.75
    if sid in SOLENE: return 0.9, 0.5
    return 0.95, 0.38
for x in json.load(open(os.path.join(BASE,"roteiro.json"))):
    sid=x["id"]; vel,pausa=humor(sid)
    frases=[f for f in re.split(r"(?<=[.!?:])\s+",x["t"].strip()) if f]
    parts=[]; sr=24000; marcas=[]; t=0.0
    for f in frases:
        a,sr=k.create(f,voice="pm_alex",speed=vel,lang="pt-br")
        parts.append(a.astype(np.float32)); marcas.append([f,round(t,3),round(t+len(a)/sr,3)]); t+=len(a)/sr
        p=pausa
        if len(f.split())<=4: p+=0.35 if sid in TRISTE else 0.15   # frases curtas e duras pedem silêncio
        if f.endswith("?"): p+=0.3
        parts.append(np.zeros(int(sr*p),dtype=np.float32)); t+=int(sr*p)/sr
    audio=np.concatenate(parts[:-1])
    sf.write(os.path.join(OUT,f"{sid}.wav"),audio,sr)
    json.dump(marcas,open(os.path.join(OUT,f"{sid}.json"),"w"),ensure_ascii=False)
    print(sid, round(len(audio)/sr,1), flush=True)
