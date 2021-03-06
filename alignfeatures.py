import neuralnet as nn
import activation as act
import numpy as np

#chordFile = open('data/table.txt', 'r')
chordFile = open('data/chordinonoenharmonic.txt', 'r')
#featureFName = 'audio_vamp_nnls-chroma_nnls-chroma_logfreqspec.csv'
featureFName = 'audio_vamp_nnls-chroma_nnls-chroma_bothchroma.csv'
dataOut = open('data/gtruth_chroma_enharmonic.csv', 'w')

'''
nnStruct = [256,24]

# Set up neural network
# uses sigmoid activation function by default at each layer
# output activation depends on the type of chromaNorm specified
activations = [act.Sigmoid()] * (len(nnStruct)-2)
# partitioned SoftMax output (L1 normalization for each chromagram)
activations.append(act.SoftMax([12]))

# Instantiate neural network
# assumes full connectivity between layer neurons.
net = nn.NeuralNet(nnStruct, actFunc=activations)

# load in trained weights
wstar = np.load("trainedweights/wstar_grad_KLDiv_[0]_0.75_10pass.npy")
net.setWeights(wstar)
'''

prevFeatureFileNum = -1
featureFile = None
for i, cLine in enumerate(chordFile):
    # skip header
    if i == 0:
        continue

    cLine.strip()
    gTruth = cLine.split(",")

    sid = gTruth[0]
    chordTime = gTruth[1]

    if sid != prevFeatureFileNum:
        # close previous feature file
        if featureFile:
            featureFile.close()

        # grab new feature file
        featureFileName = "data/burgoyne2011chords/" + sid.zfill(4) + "/" + featureFName
        print "processing: ", featureFileName
        featureFile = open(featureFileName, 'r')

    '''
    for table.txt (enharmonicities enabled)
    # 0, 1, 7, 10, 11, 12, 13
    # sid, timestamp, local.tonic.name, root.name, root.pc, quality, simple.quality
    outVec = gTruth[0:2]
    outVec.append(gTruth[7])
    outVec.extend(gTruth[10:14])
    '''

    '''
    for chordinonoenharmonic.txt (enharmonicities disabled)
    '''
    # 0,1,7,10,11,12
    # sid, timestamp, local.tonic.pc, root.pc, quality, simple.quality
    outVec = gTruth[0:2]
    outVec.append(gTruth[7])
    outVec.extend(gTruth[10:13])

    # get features
    obsLine = featureFile.readline()
    obsLine.strip()
    
    if not obsLine:
        continue

    obsLine = obsLine.split(",")
    
    # check timestamps are aligned
    if not np.allclose(float(chordTime), float(obsLine[0])):
        raise ValueError("chord timestamp did not match feature timestamp for file: " + featureFile.name)

    # run through neural net
    obs = np.asfarray(obsLine[1:])
    
    '''
    # feature normalizaton 'L1' for neural network input
    if np.sum(obs) == 0:
        output = np.zeros(net.K)
    else:
        obs /= np.sum(np.abs(obs))
        output = net.calcOutput(obs)

    output = map(str, np.round(output.squeeze(),6))  
    '''

    output = map(str, np.round(obs.squeeze(),6))

    outVec.extend(output)

    outLine = ','.join(outVec)

    dataOut.write(outLine + '\n')

    prevFeatureFileNum = sid

print "Success ... cleaning file pointers"

chordFile.close()
featureFile.close()
dataOut.close()

print "All Done!"
