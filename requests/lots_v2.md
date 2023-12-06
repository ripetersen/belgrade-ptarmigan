# Curl Commands

```
curl 'https://d1wu47wucybvr3.cloudfront.net/api/lots_v2' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: en-US,en;q=0.9,da-DK;q=0.8,da;q=0.7' \
  -H 'Authorization: null' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -H 'DNT: 1' \
  -H 'Origin: https://goldin.co' \
  -H 'Pragma: no-cache' \
  -H 'Referer: https://goldin.co/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: cross-site' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  --data-raw $'{\n  "search": {\n    "queryType": "Facet",\n    "item_type": [\n      "Single Cards"\n    ],\n    "sub_category": [\n      "Baseball"\n    ],\n    "size": 24,\n    "from": 0,\n    "auction_id": [\n      "202301-3016-2107-2bff5e07-76fe-429d-9b83-549dbb2f4089",\n      "202304-2420-5916-07971458-271a-4dea-ac87-7b6447491b74",\n      "202310-2313-4536-674bc8c3-372c-4d4a-b5c9-f40155e7ceff"\n    ]\n  }\n}' \
  --compressed ;
  ```

  ```
curl 'https://d1wu47wucybvr3.cloudfront.net/api/lots_v2' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: en-US,en;q=0.9,da-DK;q=0.8,da;q=0.7' \
  -H 'Authorization: null' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -H 'DNT: 1' \
  -H 'Origin: https://goldin.co' \
  -H 'Pragma: no-cache' \
  -H 'Referer: https://goldin.co/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: cross-site' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  --data-raw $'{\n  "search": {\n    "queryType": "Featured",\n    "item_type": [\n      "Single Cards"\n    ],\n    "sub_category": [\n      "Baseball"\n    ],\n    "size": 24,\n    "from": 0,\n    "auction_id": [\n      "202301-3016-2107-2bff5e07-76fe-429d-9b83-549dbb2f4089",\n      "202304-2420-5916-07971458-271a-4dea-ac87-7b6447491b74",\n      "202310-2313-4536-674bc8c3-372c-4d4a-b5c9-f40155e7ceff"\n    ]\n  }\n}' \
  --compressed ;
  ```

  ## images:
  `https://d1htnxwo4o0jhw.cloudfront.net/cert/146576409/small/EGr9rGCqpUeCRggKknYt5w.jpg`
  `https://d1htnxwo4o0jhw.cloudfront.net/cert/146576409/large/EGr9rGCqpUeCRggKknYt5w.jpg`


```
https://d2tt46f3mh26nl.cloudfront.net/public/Lots/202308-2417-1250-315a4f73-ac55-4bdc-8baa-59a19894a423/b8246e32-d4c3-4799-914c-af21e676f361@3x
https://d2tt46f3mh26nl.cloudfront.net/public/Lots/{lot_id}/{primary_image_name}@3x
https://d2tt46f3mh26nl.cloudfront.net

https://d2tt46f3mh26nl.cloudfront.net/public/Lots/202308-2417-1249-7b32f6e0-7cb1-4bc0-a509-f5e564f526b3/dd3e3de8-4f81-4ef6-9361-d244d3cd0c13@3x

                "lot_id": "202308-2417-1249-7b32f6e0-7cb1-4bc0-a509-f5e564f526b3",
                "lot_number": 5,
                "meta_slug": "1950-bowman-22-jackie-robinson-psa-mint-927oif",
                "min_bid_price": 25000.0,
                "number_of_bids": 15.0,
                "primary_image_name": "dd3e3de8-4f81-4ef6-9361-d244d3cd0c13",
```

  ## Item
  ```
  https://goldin.co/item/1933-goudey-106-napoleon-lajoe-psa-mint-9e51dg
                         ^--------------------------------------------^ : meta_slug
https://goldin.co/item/{meta_slug}
```

curl 'https://d1wu47wucybvr3.cloudfront.net/api/lots_v2' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: en-US,en;q=0.9,da-DK;q=0.8,da;q=0.7' \
  -H 'Authorization: null' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -H 'DNT: 1' \
  -H 'Origin: https://goldin.co' \
  -H 'Pragma: no-cache' \
  -H 'Referer: https://goldin.co/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: cross-site' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  --data-raw $'{\n  "search": {\n    "queryType": "Featured",\n    "item_type": [\n      "Single Cards"\n    ],\n    "sub_category": [\n      "Baseball"\n    ],\n    "size": 24,\n    "from": 1000,\n    "auction_id": [\n      "202301-3016-2107-2bff5e07-76fe-429d-9b83-549dbb2f4089",\n      "202304-2420-5916-07971458-271a-4dea-ac87-7b6447491b74",\n      "202310-2313-4536-674bc8c3-372c-4d4a-b5c9-f40155e7ceff"\n    ]\n  }\n}'