#!/usr/bin/env python3

import json
import time

import CryptoJS
import requests
from dotenv import dotenv_values


class MyWhoosh:
    base_url = "https://event.mywhoosh.com"
    env = dotenv_values(".env")
    email = env["MW_EMAIL"]
    password = env["MW_PASSWORD"]

    session = requests.Session()

    def login(self):
        url = self.base_url + "/api/auth/login"
        data = {"remember": True, "email": self.email, "password": self.password}
        response = self.session.post(url, json=data).json()
        self.session.cookies.set("whoosh_uuid", response.get("data").get("uuId"))
        self.session.headers.update(
            {"Authorization": "Bearer " + response.get("data").get("token")}
        )
        self.session.headers.update({"Content-Type": "application/json; charset=utf-8"})

    def get_activities(self):
        url = "https://service14.mywhoosh.com/v2/rider/profile/activities"
        aes_key = "D9436E508087E863"

        payload = {"type": "", "page": 1, "sortDate": "DESC"}
        data = CryptoJS.encrypt(json.dumps(payload), aes_key)
        response = self.session.post(url, data=f'"{data}"').json()
        activities = response.get("data").get("results")
        print(activities)

    def download_activities(self):
        pass

    def logout(self):
        url = self.base_url + "/api/auth/logout"
        self.session.post(url)


if __name__ == "__main__":
    mw = MyWhoosh()
    mw.login()
    time.sleep(1)
    mw.get_activities()
    # time.sleep(1)
    # mw.logout()
