---
title : title
date: YYYY-MM-DD HH:MM:SS +09:00
author: 배현호
layout: post
categories: [""]
tags: [""]
hide: false
---

## 문제
인텔리제이 톰캣 올리는 속도가 너무 느려짐

## 해결 시도
### 1.VM 환경 설정

 1.HELP -> Edit Custom VM Options
 2. 내용 복사 
 
 <pre>
    <code>
        -server
        -Xms4096m
        -Xmx4096m
        -XX:NewRatio=3
        -Xss16m
        -XX:+AlwaysPreTouch
        -XX:+TieredCompilation
        -XX:ReservedCodeCacheSize=512m
        -XX:SoftRefLRUPolicyMSPerMB=50
        -XX:+UseCodeCacheFlushing
        -Dsun.io.useCanonCaches=false-ea
        -XX:CICompilerCount=4
        -Dsun.io.useCanonPrefixCache=false
        -XX:+HeapDumpOnOutOfMemoryError
        -XX:-OmitStackTraceInFastThrow
        -Djdk.attach.allowAttachSelf=true
        -Dkotlinx.coroutines.debug=off
        -Djdk.module.illegalAccess.silent=true
        -Dfile.encoding=UTF-8
        -XX:+UseG1GC
        -Duser.name=사용자명
    </code>
</pre>

<pre>
    <code>
        # 일반설정
        -server : JVM이 서버 최적화된 HotSpot 컴파일러를 사용
        -Xms4096m : 초기 힙 크기
        -Xmx4096m : 최대 힙 크기
        
        # 메모리 관리
        -XX:NewRatio=3
        -Xss16m : 각 스레드의 스택 크기
        
        #성능 최적화
        -XX:+AlwaysPreTouch : 런타임 중 메모리 할당에 소요되는 시간을 줄여 성능을 향상
        -XX:+TieredCompilation : JVM은 자주 사용되는 메서드를 여러 번 컴파일하여 성능 향상, 실행 속도 향상
        -XX:ReservedCodeCacheSize=512m : 예약된 코드 캐시 크기
        -XX:SoftRefLRUPolicyMSPerMB=50 : SoftReference Least Recently Used(LRU) 정책을 조정
        -XX:+UseCodeCacheFlushing : 메모리가 부족할 때 코드 캐시를 지워 특정 시나리오에서 성능을 향상
        
        #시스템/어플리케이션 속성
        -Dsun.io.useCanonCaches=false-ea : 파일 경로에 대한 정규화 캐시 사용을 비활성화하여 특정 환경에서 성능을 향상
        -XX:CICompilerCount=4 : 백그라운드 컴파일 스레드 수
        -Dsun.io.useCanonPrefixCache=false : 정규화를 위한 접두사 캐시 사용을 비활성화하여 특정 조건에서 성능을 향상
        -XX:+HeapDumpOnOutOfMemoryError : OutOfMemoryError가 발생할 때 힙 덤프 파일을 생성하여 메모리 관련 문제 해결에 도움
        -XX:-OmitStackTraceInFastThrow : 빠른 throw에서도 예외 메시지에 스택 추적을 포함
        -Djdk.attach.allowAttachSelf=true : 디버깅 목적으로 JVM이 자체에 연결
        -Dkotlinx.coroutines.debug=off : 프로덕션 환경에서 오버헤드를 줄이기 위해 Kotlin 코루틴에 대한 디버깅을 비활성화
        -Djdk.module.illegalAccess.silent=true : 특정 타사 라이브러리에서 발생할 수 있는 불법 모듈 접근에 대한 경고를 표시하지 않음
        -Dfile.encoding=UTF-8 : 기본 파일 인코딩
        -XX:+UseG1GC : 메모리 사용 패턴이 변동하는 IDE와 같은 애플리케이션에 더 적합한 G1(Garbage-First) 가비지 컬렉터를 사용
    </code>
</pre>

### 2.인텔리제이 Profile 확인
메모리 실시간 차트를 확인 하였더니 작업 시 Non-Heap Memory가 꾸준히 증가하고
CPU 사용률이 심장 박동 수 처럼 마구 튐.. 
현재 추정으로는 플러그인 중 하나가 CPU를 많이 쓰는 것이 아닐지 의심


## 출처
- [기록하는 프로그래머:티스토리](https://jong-bae.tistory.com/82)
- [인텔리제이 프로파일링](https://www.jetbrains.com/ko-kr/pages/intellij-idea-profiler/)