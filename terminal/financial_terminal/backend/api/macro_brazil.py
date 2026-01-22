import pandas as pd
import yfinance as yf
from bcb import sgs

def get_brazil_macro_data():
    """Busca dados oficiais do Banco Central e Mercado."""
    try:
        # Códigos SGS: Selic Meta: 432 | IPCA Mensal: 433 | IPCA 12m: 13522
        selic = sgs.get({'Selic': 432}, last=1).iloc[0,0]
        ipca_m = sgs.get({'IPCA_M': 433}, last=1).iloc[0,0]
        
        # Dados via Yahoo Finance (Preços de fechamento/atual)
        tickers = {
            "Ibovespa": "^BVSP",
            "Dólar Ptax": "USDBRL=X",
            "DI": "DI=F" # Simplificado para exemplo
        }
        
        market_data = {}
        for label, ticker in tickers.items():
            data = yf.Ticker(ticker).history(period="1d")
            market_data[label] = data['Close'].iloc[-1]

        return {
            "Selic Meta": f"{selic:.2f}%",
            "IPCA Mensal": f"{ipca_m:.2f}%",
            "Ibovespa": f"{market_data['Ibovespa']:,.0f}".replace(",", "."),
            "Dólar": f"R$ {market_data['Dólar']:,.2f}"
        }
    except Exception as e:
        return {"Erro": str(e)}