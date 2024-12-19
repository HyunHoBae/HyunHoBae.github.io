---
title : 로그 파일 모니터링 shell script
date: YYYY-MM-DD HH:MM:SS +09:00
author: 배현호
layout: post
categories: ["shell"]
tags: ["shell script","log 모니터링"]
hide: true
---

## 목적 
에러 로그를 보관하는 파일을 모니터링하여 에러가 발생했을때 관리자 들이 금방 인지 할 수 있도록 하기 위함 

## 방법 
1. 어플리케이션에 에러 내용을 받으면 메일을 보내는 API를 생성 
2. shell script를 통해 에러 로그 파일을 모니터링 하며
3. 에러 로그가 생기면 변수에 담아 두었다가 5분 주기로 api 호출(주기를 주지 않으면 여러 줄이 쌓이는 로그의 경우 한번에 많은 양의 메일이 전송됨)

## 구현
shell 스크립트만 메모
<pre>
    <code>
#!/bin/bash        

echo "Error Log Monitoring Start"

#대상 파일
logFile="./err.log

#버퍼로 쓸 변수
buffer=""

#버퍼 라인 수
buffer=0

#전송 간격(초)
send_interval=300

#마지막 전송 시간
last_send_time=300

tail -f -n 0 "${logFile}"|\
    while true #에러 로그가 쌓이지 않아도 반복문은 돌고 있어야 재대로 전송이 되기에 true
    do 
        #라인이 비어있는 것이 아니면 buffer에 넣기 0.1초 대기
        read -t 0.1 line
        #로그가 쌓이지 않은 채로 돌았을 경우 무시
        if [[ -n "$line" ]] : then
            #에러 로그 저장
            buffer="${buffer}${line}"
            ((buffer_line++))
        fi
        #현재 시간 확인 
        current_time=$(date +%s)
        
        #조건에 따라 전송 - 전송 간격 초과 혹은 라인수 200 초과 
        if [[ $((current_time -last_send_time)) -ge $send_interval || $buffer_line -ge 200]]; then
            #buffer가 있을 경우만 전송
            if [[$ -n "$buffer" ]]; then
                json_payload=$(jq -n --arg buffer "$buffer" '{"errorData":$buffer}')4
                curl -d "$json_payload" -H "content-Type: application/json" -X POST 처리 API 주소 
                buffer=""
                buffer_line=0
                last_send_time=$current_time
            fi
        fi
    done

    </code>
</pre>