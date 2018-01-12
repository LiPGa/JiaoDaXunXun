# coding=utf-8
#from PIL import Image
import cv2
import sys,os,math,pickle,pprint,codecs
reload(sys)
sys.setdefaultencoding('utf-8')

class dHash:
    def __init__(self,img):
        self.res = []
        self.img = img
        self.hash = ""
        self.decimalRes = 0
        self.process()
        self.my_hash()


    def hist(self,r_b,r_e,c_b,c_e):
        red = 0
        blue = 0
        green = 0

        for i in range(r_b,r_e):
            for j in range(c_b,c_e):
                #print img[i,j][0]
                blue += self.img[i,j][0]
                green += self.img[i,j][1]
                red += self.img[i,j][2]

        return red,green,blue
        

    def process(self):
        row = self.img.shape[0]
        col = self.img.shape[1]

        r1 = int(row/2)
        c1 = int(col/2)

        blocks = [(0,r1,0,c1),(r1,row,0,c1),(0,r1,c1,col),(r1,row,c1,col)]

        for i in range(4):
            temp = self.hist(*blocks[i])
            for j in range(3):
                self.res.append(temp[j])

        total = 0
        for i in range(12):
            total += self.res[i] * self.res[i]
        total = math.sqrt(total)
        for i in range(12):
            self.res[i] /= total
            #print self.res[i],
            self.res[i] /= 0.3
            if self.res[i] > 2:
                self.res[i] = 2
            #print self.res[i]

    def my_hash(self):
        hash_string = ""    #定义空字符串的变量，用于后续构造比较后的字符串
        for row in range(0,len(self.res)): #获取pixels元素个数，从1开始遍历
            if self.res[row] > self.res[(row+2)%len(self.res)]: #当前位置非行首位时，我们拿前一位数值与当前位进行比较
                self.hash += '1'   #当为真时，构造字符串为1
            else:
                self.hash += '0'   #否则，构造字符串为0
            if self.res[row] > self.res[(row+3)%len(self.res)]:
                self.hash += '1'   #当为真时，构造字符串为1
            else:
                self.hash += '0'   #否则，构造字符串为0
              #最后可得出由0、1组64位数字字符串，可视为图像的指纹
        #print self.res
        #print self.hash
        self.decimalRes =  int(self.hash,2)  


def Difference(dhash1, dhash2):
    if dhash2 is None:
        return
    difference = dhash1 ^ dhash2  #将两个数值进行异或运算
    return bin(difference).count('1') #异或运算后计算两数不同的个数，即个数<5

def preprocess(folderpath):

    dic = {}

    namesDic = get_name()

    images = os.listdir(folderpath)

    for image in images:

        name = namesDic[image]

        fullname=os.path.join(folderpath,image)

        img = cv2.imread(fullname, cv2.IMREAD_COLOR)
        if img is None:
            continue

        img1 = cv2.resize(img,(8,8), interpolation = cv2.INTER_AREA)

        hash1 = dHash(img1)

        #print dic.keys()

        if hash1.decimalRes not in dic.keys():
            dic[hash1.decimalRes] = []
        else:
            tmp = []
            tmp.append(image)
            tmp.append(name)
            dic[hash1.decimalRes].append(tmp)

    return dic

def get_name():
    f = codecs.open('names.txt','r','utf-8')

    nameDic = {}
    cnt = 0

    for names in f:
        index = str(cnt) + '.jpg'
        nameDic[index] = names.encode('utf-8')
        cnt += 1

    f.close()
    return nameDic




def match(img,res):
    print 'res',res
    pic_rank = []
    orb = cv2.ORB()
    img = cv2.imread(img,0)
    kp2,des2 = orb.detectAndCompute(img,None)

    #print des2

    bf = cv2.BFMatcher()

    for image in res:
        print  image
        fullname=os.path.join('materials',image[0])
        print fullname
        name = image[1]
        print 'name',image[0],image[1]
        # print fullname,name
        # results = my_ocr(fullfilename)
        img1 = cv2.imread(fullname, 0)

        if img1 is None:
            print 'haha'
            continue

        kp1 = orb.detect(img1,None)
        kp1,des1 = orb.compute(img1,kp1)

        matches = bf.knnMatch(des1,des2,k=2)

        cnt = 0
        for m,n in matches:
            if m.distance < 0.75 * n.distance:
                cnt += 1
        # print image,cnt

        pic_rank.append((name,cnt))

    print 'pic_rank',pic_rank
    res  = sorted(pic_rank, key=lambda x:x[1],reverse=True)
    print 'last',res
    return res
    #print 'hello'

def match2(image,dhash):
    img = cv2.imread(image, cv2.IMREAD_COLOR)
    img1 = cv2.resize(img,(8,8), interpolation = cv2.INTER_AREA)
    test = dHash(img1)

    for dh in dhash.keys():
        if Difference(test.decimalRes,dh) == 0:
            res = dhash[dh]
    print 'fuck',res
    a = match(image,res)
    return a



# if __name__ == '__main__':
#     # dic = {}
#     # dic = preprocess('materials')
#     # #print dic
#     # dictoutput = open('dhash.pkl','wb')
#     # pickle.dump(dic, dictoutput)
#     # dictoutput.close()

#     pklfile = open('dhash.pkl','rb')
#     dhash = pickle.load(pklfile)
#     # pprint.pprint(dhash)
#     res = match('382.jpg',dhash)
#     for i in res:
#         print i[0],i[1]
    # res = match('121.jpg',dhash)

    #get_name()
