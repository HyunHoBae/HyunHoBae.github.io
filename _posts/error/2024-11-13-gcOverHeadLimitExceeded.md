---
title : GC Overhead
date: YYYY-MM-DD HH:MM:SS +09:00
author: 배현호
layout: post
categories: [""]
tags: [""]
---

## 상황

갑자기 서버의 CPU 사용률이 90%를 초과하면서 경고가 왔다 
top 명령어를 통해 자원 사용을 보았을 때는 램도 충분한데 CPU 사용률만 높았고

서비스에는 별다른 액션이 없어 로그도 heath 체크만 올라 오고 있었다.

차장님이 스레드 덤프를 확인 해보니 데드락인 것으로 추정하였고
임시로 tomcat을 재기동 시켜 상황을 해결 했고 그 다음 원인 분석을 시작했다.

<pre>
<code>
    jps -v # PID 획득
    jstack [PID] #덤프 생성
</code>
</pre>


## 원인 
기능 중 페이징 상관 없이 검색 조건에 해당되는 모든 파일을 Excel로 다운 받는 기능이 있었는데
서버에서 XSSFWorkbook로 Excel을 생성 한 후 sxssfWorkbook로 바꾸어 내보내는 형태였다.
해당 데이터가 많이 쌓이면서 Excel 생성 시 tomcat에 할당된 heap 메모리를 초과하며 문제가 발생했다.




## 해결 
아직 방안 검토 중
내 생각에 시도할 것
1차 XSSFWorkbook로 생성을 sxssfWorkbook로 변경 제안
2차 데이터를 클라이언트 단으로 가져와서 js를 톨해 Excel 생성 제안
heap 메모리가 매우 적게 설정 되어 있어 증설도 고려






## 참조
- [https://okky.kr/questions/789707](https://okky.kr/questions/789707)
- [https://shs2810.tistory.com/69](https://shs2810.tistory.com/69)
- [WAS) 현재 사용중인 Heap Memory 크기 확인하기](https://lilo.tistory.com/88)
- [개발 이야기 - 30만 row 엑셀 다운로드 기능 때문에 야근 및 조기 출근|작성자 까미유](https://blog.naver.com/websearch/223160405578)
- [[Java] Heap 모니터링 & Heap Dump 분석하기](https://steady-coding.tistory.com/591)
- [톰캣 CPU 점유 장애 (Feat. GC)](https://jaksimsamil.tistory.com/4)
