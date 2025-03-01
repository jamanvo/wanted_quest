import re


class TokenizeService:
    @staticmethod
    def tokenize_name(name: str) -> list[str]:
        target_name = re.sub(r"\s|\(.*\)|\(|\)|주식회사|inc\.", "", name.lower())
        max_length = len(target_name)

        result = []
        for i in range(2, max_length + 1):
            for j in range(len(target_name)):
                token = target_name[j : j + i]

                if len(token) == i:
                    result.append(token)
                elif len(token) < i:
                    break

        return result
