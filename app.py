import json, requests, urllib3, jwt as jwtLib, time
from flask import Flask, request, jsonify, send_from_directory
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from datetime import datetime
import MajorLoginRes_pb2 as mLrPb
urllib3.disable_warnings()
app = Flask(__name__, static_folder='.')
AeSkEy = b'Yg&tc%DEuh6%Zc^8'
AeSiV  = b'6oyZDr22E3ychjM%'
mLuRl = "https://loginbp.ggpolarbear.com/MajorLogin"
bNuRl = "https://100067.connect.garena.com/bind/app/platform/info/get"
bIdUr = "https://clientbp.ggpolarbear.com/BindDelete"
iNuRl = "https://100067.connect.garena.com/oauth/token/inspect?token={t}"
mLhDr = {
    "User-Agent":      "Dalvik/2.1.0 (Linux; U; Android 11; SM-S908E Build/TP1A.220624.014)",
    "Connection":      "Keep-Alive",
    "Accept-Encoding": "gzip",
    "Content-Type":    "application/octet-stream",
    "Expect":          "100-continue",
    "X-GA":            "v1 1",
    "X-Unity-Version": "2018.4.11f1",
    "ReleaseVersion":  "OB52",
}
iNhDr = {
    "Accept-Encoding": "gzip, deflate, br",
    "Connection":      "close",
    "Content-Type":    "application/x-www-form-urlencoded",
    "Host":            "100067.connect.garena.com",
    "User-Agent":      "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;US;)",
}
bIdHd = {
    "User-Agent":      "Free%20Fire/2019119620 CFNetwork/1335.0.3.4 Darwin/21.6.0",
    "X-GA":            "v1 1",
    "X-Unity-Version": "2018.4.11f1",
    "ReleaseVersion":  "OB52",
    "Content-Type":    "application/octet-stream",
    "Accept":          "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection":      "keep-alive",
    "Host":            "clientbp.ggpolarbear.com",
}
def encA(d): return AES.new(AeSkEy, AES.MODE_CBC, AeSiV).encrypt(pad(d, 16))
def decA(d): return unpad(AES.new(AeSkEy, AES.MODE_CBC, AeSiV).decrypt(d), 16)
def encP(d, k, v): return AES.new(k, AES.MODE_CBC, v).encrypt(pad(d, 16))
def eVr(n):
    r = []
    while True:
        b = n & 0x7F; n >>= 7
        if n: b |= 0x80
        r.append(b)
        if not n: break
    return bytes(r)
def _s(f, v):
    ev = v.encode() if isinstance(v, str) else v
    return eVr((f << 3) | 2) + eVr(len(ev)) + ev
def _i(f, v):
    return eVr((f << 3) | 0) + eVr(v)
def bUiLd(oId, tok, plat):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    p  = str(plat)
    pl = (
        _s(1,  ts) +
        _s(4,  "free fire") +
        _i(5,  1) +
        _s(7,  "1.120.1") +
        _s(8,  "Android OS 12 / API-31 (SP1A.210812.016/T505NDXS6CXB1)") +
        _s(9,  "Handheld") +
        _s(10, "we") +
        _s(11, "WIFI") +
        _i(12, 1334) +
        _i(13, 800) +
        _s(14, "225") +
        _s(15, "ARM64 FP ASIMD AES | 4032 | 8") +
        _i(16, 2705) +
        _s(17, "Adreno (TM) 610") +
        _s(18, "OpenGL ES 3.2 V@0502.0 (GIT@5eaa426211, I07ee46fc66, 1633700387) (Date:10/08/21)") +
        _s(19, "Google|dbc5b426-9715-454a-9466-6c82e151d407") +
        _s(20, "154.183.6.12") +
        _s(21, "ar") +
        _s(22, oId) +
        _s(23, p) +
        _s(24, "Handheld") +
        _s(25, "samsung SM-T505N") +
        _s(29, tok) +
        _i(30, 1) +
        _s(41, "we") +
        _s(42, "WIFI") +
        _s(57, "e89b158e4bcf988ebd09eb83f5378e87") +
        _i(60, 22394) +
        _i(61, 1424) +
        _i(62, 3349) +
        _i(63, 24) +
        _i(64, 1552) +
        _i(65, 22394) +
        _i(66, 1552) +
        _i(67, 22394) +
        _i(73, 1) +
        _s(74, "/data/app/~~GAY==/com.dts.zbiiiiiiiiiiiiiiiiiiiio==/arm64") +
        _i(76, 2) +
        _s(77, "b4d2689433917e66100ba91db790bf37|/data/app/~~GAY==/com.dts.zbiiiiiiiiiiiiiiiiiiiio==/zbi.apk") +
        _i(78, 2) +
        _i(79, 2) +
        _s(81, "64") +
        _s(83, "2019115296") +
        _i(85, 1) +
        _s(86, "OpenGLES3") +
        _i(87, 16383) +
        _i(88, 4) +
        _s(89, "Damanhur") +
        _s(90, "BH") +
        _i(91, 31095) +
        _s(92, "android_max") +
        _s(94, "KqsHTzpfADfqKnEg/KMctJLElsm8bN2M4ts0zq+ifY+560USyjMSDL386RFrwRloT0ZSbMxEuM+Y4FSvjghQQZXWWpY=") +
        _i(95, 1) +
        _i(97, 1) +
        _s(99,  p) +
        _s(100, p) +
        _s(102, (8 << 3 | 2).to_bytes(1, 'little') + b'\x03GAW')
    )
    return encA(pl)
