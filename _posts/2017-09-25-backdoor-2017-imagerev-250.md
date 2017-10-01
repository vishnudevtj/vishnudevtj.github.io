---
title:  Backdoor 2017 Imagerev 250
updated: 2017-09-25 19:03:10
---


- [Backdoor 2017 image rev 250](#org91b3d35)


<a id="org91b3d35"></a>

# Solved Backdoor 2017 image rev 250

[Imagerev 200](https://backdoor.sdslabs.co/challenges/IMAGEREV) Backdoor CTF 2017

> Reverse the encrypted file and recover the flag.
> [encrypted.txt](http://hack.bckdr.in/IMAGEREV/encrypted.txt) 
> [encrypt.py](http://hack.bckdr.in/IMAGEREV/encrypt.py)

The challenge gives you two files One `encrypt.py` and `enctrypted.txt`

```python
from PIL import Image


def bin_return(dec):
    return(str(format(dec, 'b')))


def bin_8bit(dec):
    return(str(format(dec, '08b')))


def convert_32bit(dec):
    return(str(format(dec, '032b')))


def convert_64bit(dec):
    return(str(format(dec, '064b')))


def hex_return(dec):
    return expand(hex(dec).replace('0x', '').replace('L', ''))


def dec_return_bin(bin_string):
    return(int(bin_string, 2))


def dec_return_hex(hex_string):
    return(int(hex_string, 16))


def some_LP(l, n):
    l1 = []
    j = 0
    k = n
    while k < len(l) + 1:
        l1.append(l[j:k])
        j = k
        k += n
    return(l1)


def rotate_right(bit_string, n):
    bit_list = list(bit_string)
    count = 0
    while count <= n - 1:
        list_main = list(bit_list)
        var_0 = list_main.pop(-1)
        list_main = list([var_0] + list_main)
        bit_list = list(list_main)
        count += 1
    return(''.join(list_main))


def shift_right(bit_string, n):
    bit_list = list(bit_string)
    count = 0
    while count <= n - 1:
        bit_list.pop(-1)
        count += 1
    front_append = ['0'] * n
    return(''.join(front_append + bit_list))


def addition(input_set):
    value = 0
    for i in range(len(input_set)):
        value += input_set[i]
    mod_32 = 4294967296
    return(value % mod_32)


def str_xor(s1, s2):
    return ''.join([str(int(i) ^ int(j)) for i, j in zip(s1, s2)])


def str_and(s1, s2):
    return ''.join([str(int(i) & int(j)) for i, j in zip(s1, s2)])


def str_not(s):
    return ''.join([str(int(i) ^ 1) for i in s])


def not_and_and_xor(x, y, z):
    return(str_xor(str_and(x, y), str_and(str_not(x), z)))


def and_and_and_xor_xor(x, y, z):
    return(str_xor(str_xor(str_and(x, y), str_and(x, z)), str_and(y, z)))


def some_e0(x):
    return(str_xor(str_xor(rotate_right(x, 2), rotate_right(x, 13)), rotate_right(x, 22)))


def some_e1(x):
    return(str_xor(str_xor(rotate_right(x, 6), rotate_right(x, 11)), rotate_right(x, 25)))


def some_s0(x):
    return(str_xor(str_xor(rotate_right(x, 7), rotate_right(x, 18)), shift_right(x, 3)))


def some_s1(x):
    return(str_xor(str_xor(rotate_right(x, 17), rotate_right(x, 19)), shift_right(x, 10)))


def expand(s):
    return '0' * (8 - len(s)) + s


def get_pixels_list(filename):
    im = Image.open(filename)
    return list(im.getdata())


def data_encrypted(list_of_pixels):
    data = ''
    for i in list_of_pixels:
        d = ''.join([chr(j) for j in i])
        d = encryption(d)
        data += ''.join(d)
    return data


def message_pad(bit_list):
    pad_one = bit_list + '1'
    pad_len = len(pad_one)
    k = 0
    while ((pad_len + k) - 448) % 512 != 0:
        k += 1
    back_append_0 = '0' * k
    back_append_1 = convert_64bit(len(bit_list))
    return(pad_one + back_append_0 + back_append_1)


def message_bit_return(string_input):
    bit_list = []
    for i in range(len(string_input)):
        bit_list.append(bin_8bit(ord(string_input[i])))
    return(''.join(bit_list))


def message_pre_pro(input_string):
    bit_main = message_bit_return(input_string)
    return(message_pad(bit_main))


def message_parsing(input_string):
    return(some_LP(message_pre_pro(input_string), 32))


def message_schedule(index, w_t):
    new_word = convert_32bit(addition([int(some_s1(w_t[index - 2]), 2), int(
        w_t[index - 7], 2), int(some_s0(w_t[index - 15]), 2), int(w_t[index - 16], 2)]))
    return(new_word)


initial = ['6a09e667', 'bb67ae85', '3c6ef372', 'a54ff53a',
           '510e527f', '9b05688c', '1f83d9ab', '5be0cd19']

values = ['428a2f98', '71374491', 'b5c0fbcf', 'e9b5dba5', '3956c25b', '59f111f1', '923f82a4', 'ab1c5ed5', 'd807aa98', '12835b01', '243185be', '550c7dc3', '72be5d74', '80deb1fe', '9bdc06a7', 'c19bf174', 'e49b69c1', 'efbe4786', '0fc19dc6', '240ca1cc', '2de92c6f', '4a7484aa', '5cb0a9dc', '76f988da', '983e5152', 'a831c66d', 'b00327c8', 'bf597fc7', 'c6e00bf3', 'd5a79147', '06ca6351', '14292967',
          '27b70a85', '2e1b2138', '4d2c6dfc', '53380d13', '650a7354', '766a0abb', '81c2c92e', '92722c85', 'a2bfe8a1', 'a81a664b', 'c24b8b70', 'c76c51a3', 'd192e819', 'd6990624', 'f40e3585', '106aa070', '19a4c116', '1e376c08', '2748774c', '34b0bcb5', '391c0cb3', '4ed8aa4a', '5b9cca4f', '682e6ff3', '748f82ee', '78a5636f', '84c87814', '8cc70208', '90befffa', 'a4506ceb', 'bef9a3f7', 'c67178f2']


def encryption(input_string):
    w_t = message_parsing(input_string)
    a = convert_32bit(dec_return_hex(initial[0]))
    b = convert_32bit(dec_return_hex(initial[1]))
    c = convert_32bit(dec_return_hex(initial[2]))
    d = convert_32bit(dec_return_hex(initial[3]))
    e = convert_32bit(dec_return_hex(initial[4]))
    f = convert_32bit(dec_return_hex(initial[5]))
    g = convert_32bit(dec_return_hex(initial[6]))
    h = convert_32bit(dec_return_hex(initial[7]))
    for i in range(0, 64):
        if i <= 15:
            t_1 = addition([int(h, 2), int(some_e1(e), 2), int(
                not_and_and_xor(e, f, g), 2), int(values[i], 16), int(w_t[i], 2)])
            t_2 = addition([int(some_e0(a), 2), int(
                and_and_and_xor_xor(a, b, c), 2)])
            h = g
            g = f
            f = e
            e = addition([int(d, 2), t_1])
            d = c
            c = b
            b = a
            a = addition([t_1, t_2])
            a = convert_32bit(a)
            e = convert_32bit(e)
        if i > 15:
            w_t.append(message_schedule(i, w_t))
            t_1 = addition([int(h, 2), int(some_e1(e), 2), int(
                not_and_and_xor(e, f, g), 2), int(values[i], 16), int(w_t[i], 2)])
            t_2 = addition([int(some_e0(a), 2), int(
                and_and_and_xor_xor(a, b, c), 2)])
            h = g
            g = f
            f = e
            e = addition([int(d, 2), t_1])
            d = c
            c = b
            b = a
            a = addition([t_1, t_2])
            a = convert_32bit(a)
            e = convert_32bit(e)
    value_0 = addition([dec_return_hex(initial[0]), int(a, 2)])
    value_1 = addition([dec_return_hex(initial[1]), int(b, 2)])
    value_2 = addition([dec_return_hex(initial[2]), int(c, 2)])
    value_3 = addition([dec_return_hex(initial[3]), int(d, 2)])
    value_4 = addition([dec_return_hex(initial[4]), int(e, 2)])
    value_5 = addition([dec_return_hex(initial[5]), int(f, 2)])
    value_6 = addition([dec_return_hex(initial[6]), int(g, 2)])
    value_7 = addition([dec_return_hex(initial[7]), int(h, 2)])
    value = (hex_return(value_0), hex_return(value_1), hex_return(value_2), hex_return(
        value_3), hex_return(value_4), hex_return(value_5), hex_return(value_6), hex_return(value_7))
    return(value)

list_pixels = get_pixels_list('./flag.png')
data = data_encrypted(list_pixels)
f = open('./encrypted.txt','w')
f.write(data)
f.close()
```

encrypted.txt contains the hashed output

    709e80c88487a2411e1ee4dfb9f22a861492d20c4765150c0c794abd70f8147c709e80c88487a2 ......


First I tried to Reverse the Code and it was booting , Got some ideas about the script that it takes the tuple of the pixel values and convert it to a hash of 64 length

So I Taught of Brute forcing the entire space , which is `256x256x256`

The only Problem is that it takes time, it takes 1sec in my pc to calculate 10 hashes and the whole will take 2 days ,which is not possible

```python
f = open('./encrypted.txt', 'r'),
text = f.read()
enc = [text[i:i + 64] for i in range(0, len(text), 64)]
l1 = open('./list.txt','w')
for i in enc:
    l1.write(i+"\n")
```

```shell
cat list.txt   | sort -n | uniq -c | sort -n -r
```

    5821 709e80c88487a2411e1ee4dfb9f22a861492d20c4765150c0c794abd70f8147c
     306 ac205167ca956b408a925c3854fdd82ffa43672263ae7dba5a68b29d9a81fa56
     291 2ec847d8a31a988b3117a5095dae74f490448223f035ec7eddef6768b91a9028
     188 8ae40a3583aef6697d2c2eff57eb915ed0bda54aaa92812ad97982743ac06f37
      90 ab5ab0fedc83e5a1a1871c427eccbcd3cf0fc1bb74a82a552adfd9b4e57f391b
      85 2ac9a6746aca543af8dff39894cfe8173afba21eb01c6fae33d52947222855ef
      79 f1b901847390b0ed7e374e7c1e464ec17b46a427c487a5ad6cbd2906405083d5
      73 5ae7e6a42304dc6e4176210b83c43024f99a0bce9a870c3b6d2c95fc8ebfb74c
      62 b9e8d0a22760b87553c0b9c55ae93058bf8d4389c87765488cea1637e94bd9b6
      59 a30cb1d8569c5c141b2ade1caf57038b2be46c9bc4939c8f702a0ff4fcecfd77
      58 91737e71235959a56c524997e18d6d14d6ddd714ed2a450a24f765255a2733ee
      53 700af1feb55ab0613bdbc466815643743156af4e869120244eb05ca72c45002c
      50 0aad7da77d2ed59c396c99a74e49f3a4524dcdbcb5163251b1433d640247aeb4
      47 7b108f7c5c6f1507c4ffe2275dd9b8e25a71d175a5a9d3e19aeec3f27d82caf1
      42 204164d223b35aabb54ea32b1d14d8bb5a8df56f7c81f3304987fa4193426729
      38 c4289629b08bc4d61411aaa6d6d4a0c3c5f8c1e848e282976e29b6bed5aeedc7
      24 5ae0d5195906bfc4f70167cf171ae4d08e7376aa246977acf172187d5d384f10

I spilt the encrypted.txt into fragments of length 64 and analysing the files reveals that there are only 17 uniq values

So I grabbed the most used used RGB colors from [here](http://www.cloford.com/resources/colours/500col.htm)

```python

color_list = [(176, 	23, 	31),
              (220, 	20, 	60),
              (255, 	182, 	193),
              (255, 	174, 	185),
              (238, 	162, 	173),
              (205, 	140, 	149),
              (139, 	95, 	101),
              (255, 	192, 	203),
              (255, 	181, 	197),
              ...
              ...
              ...
]

for i in range(0, len(color_list), 1):
    if data_encrypted(color_list[i:i + 1]) in col_hash:
        print(color_list[i:i + 1], data_encrypted(color_list[i:i + 1]))
```

    ([(255, 255, 255)], '5ae7e6a42304dc6e4176210b83c43024f99a0bce9a870c3b6d2c95fc8ebfb74c')
    ([(128, 128, 128)], '8ae40a3583aef6697d2c2eff57eb915ed0bda54aaa92812ad97982743ac06f37')
    ([(0, 0, 0)], '709e80c88487a2411e1ee4dfb9f22a861492d20c4765150c0c794abd70f8147c')
    ([(207, 207, 207)], '7b108f7c5c6f1507c4ffe2275dd9b8e25a71d175a5a9d3e19aeec3f27d82caf1')
    ([(191, 191, 191)], 'ac205167ca956b408a925c3854fdd82ffa43672263ae7dba5a68b29d9a81fa56')
    ([(143, 143, 143)], 'b9e8d0a22760b87553c0b9c55ae93058bf8d4389c87765488cea1637e94bd9b6')
    ([(112, 112, 112)], 'c4289629b08bc4d61411aaa6d6d4a0c3c5f8c1e848e282976e29b6bed5aeedc7')
    ([(64, 64, 64)], '2ec847d8a31a988b3117a5095dae74f490448223f035ec7eddef6768b91a9028')
    ([(48, 48, 48)], '2ac9a6746aca543af8dff39894cfe8173afba21eb01c6fae33d52947222855ef')

The output shows that the pixels have all the values equal , Let's test all the values from 0 - 256

```python

for i in range(0, 256):
    if data_encrypted([(i, i, i)]) in col_hash:
        print(i, data_encrypted([(i, i, i)]))
```

    
    Result :
    (0, '709e80c88487a2411e1ee4dfb9f22a861492d20c4765150c0c794abd70f8147c')
    (16, 'ab5ab0fedc83e5a1a1871c427eccbcd3cf0fc1bb74a82a552adfd9b4e57f391b')
    (32, '0aad7da77d2ed59c396c99a74e49f3a4524dcdbcb5163251b1433d640247aeb4')
    (48, '2ac9a6746aca543af8dff39894cfe8173afba21eb01c6fae33d52947222855ef')
    (64, '2ec847d8a31a988b3117a5095dae74f490448223f035ec7eddef6768b91a9028')
    (80, '204164d223b35aabb54ea32b1d14d8bb5a8df56f7c81f3304987fa4193426729')
    (96, 'f1b901847390b0ed7e374e7c1e464ec17b46a427c487a5ad6cbd2906405083d5')
    (112, 'c4289629b08bc4d61411aaa6d6d4a0c3c5f8c1e848e282976e29b6bed5aeedc7')
    (128, '8ae40a3583aef6697d2c2eff57eb915ed0bda54aaa92812ad97982743ac06f37')
    (143, 'b9e8d0a22760b87553c0b9c55ae93058bf8d4389c87765488cea1637e94bd9b6')
    (159, '91737e71235959a56c524997e18d6d14d6ddd714ed2a450a24f765255a2733ee')
    (175, '700af1feb55ab0613bdbc466815643743156af4e869120244eb05ca72c45002c')
    (191, 'ac205167ca956b408a925c3854fdd82ffa43672263ae7dba5a68b29d9a81fa56')
    (207, '7b108f7c5c6f1507c4ffe2275dd9b8e25a71d175a5a9d3e19aeec3f27d82caf1')
    (223, 'a30cb1d8569c5c141b2ade1caf57038b2be46c9bc4939c8f702a0ff4fcecfd77')
    (239, '5ae0d5195906bfc4f70167cf171ae4d08e7376aa246977acf172187d5d384f10')
    (255, '5ae7e6a42304dc6e4176210b83c43024f99a0bce9a870c3b6d2c95fc8ebfb74c')

Now we got all the pixels corresponding to the hashes in the encrypted text

Now Decryption , But they have not given the image resolution , there are `7371` pixels now the image resolution will be factor of this number

We try them all !!

```python

key_dic = {'709e80c88487a2411e1ee4dfb9f22a861492d20c4765150c0c794abd70f8147c': 0,
           'ab5ab0fedc83e5a1a1871c427eccbcd3cf0fc1bb74a82a552adfd9b4e57f391b': 1,
           '0aad7da77d2ed59c396c99a74e49f3a4524dcdbcb5163251b1433d640247aeb4': 3,
           '2ac9a6746aca543af8dff39894cfe8173afba21eb01c6fae33d52947222855ef': 4,
           '2ec847d8a31a988b3117a5095dae74f490448223f035ec7eddef6768b91a9028': 6,
           '204164d223b35aabb54ea32b1d14d8bb5a8df56f7c81f3304987fa4193426729': 8,
           'f1b901847390b0ed7e374e7c1e464ec17b46a427c487a5ad6cbd2906405083d5': 9,
           'c4289629b08bc4d61411aaa6d6d4a0c3c5f8c1e848e282976e29b6bed5aeedc7': 11,
           '8ae40a3583aef6697d2c2eff57eb915ed0bda54aaa92812ad97982743ac06f37': 12,
           'b9e8d0a22760b87553c0b9c55ae93058bf8d4389c87765488cea1637e94bd9b6': 14,
           '91737e71235959a56c524997e18d6d14d6ddd714ed2a450a24f765255a2733ee': 15,
           '700af1feb55ab0613bdbc466815643743156af4e869120244eb05ca72c45002c': 17,
           'ac205167ca956b408a925c3854fdd82ffa43672263ae7dba5a68b29d9a81fa56': 19,
           '7b108f7c5c6f1507c4ffe2275dd9b8e25a71d175a5a9d3e19aeec3f27d82caf1': 20,
           'a30cb1d8569c5c141b2ade1caf57038b2be46c9bc4939c8f702a0ff4fcecfd77': 22,
           '5ae0d5195906bfc4f70167cf171ae4d08e7376aa246977acf172187d5d384f10': 23,
           '5ae7e6a42304dc6e4176210b83c43024f99a0bce9a870c3b6d2c95fc8ebfb74c': 25,
           }

pixels = []
num = 0
print(len(enc))
for i in enc:
    num = key_dic[i]
    pixels.append((num, num, num))


pos_cor = [(1, 7371),
           (3, 2457),
           (7, 1053),
           (9, 819),
           (13, 567),
           (21, 351),
           (27, 273),
           (39, 189),
           (63, 117),
           (81, 91)]

for j in pos_cor:
    img = Image.new('RGB', j, 'white')
    pix = img.load()
    cordinates = []

    for i in range(0, len(pixels), j[1]):
        cordinates.append(pixels[i:i + j[1]])

    for i in range(0, j[0]):
        for k, n in zip(cordinates[i], range(0, j[1])):
            pix[i, n] = k[0:3]
    img.save("image" + str(j[0]) + ".png")


```

`image21.png` contains the flag

