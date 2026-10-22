# Authentication vs Authorization
Authentication identifies who a user is.
Authorization specifies what a user is allowed to do.

With this API, all of the `GET` endpoints are public, meaning everyone and anyone can make calls to these endpoints. To validate this, head to your dev server ([Docs](127.0.0.1:8000/docs))

![Authorize Button](./imgs/1.png)

You can see in the top right, there is now an "Authorize" button. Click the authorize button and enter "fakeuser" as the username and "password" as the password. You can leave the other fields blank.

If successful, you will see:
![Successful Authrization](./imgs/2.png)

At this point, you are now **authenticated**. The API can tell who you are. You can validate this by using the docs page to run the `auth/users/me` endpoint. You'll see from this response that `is_admin` returns False.

Now try and run the `games/delete/{id}` endpoint. You'll see that you get a 403 - Forbidden [Admin privileges required]. Even though you are authenticated, you are not authorized.

## How do we know who can be authenticated?
When a user signs up, they will enter their password as plain text during registration. As this request is sent, the server generates a "salt". This "salt" is essentially the recipe that will be used to scramble the password. Before being written to the database, the password is hashed using an algorithm and this hashed password is then stored in the database.

When a user then goes to log in, the user enters the plaintext password. The server reads the stored hash (which includes the salt and algorithm settings) and uses those same settings to hash the entered password and then compares them.

Hashes are one-way and are not reversible, meaning they cannot be decrypted. Since the 'salt' is unique to the user, it also prevents identical passwords from producing the same hashed result. This makes data breaches less serious when companies actually store hashed passwords.

How do attackers actually breach then? 
1. Hackers will iterate through combinations of letters/numbers, hash them, and keep iterating until their generated hash matches the stored hash
2. Hackers will use SQL injection to force a hashed password match and don't even need the password
3. Phishing. Since companies are all mostly storing hashed passwords, it's easier for hackers to rely on the users handing them their passwords instead of brute forcing it.

# OAuth
So that explains the database part, but what is the API actually doing with this information?

Once the server confirms that the user can access (is authenticated by their username/password), the server issues a JWT (json web token). Unlike just providing an API key, JWTs can be set to auto expire after a certain period of time, which adds another level of security. This KWT token will then be included in all future API calls to provide authentication/authorization.

If you call the `auth/token` endpoint, you'll get a response like this:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmYWtldXNlciIsImV4cCI6MTc5MjYxMzk0NH0.oKQTb4XJ3w8Nyuh1CWgAawV2hIsvWv8mYUIKtTPIV1c",
    "token_type": "bearer",
    "expires_in": 1799,
    "expires_at": "2026-10-21T20:19:04Z"
}
```

With this API's set up, the token expires after 30 minutes. Once the token expires, the user will need to re-authenticate with the `auth/token` endpoint.