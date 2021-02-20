class BotSettings:
    """
    봇의 기본세팅

    TOKEN: 봇의 토큰
    TESTBOT_TOKEN: 테스트 모드일때 실행될 봇의 토큰
    prefix: 봇의 접두사
    TEST_mode: 테스트모드의 실행 여부
    developer: 개발자 권한을 적용할 유저의 ID
    updeveloper: 개발자 권한보다 더 높은 권한을 적용할 유저의 ID
    state: 상테메시지들
    statetime: 상태메시지가 몇초마다 변경되도록 하기
    botowner: 봇 주인의 ID

    logwebid: 로그(봇실행, 에러알림)의 채널의 ID
    logwebtoken: 로그(봇실행, 에러알림)의 채널의 토큰
    """
    TOKEN = ""
    TESTBOT_TOKEN = ""
    prefix = "="
    TEST_mode = True
    developer = []
    updeveloper = []
    state = []
    statetime = 10

    botowner = 

    logwebid = 
    logwebtoken = ""
