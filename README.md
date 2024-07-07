# CourseConnect

### Welcome to CourseConnect! 

Course Connect is an app to **anonymously** connect classmates at the University of Waterloo! Securely login and anonymously create course specific posts to match and chat! Use this for specific assignments, labs, or quizzes for any class such as *wink wink* CLAS104.

## Overview
How did I create this? Visit a high level overview:

**Front End**: React Native *with Expo*

**Backend**: FastAPI *with Pydantic Schemas, Websockets, SQLAlchemy*

**Database**: PostgreSQL

**User Authentication**: AUTH0 By Okta

**Chat Implementation**: Websockets (FastAPI <=> React)

![High Level Overview](assets/Overview.png)

## Features
- Anonymously create posts for course assignments, labs, quizzes, etc. Wait until someone matches with it, and then chat away!

## Previews
**Here are some preview images of CourseConnect:**

### View Posts
<img src="assets/MobileView1.png" width="250"/>
<img src="assets/MobileView2.png" width="250"/>

### Groups and Chats
<img src="assets/MobileView9.png" width="250"/>
<img src="assets/MobileView10.png" width="250"/>

### Create Posts
<div class="image-container">
    <img src="assets/MobileView4.png" width="250"/>
    <img src="assets/MobileView3.png" width="250"/>
    <img src="assets/MobileView5.png" width="250"/>
    <img src="assets/MobileView6.png" width="250"/>
    <img src="assets/MobileView7.png" width="250"/>
    <img src="assets/MobileView8.png" width="250"/>
</div>

<style>
    .image-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;

    }
</style>

</br>

## API Documents

<img src="assets/API Docs.png" />
<img src="assets/API Schemas.png" />


## Mentions 
Thanks to Eugene Lee for creating a Figma Wireframe. [Link](https://www.figma.com/design/IBsMThM0eORSRxn2Xs5hHr/UWCourseConnect?node-id=0-1&t=Ub1CybyDOVu5Q1Gb-1)

GiftedChat: Chat UI [Link](https://github.com/FaridSafi/react-native-gifted-chat)

## License

CourseConnect is licensed under the [MIT License](LICENSE).
