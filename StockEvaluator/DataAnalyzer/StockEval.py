from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

class Indicator_Plot():
    def __init__(self, df_stock):
        self.df_stock = df_stock

    def AD_ratio(self):
        money_flow_rate = (2*self.df_stock.iloc[:,3]-self.df_stock.iloc[:,2]
                           -self.df_stock.iloc[:,1]) / (self.df_stock.iloc[:,1]-self.df_stock.iloc[:,2])
            ## 0: open, 1: high, 2: low, 3: close, 4: volume
        money_flow_vol = money_flow_rate * self.df_stock.iloc[:,4]
        self.df_stock['moneyFlowVol'] = money_flow_vol
        self.df_stock['AD'] = self.df_stock['moneyFlowVol'].cumsum()

    def gen_plot(self):
        fig_sub = make_subplots(rows=2, cols=1, shared_xaxes = True)
        self.AD_ratio()
        trace1=go.Candlestick(x=self.df_stock.index, open=self.df_stock.iloc[:,0], high=self.df_stock.iloc[:,1],
                       low=self.df_stock.iloc[:,2], close=self.df_stock.iloc[:,3], name="stock_price")
        trace2 = go.Scatter(x=self.df_stock.index, y=self.df_stock['AD'], mode='lines', name="A/D ratio")
        fig_sub.add_trace(trace1,row=1,col=1)
        fig_sub.add_trace(trace2,row=2,col=1)
        fig_sub.update_layout(xaxis_rangeslider_visible=False)


        return fig_sub.to_json()
         
