import streamlit as st
from functions import *

signals = []

uploaded_files = st.file_uploader("Upload a signal", type=["txt"], accept_multiple_files=True)

for file in uploaded_files:
    signals.append(Signal.fromUploadedFile(file))

operation = st.sidebar.selectbox(
    'Select Operation:',
    ('Add', 'Subtract', 'Multiply', "Fold", "Advance", "Delay")
)

const = 0
if operation in ("Advance", "Delay", "Multiply"):
    const = st.sidebar.number_input("Constant", value=1.0, step=1.0)

result = None

match operation:
    case "Add":
        result = AddSignals(signals)
    case "Subtract":
        if len(signals) != 2:
            st.error(f"Subtract needs exactly 2 signals, but {len(signals)} uploaded.")
        else:
            result = SubtractSignal(signals[0], signals[1])
    case "Multiply" | "Fold" | "Advance" | "Delay":
        if len(signals) != 1:
            st.error(f"{operation} needs exactly 1 signal, but {len(signals)} uploaded.")
        else:
            match operation:
                case "Multiply":
                    result = MultiplySignal(signals[0], const)
                case "Fold":
                    result = FoldSignal(signals[0])
                case "Advance":
                    result = AdvanceSignal(signals[0], const)
                case "Delay":
                    result = DelaySignal(signals[0], const)

if result is not None:
    tab1, tab2 = st.tabs(["Chart", "Dataframe"])
    df = pd.DataFrame({"Value": result.values}, index=result.indices)
    tab1.line_chart(df, height=450)
    tab2.dataframe(df, height=450)