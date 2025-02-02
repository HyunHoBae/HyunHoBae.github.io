---
title : Python으로 outlook 메일 보내기
date: YYYY-MM-DD HH:MM:SS +09:00
author: 배현호
layout: post
categories: ["python"]
tags: ["win32com"]
---
## 사용 이유 
SM 업무 중인 프로젝트에 점점 관리 체계가 도입 되면서 
주기적으로 이상 데이터가 없는지 쿼리를 통해 확인해봐야하는 일이 생겨났고 
매번 치기 귀찮으니 윈도우 작업 스케쥴러를 돌려서 자동으로 쿼리를 수행하고 결과를 매일로 보냄 

outlook 없이 네이버나 구글 이메일을 통해 보내려면 pop3/smtp 를 허용 해야하는데 
보안적으로 약해서 혹시 몰라 그냥 연동되어 있는 outlook을 사용

## 코드
이렇게 만든 후 실제 스케쥴러로 돌리는 코드에서 import하여 사용
<figure class="highlight">
<pre>
<code>

    import win32com.client
    
    def send_mail(to,subject,content, atch=[],cc=[]):
        # Outlook 실행 및 연결
        new_Mail = win32com.client.Dispatch("Outlook.Application").CreateItem(0)
        # 메일 수신자 리스트
        new_Mail.To = ";".join(to)
        # 메일 참조 리스트
        if cc:
            new_Mail.CC = "mail-add-for-cc@testadd.com"    
        # 메일 제목
        new_Mail.Subject = subject
        # 메일 내용
        new_Mail.HTMLBody = content
        # 첨부파일 추가
        if atch:
            for file in atch:
                new_Mail.Attachments.Add(file)
        # 메일 발송
        new_Mail.Send()

</code>
</pre>
</figure>
