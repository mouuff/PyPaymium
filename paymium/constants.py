
class Constants:
    URL_AUTH = "https://www.paymium.com/api/oauth/authorize"
    URL_TOKEN = "https://paymium.com/api/oauth/token"
    URL_REDIRECT = "https://www.paymium.com/page/oauth/test"
    URL_API = "https://paymium.com"
    ENV_CLIENT_ID = "PAYMIUM_CLIENT_ID"
    ENV_CLIENT_SECRET = "PAYMIUM_CLIENT_SECRET"
    TOKEN_REFRESH_BEFORE = 240  # refresh token 4 mins before expiration
    TRADING_FEES = 1 - (0.2 / 100)  # 0.2% fee
