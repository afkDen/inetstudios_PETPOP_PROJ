#!/usr/bin/env python3
"""Search Poly Haven's free public API using only Python stdlib."""
import argparse, json, urllib.parse, urllib.request
BASE='https://api.polyhaven.com'
UA='PortableRobloxDevSystem/1.0 (asset provenance client)'

def get(path, params=None):
    url=BASE+path
    if params: url += '?' + urllib.parse.urlencode(params)
    req=urllib.request.Request(url, headers={'User-Agent':UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('query', nargs='?', default='')
    ap.add_argument('--type', choices=['all','models','textures','hdris'], default='all')
    ap.add_argument('--limit', type=int, default=20)
    args=ap.parse_args()
    if args.query:
        slugs=get('/search', {'q':args.query, **({} if args.type=='all' else {'type':args.type})})
        if isinstance(slugs, dict): slugs=list(slugs)
        slugs=list(slugs)[:max(1,args.limit)]
        assets=get('/assets', {} if args.type=='all' else {'type':args.type})
        out=[]
        for slug in slugs:
            meta=assets.get(slug, {}) if isinstance(assets, dict) else {}
            out.append({'id':slug, 'name':meta.get('name'), 'type':meta.get('type'), 'category':meta.get('category'), 'tags':meta.get('tags'), 'source_url':f'https://polyhaven.com/a/{slug}', 'license':'CC0'})
    else:
        assets=get('/assets', {} if args.type=='all' else {'type':args.type})
        out=[]
        for slug,meta in list(assets.items())[:max(1,args.limit)]:
            out.append({'id':slug, 'name':meta.get('name'), 'type':meta.get('type'), 'category':meta.get('category'), 'tags':meta.get('tags'), 'source_url':f'https://polyhaven.com/a/{slug}', 'license':'CC0'})
    print(json.dumps(out, indent=2, ensure_ascii=False))
if __name__=='__main__': main()
