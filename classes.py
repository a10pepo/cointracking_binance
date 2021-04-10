

class Event():

    trans_type=""
    buy_amt=""
    buy_cur=""
    sell_amt=""
    sell_cur=""
    fee_amt=""
    fee_cur=""
    exchange=""
    trade_grp=""
    comment=""
    effective_date=None

    def __init__(self,trans_type: str=None, buy_amt: str=0.0, buy_cur: str=None, sell_amt: str=0.0,sell_cur: str=None, fee_amt: str=0.0, fee_cur: str=None, exchange: str=None, trade_grp: str=None, comment: str=None, effective_date: str=None):
        
        self.trans_type=trans_type
        
        self.buy_amt=str(buy_amt).replace(",","")
        self.buy_cur=buy_cur
        self.sell_amt=str(sell_amt).replace(",","")
        self.sell_cur=sell_cur
        self.fee_amt=str(fee_amt).replace(",","")
        self.fee_cur=fee_cur
        self.exchange=exchange
        self.trade_grp=trade_grp
        self.comment=comment
        self.effective_date=effective_date

    
    def to_string(self):
        return f"{self.trans_type},{self.buy_amt},{self.buy_cur},{self.sell_amt},{self.sell_cur},{self.fee_amt},{self.fee_cur},{self.exchange},{self.trade_grp},{self.comment},{self.effective_date}"