def gLogin(aT):
    r    = requests.get(iNuRl.format(t=aT), headers=iNhDr, timeout=10).json()
    print(f"[inspect] {r}")
    if 'error' in r: raise Exception(f"inspect: {r.get('error')}")
    oId  = r['open_id']
    plat = r.get('platform', 8)
    pl   = bUiLd(oId, aT, plat)
    x    = requests.post(mLuRl, headers=mLhDr, data=pl, timeout=15, verify=False)
    print(f"[MajorLogin] {x.status_code} {x.text[:120]}")
    if not x.ok: raise Exception(f"MajorLogin {x.status_code}: {x.text[:100]}")
    res = mLrPb.MajorLoginRes()
    try:    res.ParseFromString(decA(x.content))
    except: res.ParseFromString(x.content)
    if not res.token: raise Exception("empty jwt")
    cl   = jwtLib.decode(res.token, options={"verify_signature": False})
    aId  = cl.get('account_id', res.account_id)
    nick = cl.get('nickname', '')
    return res.token, res.ak, res.aiv, aId, nick, oId
@app.route('/')
def idx(): return send_from_directory('.', 'index.html')
@app.route('/api/check')
def chk():
    aT = request.args.get('token', '').strip()
    if not aT: return jsonify({"error": "missing token"}), 400
    try:
        tok, k, iv, aId, nick, oId = gLogin(aT)
        r = requests.get(bNuRl, params={"access_token": aT},
            headers={"User-Agent":"GarenaMSDK/4.0.19P9(Redmi Note 5 ;Android 9;en;US;)",
                     "Connection":"Keep-Alive","Accept-Encoding":"gzip"}, timeout=10)
        print(f"[check] {r.status_code} {r.text[:200]}")
        d = r.json()
        if isinstance(d, dict) and 'data' in d: d = d['data']
        if isinstance(d, dict):
            d['account_id'] = str(aId)
            d['nickname']   = nick
        return app.response_class(response=json.dumps(d, ensure_ascii=False), mimetype='application/json')
    except Exception as e:
        print(f"[check err] {e}")
        return jsonify({"error": str(e)}), 500
@app.route('/api/unbind', methods=['POST'])
def unBind():
    d   = request.get_json()
    aT  = (d or {}).get('token', '').strip()
    plt = (d or {}).get('platform')
    uid = str((d or {}).get('uid', ''))
    if not aT or plt is None: return jsonify({"error": "missing params"}), 400
    try:
        tok, k, iv, aId, nick, oId = gLogin(aT)
        pkt = _s(1, aT) + _s(2, str(int(plt))) + _s(3, uid)
        enc = encA(pkt)
        hd  = {**bIdHd, "Authorization": f"Bearer {tok}"}
        r   = requests.post(bIdUr, headers=hd, data=enc, verify=False, timeout=10)
        print(f"[unbind] {r.status_code} {r.content.hex()}")
        return jsonify({"success": r.status_code == 200, "status": r.status_code})
    except Exception as e:
        print(f"[unbind err] {e}")
        return jsonify({"error": str(e)}), 500
@app.route('/api/logout', methods=['POST'])
def lgOut():
    d  = request.get_json()
    aT = (d or {}).get('token', '').strip()
    if not aT: return jsonify({"error": "missing token"}), 400
    try:
        tok, k, iv, aId, nick, oId = gLogin(aT)
        pkt = _s(1, aT) + _s(2, "Android|00000000-0000-0000-0000-000000000000") + _s(3, "samsung SM-T505N")
        enc = encA(pkt)
        hd  = {**bIdHd, "Authorization": f"Bearer {tok}"}
        r1  = requests.post("https://clientbp.ggpolarbear.com/Logout", headers=hd, data=enc, verify=False, timeout=10)
        r2  = requests.get(f"https://100067.connect.garena.com/oauth/logout?access_token={aT}", headers=iNhDr, timeout=10)
        print(f"[logout] game={r1.status_code} garena={r2.status_code}")
        return jsonify({"success": True})
    except Exception as e:
        print(f"[logout err] {e}")
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
  
