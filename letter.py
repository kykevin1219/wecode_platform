html = """\
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>위코드 초대 메일</title>
            </head>
            <body>
                <div style="max-width: 600px; width: 100%; min-width: 375px; border-radius: 10px; border: 1px solid black; overflow: hidden; margin: 0 auto;">
                <header style="background-color: black; padding: 15px; text-align: center;">
                    <img src="https://s3.ap-northeast-2.amazonaws.com/cdn.wecode.co.kr/logo/wecode_logo.png" height="50px" />
                </header>
                <div style="font-size: 16px; padding: 40px 25px 0 25px; background-color: white;">
                    <p style="margin: 0 0 30px 0; line-height: 24px;">
                        {name}님, Wecode와 함께 하게 되신 것을 축하드립니다!<br/>
                        앞으로 Wecode와 12주 동안 재밌게 열심히 코딩 공부를 하여 훌륭한 개발자가 되시길 기원합니다.
                    </p>
                    <p style="margin: 0 0 30px 0; line-height: 24px;">
                        wecode 전용 사이트는 <a href="https://github.com/" target="_blank">github</a> 계정으로 로그인 됩니다.<br/>
                        가입을 안 하셨으면 <a href="https://github.com/" target="_blank">github</a> 먼저 가입해주세요!
                    </p>
                    <a href="http://localhost:3000/login?token={token}" style="display: inline-block; margin-bottom: 40px; background-color: #377dff; border-radius: 3px; color: white; text-decoration: none; padding: 13px 20px;">
                        wecode 사이트 가입하기
                    </a>
                </div>
                <footer style="background-color: black; padding: 15px; text-align: center;">
                    <a href="https://wecode.co.kr" target="_blank" style=" color: white; font-size: 13px;">
                        wecode.co.kr
                    </a>
                    <p style="color: white; font-size: 12px; margin: 5px 0 0 0;">
                        서울특별시 강남구 테헤란로 427 위워크 선릉2호점
                    </p>
                </footer>
                </div>
            </body>
            </html>
        """
