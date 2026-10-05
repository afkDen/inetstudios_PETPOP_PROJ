#!/usr/bin/env python3
"""Search Openverse for reference/discovery. Verify every item's source license before production use."""
import argparse, json, urllib.parse, urllib.request
BASE='https://api.openverse.org/v1'
UA='PortableRobloxDevSystem/1.0'

def search(media, q, page_size):
    params={'q':q,'page_size':page_size}
    url=f'{BASE}/{media}/?'+urllib.parse.urlencode(params)
    req=urllib.request.Request(url, headers={'User-Agent':UA})
    with urllib.request.urlopen(req, timeout=30) as r: data=json.load(r)
    out=[]
    for x in data.get('results',[]):
        out.append({k:x.get(k) for k in ('id','title','creator','creator_url','license','license_version','license_url','source','foreign_landing_url','url','thumbnail')})
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('query')
    ap.add_argument('--media', choices=['images','audio'], default='images')
    ap.add_argument('--limit', type=int, default=20)
    args=ap.parse_args()
    print(json.dumps(search(args.media,args.query,max(1,min(50,args.limit))), indent=2, ensure_ascii=False))
    print('\nWARNING: Openverse license metadata must be verified at the original source before production use.', file=__import__('sys').stderr)
if __name__=='__main__': main()
