# Dacon-star2

## INTRODUCTION

행동 데이터 분석 인공지능 AI 경진대회
디지털로 된 정보 위에서 경쟁한다는 점에서, 게임 대회와 데이터 분석 경진대회는 맥락이 비슷합니다.
Blizzard 스타크래프트2 경기의 행동 데이터로 승패를 예측합니다.



## FEATURE

  #### game_id : 경기 구분 기호
  #### winner : player 1의 승리 확률
  #### time : 경기 시간
  #### player : 선수
  #### 1) 0: player 0
  #### 2) 1: player 1
  #### species : 종족
  #### 1) T: 테란
  #### 2) P: 프로토스
  #### 3) Z: 저그
  #### event : 행동 종류
  #### event_contents : 행동 상세
  #### 1) Ability : 생산, 공격 등 선수의 주요 행동
  #### 2) AddToControlGroup : 부대에 추가
  #### 3) Camera : 시점 선택
  ####  4) ControlGroup : 부대 행동
  #### 5) GetControlGroup : 부대 불러오기
  #### 6) Right Click : 마우스 우클릭
  #### 7) Selection : 객체 선택
  #### 8) SetControlGroup : 부대 지정

## MODEL
- LightGBM 사용
