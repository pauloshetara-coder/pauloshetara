"""Narração com voz neural (Microsoft Edge TTS, pt-BR-AntonioNeural), frase a frase,
mais lenta, grave e com pausas maiores nas cenas tristes. Gera assets/voz/sNN.wav + sNN.json (marcas)."""
import asyncio, json, os, re, ssl, subprocess, tempfile
import numpy as np, soundfile as sf, edge_tts, edge_tts.communicate as c
c._SSL_CTX = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE", "/root/.ccr/ca-bundle.crt"))
BASE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(BASE, "..", "elesbao-hf", "assets", "voz")
VOZ = "pt-BR-AntonioNeural"; SR = 24000
TRISTE = {"s01","s04","s09","s11","s13","s14","s15","s17","s19"}
SOLENE = {"s02","s08","s16","s18","s20"}
def humor(sid):
    if sid in TRISTE: return "-14%", "-6Hz", 0.8
    if sid in SOLENE: return "-9%", "-3Hz", 0.55
    return "-5%", "-2Hz", 0.4
async def tts(texto, rate, pitch, tries=4):
    for i in range(tries):
        try:
            tmp = tempfile.mktemp(suffix=".mp3")
            await edge_tts.Communicate(texto, VOZ, rate=rate, pitch=pitch, proxy=os.environ.get("HTTPS_PROXY")).save(tmp)
            pcm = subprocess.check_output(["ffmpeg","-v","error","-i",tmp,"-ac","1","-ar",str(SR),"-f","f32le","-"])
            os.remove(tmp); return np.frombuffer(pcm, dtype=np.float32)
        except Exception as e:
            print("retry", e, flush=True); await asyncio.sleep(3*(i+1))
    raise SystemExit("falhou: "+texto)
def apara(a, lim=0.01):
    idx = np.where(np.abs(a) > lim)[0]
    return a[max(0, idx[0]-240): idx[-1]+2400] if len(idx) else a
async def main():
    import sys
    so = sys.argv[1].split(",") if len(sys.argv) > 1 else None
    for x in json.load(open(os.path.join(BASE, "roteiro.json"))):
        sid = x["id"]
        if so and sid not in so: continue
        rate, pitch, pausa = humor(sid)
        frases = [f for f in re.split(r"(?<=[.!?:])\s+", x["t"].strip()) if f]
        parts, marcas, t = [], [], 0.0
        for f in frases:
            for _ in range(5):
                a = apara(await tts(f, rate, pitch))
                if len(a)/SR >= 0.27*len(f.split()): break
                print("curta, refazendo:", f[:40], round(len(a)/SR,2), flush=True)
            parts.append(a); marcas.append([f, round(t,3), round(t+len(a)/SR,3)]); t += len(a)/SR
            p = pausa
            if len(f.split()) <= 4: p += 0.35 if sid in TRISTE else 0.15
            if f.endswith("?"): p += 0.3
            parts.append(np.zeros(int(SR*p), dtype=np.float32)); t += int(SR*p)/SR
        audio = np.concatenate(parts[:-1])
        sf.write(os.path.join(OUT, f"{sid}.wav"), audio, SR)
        json.dump(marcas, open(os.path.join(OUT, f"{sid}.json"), "w"), ensure_ascii=False)
        print(sid, round(len(audio)/SR, 1), flush=True)
asyncio.run(main())
