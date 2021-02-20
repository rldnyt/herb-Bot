class BotSettings:
    """
    봇의 기본세팅

    TOKEN: 봇의 토큰
    TESTBOT_TOKEN: 테스트 모드일때 실행될 봇의 토큰
    prefix: 봇의 접두사
    TEST_mode: 테스트모드의 실행 여부
    developer: 개발자 권한을 적용할 유저의 ID
    """
    TOKEN = ""
    TESTBOT_TOKEN = ""
    prefix = ""
    TEST_mode = False
    developer = []
    updeveloper = []
