import qrcode
img = qrcode.make('https://oa.zalo.me/home')
print(type(img))  # qrcode.image.pil.PilImage
img.save("QR.png")