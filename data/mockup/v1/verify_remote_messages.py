"""Verify downloaded Confluence MSG bytes and expose their decoded content.

Usage: python verify_remote_messages.py /tmp/tasks.json
tasks.json contains short-lived download URLs; never store it in the repo.
Requires extract-msg==0.58.1. This is not an Outlook compatibility test.
"""
import concurrent.futures
import hashlib
import html
import json
import os
from pathlib import Path
import struct
import sys
import urllib.request

import extract_msg
import olefile

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
OUT=REPO/'output/msg-validation'
OUT.mkdir(parents=True,exist_ok=True)
TEMP=Path('/tmp/cip-remote-msg-audit')
TEMP.mkdir(exist_ok=True)
task_file=Path(sys.argv[1])
os.chmod(task_file,0o600)
tasks=json.loads(task_file.read_text())
manifest=json.loads((ROOT/'manifest.json').read_text())
lookup={f['filename']:(c,ROOT/c['input_dir']/f['filename']) for c in manifest['cases'] for f in c['files'] if f['format']=='outlook-msg-unicode'}

def normalize(s):return s.replace('\r\n','\n')

def inspect(task):
    name=task['name'];case,local=lookup[name]
    oracle=json.loads((ROOT/case['ground_truth']).read_text())
    expected=next(e for e in oracle['evidence'].values() if e.get('filename')==name)
    with urllib.request.urlopen(task['url'],timeout=45) as response:
        downloaded=response.read()
    path=TEMP/name;path.write_bytes(downloaded)
    digest=hashlib.sha256(downloaded).hexdigest()
    checks={
        'download_succeeded':True,
        'sha256_matches_local':digest==hashlib.sha256(local.read_bytes()).hexdigest(),
    }
    with extract_msg.openMsg(str(path)) as msg:
        subject=msg.subject;sender=msg.sender;recipient=msg.to;body=msg.body
    checks.update(
        parser_opened=True,
        subject_matches=subject==expected['subject'],
        sender_matches=expected['sender'] in sender,
        recipient_matches=expected['recipient'] in recipient,
        body_matches=normalize(body)==normalize(expected['body']),
    )
    with olefile.OleFileIO(path) as ole:
        checks['message_root_clsid']=ole.root.clsid=='00020D0B-0000-0000-C000-000000000046'
        checks['nameid_storage_and_streams']=all(ole.exists('__nameid_version1.0/__substg1.0_'+s) for s in ('00020102','00030102','00040102'))
        props=ole.openstream('__properties_version1.0').read()
        checks['property_record_alignment']=len(props)>=32 and (len(props)-32)%16==0
        entries={struct.unpack('<I',props[i:i+4])[0]:props[i+8:i+16] for i in range(32,len(props),16)}
        checks['unicode_support_flag']=bool(struct.unpack('<I',entries[0x340D0003][:4])[0]&0x40000)
        checks['recipient_and_attachment_counts']=struct.unpack('<IIII',props[8:24])==(1,0,1,0)
        string_sizes_ok=True
        direct_values={}
        for tag,value in entries.items():
            if tag&0xffff==0x1f:
                stream=ole.openstream(f'__substg1.0_{tag:08X}').read()
                string_sizes_ok &= bool(stream) and len(stream)%2==0 and struct.unpack('<I',value[:4])[0]==len(stream)+2
                direct_values[tag]=stream.decode('utf-16-le')
        checks['unicode_string_sizes']=string_sizes_ok
        checks['direct_stream_subject_matches']=direct_values[0x0037001F]==expected['subject']
        checks['direct_stream_body_matches']=normalize(direct_values[0x1000001F])==normalize(expected['body'])
    decoded={'subject':subject,'sender':sender,'recipient':recipient,'body':body}
    preview_name=Path(name).stem+'.html'
    preview=f'''<!doctype html><html lang="vi"><meta charset="utf-8"><title>{html.escape(name)}</title><style>body{{font-family:Arial,sans-serif;max-width:900px;margin:40px auto;line-height:1.6;padding:0 24px;color:#18344b}}pre{{white-space:pre-wrap;background:#f1f6f8;padding:20px;border-left:4px solid #087f8c}}code{{overflow-wrap:anywhere}}</style><h1>{html.escape(name)}</h1><p>Nội dung dưới đây được đọc trực tiếp từ tệp .msg tải lại từ Confluence.</p><p><b>From:</b> {html.escape(sender)}<br><b>To:</b> {html.escape(recipient)}<br><b>Subject:</b> {html.escape(subject)}</p><pre>{html.escape(body)}</pre><p>SHA-256 của tệp tải xuống: <code>{digest}</code></p><p>Chưa kiểm chứng mở bằng Outlook.</p></html>'''
    (OUT/preview_name).write_text(preview)
    return {'case_id':case['case_id'],'filename':name,'attachment_id':task['id'],'page_id':task['pageId'],'bytes':len(downloaded),'sha256':digest,'checks':checks,'automated_checks_passed':all(checks.values()),'outlook_open_test':'not_performed','decoded':decoded,'preview':preview_name}

