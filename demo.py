from image_tools import encode_image, decode_image, save_image

# simple demonstration of encoding a string in an image file
# > python3 demo.py

data = 'Wow this is going to be encoded in an image file!'
img = 'col.jpg'

print('Encoding ' + data + ' in image ' + img + '...')

enc_img = encode_image(data, 'col.jpg')
save_image(enc_img, 'demo_enc.png')

print('Message encoded.')

print('Decoding message from image...')

decoded_data = decode_image('demo_enc.png')
print('Decoded message: ' + decoded_data)
