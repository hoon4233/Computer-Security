import os
from sklearn.model_selection import train_test_split

curDir = os.getcwd()
norDir = "/API/000/"
malDir = "/API/111/"

nTrain, nTest = list(), list()
mTrain, mTest = list(),list()

map_api = dict()
map_key = 0

nTrain_TF = dict()
mTrain_TF = dict()
nTest_TF = dict()
mTest_TF = dict()

nTrain_rate = dict()
mTrain_rate = dict()

filter_rate = 0.00058
# error_rate = 0.000078
error_rate = 0.00009

nTon = 0
nTom = 0
mTon = 0
mTom = 0


def makeTrainTestset() :
    global nTest, nTrain, mTest, mTrain

    nfiles = os.listdir(curDir+norDir)
    mfiles = os.listdir(curDir+malDir)

    nTrain, nTest = train_test_split(nfiles, random_state=100)
    mTrain, mTest = train_test_split(mfiles, random_state=100)

    print("nTrain count : "+ str(len(nTrain)) + "  nTest count : " + str(len(nTest)) )
    print("mTrain count : "+ str(len(mTrain)) + "  mTest count : " + str(len(mTest)) )
    # print(nTrain, nTest)
    # print(mTrain, mTest)


def make4gram(filename) :
    global map_api, map_key

    apis = list()
    ret = list()

    f = open(filename,"r")
    while True :
        sentence = f.readline()
        if not sentence : break
        apis.append(sentence)
        if sentence not in map_api :
            map_api[sentence] = str(map_key)
            map_key += 1
    f.close()

    for i in range(len(apis)-4):
        tmp =  map_api[apis[i]] +  map_api[apis[i+1]] +  map_api[apis[i+2]] + map_api[apis[i+3]]
        ret.append(tmp)

    # print("\n\nmake4gram")
    # print(ret)
    # print(map_api)
    # a = 0
    # print("len ret")
    # print(len(ret))

    return ret

def TFaboutFile(filename) :
    tmp_TF = dict()
    ngram = make4gram(filename)
    
    for i in ngram :
        if i not in tmp_TF :
            tmp_TF[i] = 1
        else :
            tmp_TF[i] += 1

    # print("TFaboutFile")
    # print(tmp_TF)
    # a = 0
    # for i in tmp_TF.values():
    #     a += i
    # print("a")
    # print(a)

    return tmp_TF

def TFaboutNtrainset() :
    global nTrain, nTrain_TF, error_rate
    tmp_nTrain = dict()
    
    for i in nTrain :
        
        if not (i.endswith(".txt")) :
            continue
        # print("IN TFaboutNtrainset file name : "+i)
        tmp_TF = TFaboutFile(curDir + norDir + i)
        
        for j in tmp_TF.keys():
            
            if j not in tmp_nTrain :
                tmp_nTrain[j] = 1
            else :
                tmp_nTrain[j] += 1
    
    total_count = 0
    for i in tmp_nTrain.values():
        total_count += float(i)
    for i in tmp_nTrain.keys() :
        tmp_nTrain[i] = float(tmp_nTrain[i]) / total_count
        
    
    
    for i in tmp_nTrain.keys() :
        nTrain_TF[i] = tmp_nTrain[i]

    print("len nTrain_TF")
    print(len(nTrain_TF))
    
            
    

def TFaboutMtrainset() :
    global mTrain, mTrain_TF, error_rate, nTrain
    tmp_mTrain = dict()
    
    for i in mTrain :
        if not (i.endswith(".txt")) :
            continue
        # print("IN TFaboutMtrainset file name : "+i)
        tmp_TF = TFaboutFile(curDir + malDir + i)
        
        for j in tmp_TF.keys():
            
            if j not in tmp_mTrain :
                tmp_mTrain[j] = 1
            else :
                tmp_mTrain[j] += 1

    total_count = 0.0
    for i in tmp_mTrain.values():
        total_count += float(i)
    for i in tmp_mTrain.keys() :
        tmp_mTrain[i] = float(tmp_mTrain[i]) / total_count
    
    for i in nTrain_TF.keys() :
        tmp_mTrain[i] = 0.0
    
    print("len tmp_mTrain")
    print(len(tmp_mTrain))
    print("max tmp_mTrain value")
    print(max(tmp_mTrain.values()))


    for i in tmp_mTrain.keys() :
        if tmp_mTrain[i] >= error_rate :
            mTrain_TF[i] = tmp_mTrain[i]

    
    for i in tmp_mTrain.keys() :
        if tmp_mTrain[i] >= error_rate :
            mTrain_TF[i] = tmp_mTrain[i]
            
    print("total_count")
    print(total_count)
    print("mTrain_TF")
    print(mTrain_TF)
    print("len mTrain_TF")
    print(len(mTrain_TF))
    

    # print("\n\nTFaboutMtrainset")        
    # print(mTrain_TF)

