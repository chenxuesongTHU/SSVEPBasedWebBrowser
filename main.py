from Communication.DSIParser import DSIParser
import time
from Models.CCA import CCAModel


if __name__ == '__main__':
    parser = DSIParser('127.0.0.1', 8844)
    target_frequencies = {'up': 9, 'down': 12}
    parser.start()
    cca = CCAModel(target_frequencies=target_frequencies, samplingRate=parser.fsample)
    win_size = 3
    while True:
        time.sleep(win_size / 4)
        signalArray = None
        try:
            signalArray = parser.get_occipital_lobe_epoch(3)
        except:
            pass
        if type(signalArray) == type(None):
            continue
        if signalArray.shape[1] != parser.fsample * win_size:
            continue
        cca.predict(signalArray, win_size)
    parser.stop()
    print()

