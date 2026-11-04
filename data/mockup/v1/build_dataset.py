"""Build synthetic CIP input bundles and isolated ground truth.

Requires extract-msg==0.58.1. Does not call Jira/Confluence or send email.
"""
from pathlib import Path
import json
import struct
from datetime import datetime, timezone
import hashlib
from collections import Counter
from html import escape

import extract_msg
from extract_msg import OleWriter

ROOT = Path(__file__).resolve().parent
state = json.loads((ROOT/'remote-resources.json').read_text())
cases = state['cases']
first_ticket = cases[0]['jira']['key']
date = datetime(2026, 11, 3, 8, 0, tzinfo=timezone.utc)
filetime = int((date.timestamp() + 11644473600) * 10_000_000)

def write_message(path, subject, body, sender_name, sender_email):
    writer = OleWriter()
    root_properties = []

    # MS-OXMSG 2.3 requires one named-property mapping storage, even when no
    # named properties are used. Its three mapping streams are then empty.
    writer.addEntry('__nameid_version1.0', storage=True)
    for mapping_stream in ('00020102', '00030102', '00040102'):
        writer.addEntry('__nameid_version1.0/__substg1.0_' + mapping_stream, b'')

    def fixed(tag, value, dest, props):
        props.append(struct.pack('<II', tag, 6) + value.ljust(8,b'\x00'))

    def string(prop_id, value, dest, props):
        data = value.encode('utf-16-le')
        writer.addEntry(dest+f'__substg1.0_{prop_id:04X}001F',data)
        props.append(struct.pack('<IIII',(prop_id<<16)|0x001F,6,len(data)+2,0))

    for pid,value in [(0x001A,'IPM.Note'),(0x0037,subject),(0x1000,body),
                      (0x0C1A,sender_name),(0x0C1E,'SMTP'),(0x0C1F,sender_email),
                      (0x5D01,sender_email),(0x0042,sender_name),(0x0065,sender_email),
                      (0x0E04,'Demo Reviewer'),(0x007D,f'From: {sender_name} <{sender_email}>\r\nTo: Demo Reviewer <reviewer@example.test>\r\nSubject: {subject}\r\nDate: Tue, 03 Nov 2026 08:00:00 +0000\r\nX-CIP-Mockup: cip-mock-v1\r\n')]:
        string(pid,value,'',root_properties)
    fixed(0x0E070003,struct.pack('<I',1),'',root_properties)
    # MS-OXMSG 2.1.3: all our 001F strings are Unicode. Without this flag,
    # strict clients must treat the file as non-Unicode.
    fixed(0x340D0003,struct.pack('<I',0x00040000),'',root_properties)
    fixed(0x0FFE0003,struct.pack('<I',5),'',root_properties)
    fixed(0x3FDE0003,struct.pack('<I',65001),'',root_properties)
    fixed(0x0E060040,struct.pack('<Q',filetime),'',root_properties)
    recipient='__recip_version1.0_#00000000/'
    recipient_props=[]
    writer.addEntry(recipient.rstrip('/'),storage=True)
    for pid,value in [(0x3001,'Demo Reviewer'),(0x3002,'SMTP'),(0x3003,'reviewer@example.test'),(0x39FE,'reviewer@example.test')]:
        string(pid,value,recipient,recipient_props)
    fixed(0x0C150003,struct.pack('<I',1),recipient,recipient_props)
    fixed(0x0FFE0003,struct.pack('<I',6),recipient,recipient_props)
    writer.addEntry(recipient+'__properties_version1.0',bytes(8)+b''.join(recipient_props))
    header=bytes(8)+struct.pack('<IIII',1,0,1,0)+bytes(8)
    writer.addEntry('__properties_version1.0',header+b''.join(root_properties))
    writer.write(str(path))

