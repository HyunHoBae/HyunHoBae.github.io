---
title : title
date: YYYY-MM-DD HH:MM:SS +09:00
author: 배현호
layout: post
categories: [""]
tags: [""]
---


## 문제 
mybatis 로 insert 한 key를 얻기 위해 last_insert_id를 사용함
<pre>
    <code>
        <selectKey resultType="String" keyProperty="받을 KEY 명" order="AFTER">
            select last_insert_id()
        </selectKey>
    </code>
</pre>

그러나 on duplicate key update를 사용하고 업데이트가 될 경우 key가 재대로 넘어 오지 않음 

## 해결
on duplicate key update에 키 추가
<pre>
    <code>
        on duplicate key update
        key 컬럼명 = last_insert_id(last_insert_id)
    </code>
</pre>


## 참조
[on duplicate key update  사용시 last_Insert_Id 가져오기[써브 개발:티스토리]](https://servedev.tistory.com/78)