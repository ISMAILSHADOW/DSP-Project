from collections import defaultdict
import pandas as pd
import test as t
import io

def ReadSignalStream(f):
    indices = []
    values = []
    for _ in range(4): 
        line = f.readline()
    while line:
        L=line.strip()
        if len(L.split(' '))==2:
            L=line.split(' ')
            V1=int(L[0])
            V2=float(L[1])
            indices.append(V1)
            values.append(V2)
            line = f.readline()
        else:
            break
    return indices, values


class Signal:
    def __init__(self, i : list[int], v : list[float]) -> None:
        self.indices = i
        self.values = v


    @classmethod
    def fromFile(cls, fileName):
        indices, values = t.ReadSignalFile(fileName)
        return cls(indices, values)


    @classmethod
    def fromDefaultDict(cls, dict : defaultdict):
        indices = []
        values = []
        for i, v in sorted(dict.items()):
            indices.append(i)
            values.append(v)
        return cls(indices, values)

    @classmethod
    def fromUploadedFile(cls, uploaded_file : io.BytesIO):
        text = uploaded_file.getvalue().decode("utf-8")
        indices, values = ReadSignalStream(io.StringIO(text))
        return cls(indices, values)


    def toDataFrame(self) -> pd.DataFrame:
        return pd.DataFrame(self.toDict())


    def toDict(self) -> defaultdict:
        result = defaultdict(float)
        for i, sig_index in enumerate(self.indices):
            result[sig_index] = self.values[i]
        return result 

    
def AddSignals(signals : list[Signal]) -> Signal:
    result = defaultdict(float)
    for signal in signals:
        for i, sig_index in enumerate(signal.indices):
            result[sig_index] += signal.values[i]
    return Signal.fromDefaultDict(result)


def MultiplySignal(signal : Signal, const : float) -> Signal:
    for i in range(len(signal.values)):
        signal.values[i] *= const
    return signal


def SubtractSignal(signal1 : Signal, signal2 : Signal) -> Signal:
    return AddSignals([signal1, MultiplySignal(signal2, -1)])


def FoldSignal(signal : Signal) -> Signal:
    result = defaultdict(float)
    for i, sig_index in enumerate(signal.indices):
        result[-sig_index] = signal.values[i]
    return Signal.fromDefaultDict(result)


def AdvanceSignal(signal : Signal, shift : float) -> Signal:
    result = defaultdict(float)
    for i, sig_index in enumerate(signal.indices):
        result[sig_index - shift] = signal.values[i]
    return Signal.fromDefaultDict(result)


def DelaySignal(signal : Signal, shift : float) -> Signal:
    result = defaultdict(float)
    for i, sig_index in enumerate(signal.indices):
        result[sig_index + shift] = signal.values[i]
    return Signal.fromDefaultDict(result)