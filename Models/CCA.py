import numpy
from sklearn.cross_decomposition import CCA



class CCAModel:
    def __init__(self, target_frequencies, samplingRate):
        '''

        :param frequencies: dic
            flicker的频率
            e.g. {'up': 8, 'down': 15}
        :param samplingRate: float


        '''
        self.signalHeader = None
        self.stimLabel = None
        self.stimCode = None
        self.target_frequencies = target_frequencies
        self.samplingRate = samplingRate
        self.numTargs = None
        self.prevTime = 0
        self.targets = list(target_frequencies.keys())

    def predict(self, eeg_signals, win_size):
        '''

        :param eeg_signals: vector
            [#channels, #samples]
        :param win_size: float
            单位为second
        :return:
            (target, confidence)
        '''
        n_samps = win_size * self.samplingRate
        ref_signals = []
        for freq in self.target_frequencies.values():
            _tmp_ref_sig = self.getReferenceSignals(n_samps, freq)
            ref_signals.append(_tmp_ref_sig)

        n_components = 2
        # Concatenate all templates into one matrix
        ref_signals = numpy.array(ref_signals)
        # Compute CCA
        result = self.findCorr(n_components, eeg_signals, ref_signals)
        # Find the maximum canonical correlation coefficient and corresponding class for the given SSVEP/EEG data
        max_result = max(result, key=float)
        predictedClass = numpy.argmax(result)
        # Print the predicted class label
        print("识别结果：", max_result, self.targets[predictedClass])


    def getReferenceSignals(self, length, target_freq):
        # generate sinusoidal reference templates for CCA for the first and second harmonics
        reference_signals = []
        t = numpy.arange(0, (length / (self.samplingRate)), step=1.0 / (self.samplingRate))
        # First harmonics/Fundamental freqeuncy
        reference_signals.append(numpy.sin(numpy.pi * 2 * target_freq * t))
        reference_signals.append(numpy.cos(numpy.pi * 2 * target_freq * t))
        # Second harmonics
        reference_signals.append(numpy.sin(numpy.pi * 4 * target_freq * t))
        reference_signals.append(numpy.cos(numpy.pi * 4 * target_freq * t))
        reference_signals = numpy.array(reference_signals)
        return reference_signals    # samps

    def findCorr(self, n_components, numpyBuffer, freq):
        # Perform Canonical correlation analysis (CCA)
        # numpyBuffer - consists of the EEG
        # freq - set of sinusoidal reference templates corresponding to the flicker frequency
        cca = CCA(n_components)
        corr = numpy.zeros(n_components)
        result = numpy.zeros((freq.shape)[0])
        for freqIdx in range(0, (freq.shape)[0]):
            cca.fit(numpyBuffer.T, numpy.squeeze(freq[freqIdx, :, :]).T)
            O1_a, O1_b = cca.transform(numpyBuffer.T, numpy.squeeze(freq[freqIdx, :, :]).T)
            indVal = 0
            for indVal in range(0, n_components):
                corr[indVal] = numpy.corrcoef(O1_a[:, indVal], O1_b[:, indVal])[0, 1]
            result[freqIdx] = numpy.max(corr)
        return result