rules=[
    ('MC-01','Ticket Jira','Mục Ticket Jira có giá trị.'),
    ('MC-02','Service','Mục Service có giá trị.'),
    ('MC-03','Type','Mục Type có giá trị trong danh mục mockup Normal/Standard/Emergency.'),
    ('MC-04','Risk','Mục Risk có nội dung, không chỉ là khoảng trắng.'),
    ('MC-05','BO sign-off','Có tệp .msg BO sign-off đúng tên được MC tham chiếu.'),
    ('MC-06','Request','Có tệp .msg Request đúng tên được MC tham chiếu.'),
    ('FMT-01','Ticket Jira','Ticket Jira là URL HTTP(S), host Jira của sandbox và path /browse/KEY hợp lệ.'),
    ('READ-01','BO sign-off','Đọc được subject, sender, recipient và body của .msg BO sign-off.'),
    ('READ-02','Request','Đọc được subject, sender, recipient và body của .msg Request.'),
    ('MATCH-01','Service','Service trong hai email đọc được khớp chính xác Service trong MC.'),
    ('MATCH-02','Ticket Jira','Ticket trong hai email đọc được khớp ticket được MC tham chiếu.')
]
(ROOT/'checklist.json').write_text(json.dumps({'version':'cip-mock-v1','approval':'proposed-not-mentor-approved','scope':'Mockup only; completeness is not authorization to approve.','aggregation':'fail if any criterion fails; otherwise needs_review if any criterion needs review; otherwise pass.','missing_dependency':'Dependent checks are needs_review when source field/file is missing, unreadable or invalid.','criteria':[{'criterion_id':i,'field':f,'description':d} for i,f,d in rules]},ensure_ascii=False,indent=2))

