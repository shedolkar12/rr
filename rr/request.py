import requests
import json,os
import base64
# mytoken = "0b2f711d1f9b2fd702df1ce17bf8661b2ac9cda6"
mytoken = "e21a7a8aca717085ecdd5ed552005596d45b772a"
# mytoken = "3432917d64de7d4ae07b5838eeaa93ef12e75074"
# myurl = "http://localhost:8000/addproduct/"
# myurl = "http://localhost:8000/productdetail/?reg_id=1238&product_id=3041364cf6db4508a1e057780619c4e4"
myurl = "http://localhost:8000/user/getallproduct/?reg_id=1454545"

# A get request (json example):
# response = requests.get(myurl, headers={'Authorization': 'Token {}'.format(mytoken)})
# data = response.json()

# A post request:
# 'rent', 'negotiable_flag', 'images', 'location', 'category', 'date'
imgs = os.listdir(os.getcwd()+'/img')
path = os.getcwd()+'/img'
# # print(imgs[0])
stack = []
for img in imgs:
    with open(path +'/'+img, "rb") as imageFile:
        stack.append(base64.b64encode(imageFile.read()))
p = []
for i in stack:
    print(i[0:10])
    a = i.decode('UTF-8')
    print(a[0:10])
    p.append(a)
    # print(type(i))
data = {"title":"fhhghg", "description": "djfj fjjfh", "rent":1000, "deposit":2000, "negotiable_flag": False, "images": p,  "category": "djdjd", "location":{"lat": 34.45, "long": 23.34}, }
# data = {'reg_id': '1238', 'product_id': 'bc2b13762b654d619a4958a231a4e928'}

headers = {'Authorization': 'Token {}'.format(mytoken)}
# t = requests.post(myurl, json=data, headers=headers)
t = requests.get(myurl, headers=headers)
print(t.json())
