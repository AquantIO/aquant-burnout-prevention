import pandas as pd
class DetectSharpChangesWFuncInput:
    def __init__(self, df: pd.DataFrame, func, threshold: float = 0.5, detection_type: str = 'INCREASE', lookback_period: str='90D', output_type:str='summary', eval_col=None):
        self.df = df
        self.func = func
        self.threshold = threshold
        self.detection_type = detection_type
        self.lookback_period = lookback_period
        self.output_type = output_type
        self.eval_col = eval_col
