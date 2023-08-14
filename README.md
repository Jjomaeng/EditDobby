![final](https://user-images.githubusercontent.com/79674119/164652365-de9154be-72b8-4b97-a614-7e6f73370ac4.png)


# 크리에이터를 위한 자동 영상 편집 웹 서비스 EDIT DOBBY [![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FAIVLE-School-first-Big-Project%2FEditDobby&count_bg=%236E5029&title_bg=%23F3C385&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
<br/>


:link: **관련링크** <a href="https://drive.google.com/file/d/1fzgPNdyGTnzvcMkRXTbUQq1-1Dv0BtUc/view?usp=sharing"><img src="https://img.shields.io/badge/Poster-3766AB?style=flat-square&color=blue&link=내링크"/></a>

<br/>

## 개발 배경

기술의 발달과 인터넷의 확산, 스트리밍 기술의 발전으로 사용자들이 다양한 영상 데이터를 전송하고 활용할 수 있는 환경들이 조성되고 있다. 특히 유튜브의 성장은 영상 데이터의 지속적인 증가에 결정적으로 기여하고 있다. 이에 따라 사용자들이 원하는 정보를 무수한 컨텐츠 사이에서 시간과 노력을 들여 찾는 노력이 필요하다. 따라서 이제 유튜브를 시작하는 초보 크리에이터에게 이미 존재하는 여러 영상들로부터 경쟁력을 부여하기 위해 필요한 기능들을 지원하고자 기획하였다. 유튜브 전성시대에서 크리에이터로서 가장 많은 시간이 소요되는 과정은 자막을 입히고 영상을 편집하는 과정이다. 따라서, 유투브 초보자들의 편집을 용이하게 해주는 서비스를 구상하였다. 

<br/>

## 주요 기능

- 사용자가 폰트, 글자 색상, 배경 색상을 선택하면 자동으로 영상에 자막 생성
- 영상에 어울리는 유튜브 제목 키워드 추천
- 영상 업로드시 shorts를 자동으로 생성
- 영상에 들어간 비속어를 자동으로 필터링
- 영상에 어울리는 유튜브 썸네일 추천 

<br/>

## Main Model Architecture

![모델 구조2](https://user-images.githubusercontent.com/79674119/167116303-608e0b91-1c72-4fd3-bde6-372ad059a8d2.png)

#### 학습된 모델 경로(\dobbyedit\dobby\imgcap\ 내 저장)
https://drive.google.com/file/d/1V7E8Nj9tceUOHj4vmLwUs6BUF02zUmPG/view?usp=sharing
  
<br/>

## 데이터베이스
![ERD](https://user-images.githubusercontent.com/72778887/167324829-7e4031fc-0ed2-4469-9304-dbf63c5d2118.png)

<br/>


## 서비스 메인 화면  
![animation](https://user-images.githubusercontent.com/74889165/167283316-73bbcffb-7dea-4135-afa9-bbc86cebbc09.gif)

<br/>
  
  
## Tech
<img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white"/></a>
<img src="https://img.shields.io/badge/OpenCV-3766AB?style=flat-square&logo=OpenCV&logoColor=49FF00&color=red"/></a>
<img src="https://img.shields.io/badge/Django-3766AB?style=flat-square&color=84DFFF"/></a>
<img src="https://img.shields.io/badge/JavaScript-3766AB?style=flat-square&logo=React&logoColor=black&color=84DFFF"/></a>
<img src="https://img.shields.io/badge/CSS-3766AB?style=flat-square&color=grey"/></a>
<img src="https://img.shields.io/badge/TensorFlow-3766AB?style=flat-square&logo=TensorFlow&logoColor=yellow&color=orange"/></a>

EDIT DOBBY uses a number of open source projects to work properly:

- Python - version.3 환경
- [OpenCV] - 다양한 영상 및 동영상 데이터 처리
- [Django] - 웹 페이지 구현
- [JavaScript] - 프론트엔드 구현
- [CSS] - 프론트엔드 구현
- [TensorFlow] - 모델 구현
- [Colab] - 딥러닝 코드를 실행하기 위한 가상서버

![image](https://user-images.githubusercontent.com/74889165/167285478-a7a94161-8397-47b4-bd88-200f32d29674.png)
