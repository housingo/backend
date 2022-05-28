import requests


urls = {
    "eindhoven": "https://discordapp.com/api/webhooks/940325425257783346/paCcXuB0XzkFpp4i7uMBVQnVjB_IM7Av_KYpJQX2lmJq4pi62DR6kgFA9gvsw-MaMTAv",
    "tilburg": "https://discordapp.com/api/webhooks/975784930602795059/QjNm-XeQ715Vw3vR_Y3m1NspBvJhoMTnhjkZ9dz4x26OInm3y4Qvedj7qOnXHGVTCTVS",
    "amsterdam": "https://discordapp.com/api/webhooks/975783149164437564/fhWw5LatMzA7JycLjHBS1cV2cKMVu_UIix6ZyJ-zsxJO3azm0PhuSPvtL32gRbdd8OQB",
    "groeningen": "https://discordapp.com/api/webhooks/975783829518311484/wgPkDkhJnSk4Zhh1Zq17G-MVgMUj3xy_TQ5d089IwxYCjCH6mzhGLUQzSyZK8NZKb0_E",
    "utrecht": "https://discordapp.com/api/webhooks/975784077699481710/yYOc3euZG6leX6JCKdtbwnNQYDYZMGIe-ardbtWSYYeSGdKoJCwm1R4fmcaLXLweT4AW",
    "hague": "https://discordapp.com/api/webhooks/975784386131795988/HBPl0IecHmGrCgMzKax4z-Iaet1bledpSiM1fpKoivNRYoHxQHGqnKJcS23Y5Xu2jnOV",
    "maastricht": "https://discordapp.com/api/webhooks/975784631884451900/V2CP2CGrfGZdfTEQb4DeOqIITagIvtzxuE2mPu-gKCGrRp4ZZJ529DeZbma9nDDS34iK",
}


def alert_customers(item: str, city: str):
    requests.post(
        urls.get(city),
        data={"content": "⚠⚠⚠ NEW APARTMENT FOUND ⚠⚠⚠ \n \n" + item},
    )