results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    futures={executor.submit(inspect,t):t for t in tasks}
    for future in concurrent.futures.as_completed(futures):
        task=futures[future]
        try:
            result=future.result();results.append(result)
            print(('verified' if result['automated_checks_passed'] else 'mismatch'),task['name'],flush=True)
        except Exception as error:
            results.append({'filename':task['name'],'automated_checks_passed':False,'error':type(error).__name__+': '+str(error),'outlook_open_test':'not_performed'})
            print('failed',task['name'],type(error).__name__,flush=True)
results.sort(key=lambda r:r['filename'])
report={'scope':'42 expected-readable files; excludes two deliberately corrupt fixtures and four missing fixtures.','msg_revision':'msg-fix-1','file_reader':'extract-msg 0.58.1 and direct OLE stream checks','downloaded_files':len(results),'automated_passed':sum(r['automated_checks_passed'] for r in results),'outlook_compatibility':'UNVERIFIED: Outlook was not available and was not used.','checks_do_not_prove_full_ms_oxmsg_conformance':True,'files':results}
(ROOT/'remote-msg-validation-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
rows=''.join('<tr><td><a href="'+r.get('preview','#')+'">'+html.escape(r['filename'])+'</a></td><td>'+('PASS' if r['automated_checks_passed'] else 'FAIL')+'</td><td><code>'+r.get('sha256','')+'</code></td></tr>' for r in results)
summary=f'''<!doctype html><html lang="vi"><meta charset="utf-8"><title>Kiểm chứng MSG tải từ Confluence</title><style>body{{font-family:Arial,sans-serif;max-width:1150px;margin:40px auto;padding:0 20px;line-height:1.5;color:#18344b}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #d8e3e9;padding:10px;text-align:left}}th{{background:#18344b;color:white}}code{{font-size:11px;overflow-wrap:anywhere}}.note{{padding:18px;background:#fff0b3}}</style><h1>Kiểm chứng tệp MSG trên Confluence</h1><p>Tải lại và kiểm tra {len(results)} tệp; {report['automated_passed']} tệp vượt qua toàn bộ kiểm tra tự động.</p><p class="note"><b>Chưa kiểm chứng bằng Outlook.</b> Các kiểm tra này xác nhận bản tải xuống khớp dữ liệu cục bộ, đọc đúng thông tin kỳ vọng và đáp ứng các điều kiện cấu trúc đã kiểm tra. Chúng chưa chứng minh khả năng mở bằng mọi ứng dụng.</p><p>Bấm tên tệp để xem nội dung được giải mã trực tiếp từ bản tải xuống. Hai tệp hỏng và bốn tệp thiếu chủ đích không thuộc phép kiểm tra này.</p><table><tr><th>Tệp</th><th>Kiểm tra tự động</th><th>SHA-256 bản tải xuống</th></tr>{rows}</table></html>'''
(OUT/'index.html').write_text(summary)
print(json.dumps({'downloaded':len(results),'automated_passed':report['automated_passed'],'outlook_compatibility':'unverified','report':str(ROOT/'remote-msg-validation-report.json'),'readable_report':str(OUT/'index.html')},ensure_ascii=False),flush=True)
if report['automated_passed']!=42:raise SystemExit(1)
