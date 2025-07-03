class BelugaError(Exception):
    """기본 Beluga 에러"""
    pass

class BelugaValidationError(BelugaError):
    """Beluga 클래스 검증 에러"""
    pass

class BelugaParsingError(BelugaError):
    """Beluga 파싱 에러"""
    pass