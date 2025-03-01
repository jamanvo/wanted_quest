from app.services.tokenizer import TokenizeService


def test_tokenize():
    cases = (
        ("대상홀딩스 (주)", 10),
        ("지오코리아주식회사", 10),
        ("바이럴네이션", 15),
    )

    for case in cases:
        name = case[0]
        expect_length = case[1]

        result = TokenizeService.tokenize_name(name)
        assert expect_length == len(result)
