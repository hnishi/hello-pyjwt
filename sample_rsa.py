import jwt
from datetime import datetime, timezone, timedelta
import time

with open("jwtRS256.key", "r") as text_file:
    private_key = text_file.read()

with open("jwtRS256.key.pub", "r") as text_file:
    public_key = text_file.read()

# JWT の生成
headers = {"kid": "230498151c214b788dd97f22b85410a5"}  # kid --> key id (Optional)
# JWT の仕様で定められている標準クレーム
# - “exp” (Expiration Time) Claim
# - “nbf” (Not Before Time) Claim
# - “iss” (Issuer) Claim
# - “aud” (Audience) Claim
# - “iat” (Issued At) Claim
dt_now = datetime.now(tz=timezone.utc)
payload = {
    # 期限は UTC で検証されるため、encode の際には UTC で設定する
    "exp": dt_now + timedelta(seconds=1),
    # 指定の日時より前は無効とする (指定は Optional)
    "nbf": dt_now,
    # JWT の発行者。アプリ依存。このクレームの利用は Optional
    "iss": "hnishi",
    # JWT の意図された受領者。利用はアプリ依存。 (Optional)
    "aud": ["urn:foo", "urn:bar"],
    # JWT が発行された日時 (Optional)
    "iat": dt_now,
}
encoded = jwt.encode(payload, private_key, algorithm="RS256", headers=headers)
#encoded = jwt.encode(payload, private_key, algorithm="RS256")
print("encode:", encoded)

# 検証後に payload を読む
audience = ["urn:bar"]
decoded = jwt.decode(encoded, public_key, audience=audience, algorithms=["RS256"])
print("decode with validation:", decoded)

# Audience の不一致で検証に失敗
try:
    decoded = jwt.decode(encoded, public_key, algorithms=["RS256"])
except jwt.exceptions.InvalidAudienceError:
    print("InvalidAudienceError")

# 公開鍵の不一致で検証に失敗
try:
    decoded = jwt.decode(encoded, public_key.replace("a", "b"), algorithms=["RS256"])
except Exception as e :
    print("validation failed:", e)

# token の期限切れで失敗
time.sleep(2)
try:
    decoded = jwt.decode(encoded, public_key, algorithms=["RS256"])
except jwt.ExpiredSignatureError:
    print("ExpiredSignatureError")

# 検証なしで payload を読む
decoded = jwt.decode(encoded, options={"verify_signature": False})
print("decode without validation:", decoded)

# 検証なしで headers を読む
headers = jwt.get_unverified_header(encoded)
print("headers without validation:", headers)