def analysisNtest() :
    global nTest, mTrain_TF, nTon, nTom
    detect_filter = mTrain_TF.keys()
    for i in nTest :
        if not (i.endswith(".txt")) :
            continue
        # print("In analysisNtest file name : " + i)
        tmp_nTest = TFaboutFile(curDir + norDir + i)
        
        for i in tmp_nTest.keys() :
            if i in detect_filter :
                nTom += 1
                break
    nTon = len(nTest) - nTom
    
    print("Total test num : "+str(len(nTest)))
    print("Result analysisNtest nton :"+str(nTon)+", ntom : "+str(nTom))

def analysisMtest() :
    global mTest, mTrain_TF, mTon, mTom
    detect_filter = mTrain_TF.keys()
    for i in mTest :
        if not (i.endswith(".txt")) :
            continue
        # print("In analysisMtest file name : " + i)
        tmp_mTest = TFaboutFile(curDir + malDir + i)
        for i in tmp_mTest.keys() :
            if i in detect_filter :
                mTom += 1
                break
    mTon = len(mTest) - mTom

    print("Total test num : "+str(len(mTest)))
    print("Result analysisMtest mton :"+str(mTon)+", mtom : "+str(mTom))
orinTon = 0
orinTom = 0
orimTon = 0
orimTom = 0
def analysisoriNtest() :
    global nTrain, mTrain_TF, orinTon, orinTom
    detect_filter = mTrain_TF.keys()
    for i in nTrain :
        if not (i.endswith(".txt")) :
            continue
        # print("In analysisMtest file name : " + i)
        tmp_nTrain = TFaboutFile(curDir + norDir + i)
        for i in tmp_nTrain.keys() :
            if i in detect_filter :
                orinTom += 1
                break
    orinTon = len(nTrain) - orinTom

    print("Total test num : "+str(len(nTrain)))
    print("Result analysisoriNtest nton :"+str(orinTon)+", ntom : "+str(orinTom))

def analysisoriMtest() :
    global mTrain, mTrain_TF, orimTon, orimTom
    detect_filter = mTrain_TF.keys()
    for i in mTrain :
        if not (i.endswith(".txt")) :
            continue
        # print("In analysisMtest file name : " + i)
        tmp_mTrain = TFaboutFile(curDir + malDir + i)
        for i in tmp_mTrain.keys() :
            if i in detect_filter :
                orimTom += 1
                break
    orimTon = len(mTrain) - orimTom

    print("Total test num : "+str(len(mTrain)))
    print("Result analysisMtest mton :"+str(orimTon)+", mtom : "+str(orimTom))

makeTrainTestset()
TFaboutNtrainset()
TFaboutMtrainset()
analysisNtest()
analysisMtest()
analysisoriNtest()
analysisoriMtest()

# makeTrainTestset()
#ngram & file TF test
# make4gram(curDir + norDir + "1.txt")
# make4gram(curDir + malDir + "1.txt")
# TFaboutFile(curDir + norDir + "1.txt")
# TFaboutFile(curDir + malDir + "1.txt")

#file set TF test
# nTrain.append("1.txt")
# mTrain.append("1.txt")
# nTrain.append("2.txt")
# mTrain.append("2.txt")
# TFaboutNtrainset()
# TFaboutMtrainset()

# anaylsis test
# nTrain.append("1.txt")
# mTrain.append("1.txt")
# nTrain.append("2.txt")
# mTrain.append("2.txt")
# nTest.append("1.txt")
# mTest.append("1.txt")
# nTest.append("2.txt")
# mTest.append("2.txt")
# TFaboutNtrainset()
# TFaboutMtrainset()
# analysisNtest()
# analysisMtest()