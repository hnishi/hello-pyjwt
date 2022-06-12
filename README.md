# Hello PyJWT

## 暗号化方法 RS256 vs HS256

### RS256

- RSA Signature with SHA-256
- 非対称な鍵を使う
- 秘密鍵と共通鍵を使う
- アイデンティティプロバイダは秘密鍵を使って署名を生成する
- クライアントは公開鍵を使って署名を検証する
- プロバイダ側は公開鍵はメタデータ URL から公開してクライアントが検証できるようにすることが多い
- クライアントは、プログラムで公開鍵を公開 URL から自動で取得可能

### HS256

- HMAC with SHA-256
- 対称な鍵を利用する（共通の１つの鍵）
- １つのキーを２つの箇所で共通利用する
- 共通のキーを用いてハッシュを生成して署名とする
- 鍵が共通のため不特定多数のクライアントが利用する場合、鍵の流出により、他者が利用できるようになってしまうため、HS256 の利用は不適切
- 共通の鍵は安全な通信チャネルを通して受け渡される必要がある
- 鍵のロールオーバーの際には、手動で更新される必要がある
- 一方で、クライアントのコントロールができる場合、鍵は１つで済むため、管理しやすい

### 参考

- [RS256 vs HS256: What&#x27;s the difference?](https://stackoverflow.com/questions/39239051/rs256-vs-hs256-whats-the-difference)

## Hello PyJWT

### Install PyJWT

RSA や ECDSA などのデジタル署名アルゴリズムを利用する場合、下記のようにインストールする。

```shell
$ pip install pyjwt[crypto]
```

- ref: [Installation &mdash; PyJWT 2.4.0 documentation](https://pyjwt.readthedocs.io/en/latest/installation.html#installation-cryptography)

利用できるデジタル署名アルゴリズムは、下記のページで確認できる。

- [Digital Signature Algorithms &mdash; PyJWT 2.4.0 documentation](https://pyjwt.readthedocs.io/en/latest/algorithms.html)

### RS256

```shell
ssh-keygen -t rsa -b 4096 -m PEM -f jwtRS256.key
openssl rsa -in jwtRS256.key -pubout -outform PEM -out jwtRS256.key.pub
```

### PyJWT の利用例

```shell
$ python sample_rsa.py
encode: eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjIzMDQ5ODE1MWMyMTRiNzg4ZGQ5N2YyMmI4NTQxMGE1In0.eyJleHAiOjE2NTUwNDcyMjQsIm5iZiI6MTY1NTA0NzIyMywiaXNzIjoiaG5pc2hpIiwiYXVkIjpbInVybjpmb28iLCJ1cm46YmFyIl0sImlhdCI6MTY1NTA0NzIyM30.DwgC8EmG3QO1i5S_thlS8w5lb_3cDg1qpMBIR3GL326cFJYsxKm58Wt1Z2IvHexsupAFR0yoZr8jdU-tmvSCmqS0i_A8MC5au2F9-2yusoYunCFUogZ1HbyetBNtbIIeuRe0dUDXn-0LG-jneedu41mj7_J6M184_MJO4Ds8B-yvxvLfog8lTF4h3iTIPErZwbblY27QPUmEE1s4tIqxZ1jsKINuzuK3A1SPWD4rzC_eVqjBCp08mLYr5cfd0mN4xIrzAqRtcytwUAaIKrsiMMEurHLE1GYzcUl_f5OiEuadKLvMQUR7p_PwgNzKkNl738EqrQYEXGb5sDTynryZtePjKOCuqzInvUE208OEASaVbJE9_vgw8_3S0xDhJIvOl-ISiJ5Da6ss5XwJjfxsq3m0g_iXQKxiJ7N51On0sfQtlNPtd1lA_ynIdVIEN2JY70kFogkvYu3J7HX3KHwI-swdzY3YqDxH0fYYVddnrikrBSPn1aDFF3pHG7_uTR4AP2xGK5cDpopHIWBQz2G5M5BNl2po2ce8qnij0q7VjOdGYREJyvtHRm7Aynv5MjhZord9gZhKJeiFrx-7412Nw_DkIBDQ6lhfCeHH4twEpJw2JBVeTgoJbPhohRBZZzGOLPXVSHpV6QjrbuJUdpIiwwfxf6721oY1NPYLZF8nYIo
decode with validation: {'exp': 1655047224, 'nbf': 1655047223, 'iss': 'hnishi', 'aud': ['urn:foo', 'urn:bar'], 'iat': 1655047223}
InvalidAudienceError
validation failed: Signature verification failed
ExpiredSignatureError
decode without validation: {'exp': 1655047224, 'nbf': 1655047223, 'iss': 'hnishi', 'aud': ['urn:foo', 'urn:bar'], 'iat': 1655047223}
headers without validation: {'typ': 'JWT', 'alg': 'RS256', 'kid': '230498151c214b788dd97f22b85410a5'}
```

以下のスクリプトにコメントと共に記載した。

[sample_rsa.py](./sample_rsa.py)

- ref: [Usage Examples &mdash; PyJWT 2.4.0 documentation](https://pyjwt.readthedocs.io/en/latest/usage.html)
