---
title : mysql 랜덤
date: YYYY-MM-DD HH:MM:SS +09:00
author: 배현호
layout: post
categories: ["mysql"]
tags: ["mysql"]
---


<figure class="highlight">
<pre>
<code>
select 
    #날짜
    FROM_UNIXTIME(FLOOR(unix_timestamp('2020-09-01 00:00:00')+(RAND()*(unix_timestamp('2021-10-30 00:00:00')-unix_timestamp('2012-09-01 00:00:00'))))) 
    # 문자    
    ,char(floor(rand() * 4)+65) 
    #숫자
    ,floor(rand() * (10-1)) +1 

</code>
</pre>
</figure>

### 출처
- [랜덤 날짜](https://blog.naver.com/ceman/180860893)
- [랜덤 문자](https://alithedeveloper.tistory.com/entry/MySQL-%EC%88%AB%EC%9E%90-%EC%98%81%EC%96%B4-%ED%95%9C%EA%B8%80-%EB%9E%9C%EB%8D%A4%EA%B0%92-%EC%83%9D%EC%84%B1-%EC%BF%BC%EB%A6%AC)