validation=[]
manifest=[]
for c in cases:
    cid=c['case_id'];v=c['variant'];directory=ROOT/c['split']/cid
    directory.mkdir(parents=True,exist_ok=True)
    (directory/'mc.html').write_text('<!doctype html><html lang="vi"><meta charset="utf-8"><title>'+cid+'</title><body>'+c['mc_html']+'</body></html>')
    files=[]
    evidence_data={}
    for kind in ('bo','request'):
        name=c['email_files'][kind]
        if (kind=='bo' and v=='missing_bo') or (kind=='request' and v=='missing_request'):
            evidence_data[kind]={'filename':name,'present':False}
            continue
        path=directory/name
        if (kind=='bo' and v=='corrupt_bo') or (kind=='request' and v=='corrupt_request'):
            path.write_bytes(bytes.fromhex('D0CF11E0A1B11AE1')+b'CIP SYNTHETIC TRUNCATED CFB FIXTURE\x00')
            failed=False
            try:
                with extract_msg.openMsg(str(path)) as message:
                    _=message.body
            except Exception:
                failed=True
            if not failed:raise AssertionError('Corrupt fixture unexpectedly parsed: '+cid)
            validation.append({'case_id':cid,'file':name,'expected':'unreadable','verified':True})
            files.append({'filename':name,'size':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'format':'intentionally-truncated-msg'})
            evidence_data[kind]={'filename':name,'present':True,'readable':False}
            continue
        service='Demo Alternate Service' if v=='mismatch_service' and kind=='request' else c['service']
        key=first_ticket if v=='mismatch_ticket' and kind=='bo' else c['jira']['key']
        purpose='BO sign-off giả lập' if kind=='bo' else 'Yêu cầu thay đổi giả lập'
        subject=f'[MOCKUP][{cid}] {purpose} — {service}'
        sender_name='Demo Business Owner' if kind=='bo' else 'Demo Requester'
        sender_email='bo@example.test' if kind=='bo' else 'requester@example.test'
        content=(f'DỮ LIỆU GIẢ LẬP — KHÔNG PHẢI EMAIL THẬT.\r\n'
                 f'Case ID: {cid}\r\nTicket: {key}\r\nService: {service}\r\nType: {c["type"]}\r\nRelease: {c["release"]}\r\n'
                 f'Nội dung: '+('Tôi xác nhận BO sign-off giả lập cho thay đổi cấu hình nêu trên.' if kind=='bo' else 'Đề nghị chuẩn bị hồ sơ CIP cho thay đổi cấu hình nêu trên.')+'\r\n'
                 f'Risk: {c["risk"]}\r\n'
                 'Thông điệp này chỉ là bằng chứng mẫu để kiểm chứng parser và quy tắc, không có giá trị phê duyệt thực tế.\r\n')
        write_message(path,subject,content,sender_name,sender_email)
        with extract_msg.openMsg(str(path)) as message:
            assert message.subject==subject,(cid,'subject',message.subject)
            assert sender_email in message.sender,(cid,'sender',message.sender)
            assert 'reviewer@example.test' in message.to,(cid,'recipient',message.to)
            assert message.body.replace('\r\n','\n')==content.replace('\r\n','\n'),(cid,'body')
        validation.append({'case_id':cid,'file':name,'expected':'readable-msg','verified':True})
        files.append({'filename':name,'size':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'format':'outlook-msg-unicode'})
        evidence_data[kind]={'filename':name,'present':True,'readable':True,'subject':subject,'sender':sender_email,'recipient':'reviewer@example.test','service':service,'ticket':key,'body':content}

    results={rule[0]:{'criterion_id':rule[0],'status':'pass','source':rule[1]} for rule in rules}
    def mark(rule,status,reason):results[rule].update(status=status,reason=reason)
    if v=='missing_ticket':
        mark('MC-01','fail','Không có mục Ticket Jira trong MC.')
        mark('FMT-01','needs_review','Không có Ticket Jira để kiểm tra định dạng.')
        mark('MATCH-02','needs_review','Không có Ticket Jira trong MC để đối chiếu.')
    if v=='missing_service':
        mark('MC-02','fail','Không có mục Service trong MC.')
        mark('MATCH-01','needs_review','Không có Service trong MC để đối chiếu.')
    if v=='blank_type':mark('MC-03','fail','Type có mục nhưng giá trị trống.')
    if v=='blank_risk':mark('MC-04','fail','Risk chỉ chứa khoảng trắng.')
    if v in ('missing_bo','missing_request'):
        mark('MC-05' if v=='missing_bo' else 'MC-06','fail','Tệp được MC tham chiếu không tồn tại trong gói và không đính kèm trang.')
        mark('READ-01' if v=='missing_bo' else 'READ-02','needs_review','Thiếu tệp để đọc.')
        for rule in ('MATCH-01','MATCH-02'):mark(rule,'needs_review','Thiếu một trong hai email để đối chiếu đầy đủ.')
    if v=='bad_url':
        mark('FMT-01','fail','Ticket Jira sử dụng scheme jira-invalid thay vì HTTP(S).')
        mark('MATCH-02','needs_review','Ticket Jira trong MC không phải URL hợp lệ để xác định ticket đối chiếu.')
    if v in ('corrupt_bo','corrupt_request'):
        mark('READ-01' if v=='corrupt_bo' else 'READ-02','needs_review','Tệp .msg bị cắt cụt có chủ đích; không đủ dữ liệu để đọc.')
        for rule in ('MATCH-01','MATCH-02'):mark(rule,'needs_review','Một email không đọc được, chưa đủ căn cứ đối chiếu.')
    if v=='mismatch_service':mark('MATCH-01','fail','Request ghi Demo Alternate Service, khác Service trong MC.')
    if v=='mismatch_ticket':mark('MATCH-02','fail',f'BO sign-off ghi {first_ticket}, khác {c["jira"]["key"]} trong MC.')
    statuses=[x['status'] for x in results.values()]
    overall='fail' if 'fail' in statuses else 'needs_review' if 'needs_review' in statuses else 'pass'
    oracle={'case_id':cid,'split':c['split'],'group':c['group'],'variant':v,'checklist_version':'cip-mock-v1','overall_expected':overall,'criteria':list(results.values()),'evidence':evidence_data,'email_constraints':{'may_state_complete':overall=='pass','must_surface':[x['criterion_id'] for x in results.values() if x['status']!='pass'],'must_not_invent':['employee_grade','approver','recipient','approval_status','missing_values'],'note':'Sender/recipient strings in source emails do not establish employee grades or authority.'}}
    (ROOT/'ground_truth'/f'{cid}.json').write_text(json.dumps(oracle,ensure_ascii=False,indent=2))
    input_manifest={'case_id':cid,'dataset_version':'cip-mock-v1','mc_file':'mc.html','email_files':[f['filename'] for f in files]}
    (directory/'manifest.json').write_text(json.dumps(input_manifest,ensure_ascii=False,indent=2))
    manifest.append({'case_id':cid,'split':c['split'],'group':c['group'],'variant':v,'jira':c['jira'],'confluence':c['confluence'],'input_dir':str(directory.relative_to(ROOT)),'ground_truth':f'ground_truth/{cid}.json','files':files,'overall_expected':overall})

(ROOT/'manifest.json').write_text(json.dumps({'dataset_version':'cip-mock-v1','provenance':'synthetic-only','root_page_id':state['root_page_id'],'cases':manifest},ensure_ascii=False,indent=2))
report={'dataset_version':'cip-mock-v1','file_reader':'extract-msg 0.58.1','mock_cases':len(cases),'valid_msg_files':sum(x['expected']=='readable-msg' for x in validation),'intentionally_corrupt_msg_files':sum(x['expected']=='unreadable' for x in validation),'intentionally_missing_files':48-len(validation),'all_email_fixture_checks_passed':all(x['verified'] for x in validation),'expected_case_counts':dict(Counter(c['overall_expected'] for c in manifest)),'checks':validation}
(ROOT/'validation-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='checks'},ensure_ascii=False,indent=2))
