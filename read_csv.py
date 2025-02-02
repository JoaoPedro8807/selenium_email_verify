import pandas as pd


def read_csv() -> list[tuple[str, str]]:
    df = pd.read_csv("emails.csv").dropna()
    lista_emails_senha = [(email, senha) for email, senha in zip(df["email"], df["senha"])]

    return lista_emails_senha

if __name__ == "__main__":
    read_csv()