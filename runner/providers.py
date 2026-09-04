import os, json, time, urllib.request, subprocess

def call_agy(prompt, model=None, timeout='360s'):
    model = model or os.getenv('CDE_MODEL', 'gemini-3.6-flash-high')
    t=time.time()
    p=subprocess.run(['agy','--model',model,f'--print={prompt}',f'--print-timeout={timeout}'],capture_output=True,text=True,timeout=390)
    if p.returncode: raise RuntimeError(p.stderr.strip() or p.stdout.strip() or f'agy exit {p.returncode}')
    return {'text':p.stdout.strip(),'usage':{},'latency_s':time.time()-t,'model':model}

def call_api(prompt, system='', config=None):
    config=config or {}; base=os.getenv('CDE_API_BASE',config.get('api_base','')).rstrip('/')
    key=os.getenv('CDE_API_KEY',''); model=os.getenv('CDE_MODEL',config.get('model',''))
    if not base or not key or not model: raise RuntimeError('API mode needs CDE_API_BASE, CDE_API_KEY, CDE_MODEL')
    body={'model':model,'temperature':float(config.get('temperature',0)),'max_tokens':int(config.get('max_tokens',1800)),'messages':[{'role':'system','content':system},{'role':'user','content':prompt}]}
    req=urllib.request.Request(base+'/chat/completions',data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
    t=time.time()
    with urllib.request.urlopen(req,timeout=180) as r: data=json.load(r)
    text=data['choices'][0]['message']['content']; usage=data.get('usage',{})
    return {'text':text,'usage':usage,'latency_s':time.time()-t,'model':model}
