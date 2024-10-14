from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime, timedelta
import pandas as pd


SALESORDER_URL = "https://pathfinder.automationanywhere.com/challenges/salesorder-challenge.html?_gl=1*1coiioq*_gcl_au*MTQxODg0OTUyLjE3Mjg0MDgyNjQ.*_ga*MTA0NTQxMjQzLjE3Mjg0MDgyNjQ.*_ga_DG1BTLENXK*MTcyODQ5MDE5MS4yLjEuMTcyODQ5MTAwMC4yMC4wLjQ1NTk3MjE4MQ..&_fsi=H2XSK82c"
SALESORDER_URL_LOGIN = "https://pathfinder.automationanywhere.com/challenges/salesorder-applogin.html"
SALESORDER_URL_TRACKING = "https://pathfinder.automationanywhere.com/challenges/salesorder-tracking.html"

# Variáveis de usuário e senha
SALESORDER_USER = "douglasmcgee@catchycomponents.com"
SALESORDER_PASSWORD = "i7D32S&37K*W"

COMUNITY_USAR = "contatokennedylima@gmail.com"
COMUNITY_PASSWORD = "TestePyT2c"

class DesafioPage:
    def __init__(self, driver=None, timeout: int = 10):
        self.driver = driver or self.get_new_driver()
        self.timeout = timeout

    def get_new_driver(self):
        """ Método para configurar e retornar uma nova instância do WebDriver """
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')  # Maximiza a janela
        service = Service(ChromeDriverManager().install())  # Instala e configura o ChromeDriver automaticamente
        return webdriver.Chrome(service=service, options=options)

    def open(self, url):
        """ Abre uma URL no navegador """
        self.driver.get(url)
        print(f"Abrindo a URL: {url}")

    def switch_to_iframe(self,iframe):
        try:
            # Troca o foco para o iframe com ID ou nome 'e1menuAppIframe'
            iframe = self.find_element(By.ID, iframe)
            self.driver.switch_to.frame(iframe)
            print("Foco trocado para o iframe.")
        except TimeoutException:
            print("Erro: Iframe não encontrado.")

    def switch_to_default_content(self):
     # Retorna o foco para o conteúdo principal da página
        self.driver.switch_to.default_content()
        print("Foco trocado de volta para o conteúdo principal.")

    def find_element(self, by, value, timeout: int = None):
        """ Encontra um elemento na página com base em seu localizador """
        timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, value)))
        except TimeoutException:
            print(f"Elemento {value} não encontrado")
            raise

    def login(self):
        """ Realiza o login """
        self.open(SALESORDER_URL)
        print("Iniciando o processo de login")

        try:

            self.find_element(By.XPATH, "//*[@id='onetrust-accept-btn-handler']").click()

            # Efetua o click no campo Login por conta Comunity 
            self.find_element(By.XPATH, "//*[@id='button_modal-login-btn__iPh6x']").click()
            print('Click efetuado para login')

            self.find_element(By.XPATH, "//*[@id='43:2;a']").send_keys(COMUNITY_USAR)
            self.find_element(By.XPATH, "//*[@id='43:2;a']").send_keys(Keys.ENTER)
            print('Email incluido')


            self.find_element(By.XPATH, "//*[@id='10:152;a']").send_keys(COMUNITY_PASSWORD)
            self.find_element(By.XPATH, "//*[@id='10:152;a']").send_keys(Keys.ENTER)
            print('Senha incluida')

            self.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/div/a").click()
            print("Preparação pra login efetuada com sucesso.")


            handles = self.driver.window_handles
            self.driver.switch_to.window(handles[1])
            self.driver.refresh()

            # Acessar o campo de usuário
            self.find_element(By.XPATH, "//*[@id='salesOrderInputEmail']").send_keys(SALESORDER_USER)
            print("Usuário inserido")

            # Acessar o campo de senha
            self.find_element(By.XPATH, "//*[@id='salesOrderInputPassword']").send_keys(SALESORDER_PASSWORD)
            print("Senha inserida")

            # Clicar no botão de login
            self.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div/div/div[2]/div/form/a").click()
            print("Login realizado com sucesso")


            self.driver.execute_script(f"window.open('{SALESORDER_URL_TRACKING}', '_blank');")
            new_handles = self.driver.window_handles
            self.driver.switch_to.window(new_handles[2])  # Mudar para a nova aba
            print("aberto link para tracking ")


        except TimeoutException as e:
            print("Erro ao tentar fazer login: TimeoutException")
            raise e

    def nav(self):
        """ Efetuar Navegação """
        try:

            handles = self.driver.window_handles
            self.driver.switch_to.window(handles[1])
            self.driver.refresh()

            # Clicar no menu uma vez
            self.find_element(By.XPATH, "//*[@id='accordionSidebar']/li[6]/a/span").click()
            print("Click Menu")
            
            self.find_element(By.XPATH, "//*[@id='salesOrderDataTable_length']/label/select/option[3]").click()
            print("Efetuado a mudança para 50 itens na pagina")

        except TimeoutException as e:
            print("Erro ao tentar navegar")
            raise e
            
    def verificaItens(self):
        """ Verifica o status dos itens """
        # OBS: Como informado que nao seria necessario a mudança de paginas e escopo atual seria de 50 itens,
        # foi incluido um loop fixo mas poseria ser coletado numero total de itens na pagina 
        # para que fosse mais dinamico nesse caso 
        try:
            for i in range(1, 51):
                    xpath_SO_Num = f"//*[@id='salesOrderDataTable']/tbody/tr[{i}]/td[2]"
                    xoath_Status = f"//*[@id='salesOrderDataTable']/tbody/tr[{i}]/td[5]"

                    so_num = self.find_element(By.XPATH, xpath_SO_Num).text
                    order_status = self.find_element(By.XPATH, xoath_Status).text

                    if order_status in ["Confirmed", "Delivery Outstanding"]:
                        
                        table_itens = DesafioPage.coleta_informacoes_item(self, so_num, i)

                        DesafioPage.verificaTracing(self, table_itens, i)

                        print("Items status é igual a Confirmed ou Delivery Outstanding ")
                    else:
                        print("Items status diferente de Confirmed ou Delivery Outstanding ")
            pass
        
        except Exception as e:
            print(f"Erro ao coletar dados: {e}")
            raise e

    def coleta_informacoes_item(self, so_num, i):
        """ Verifica o status dos itens """
        try:

            self.find_element(By.CSS_SELECTOR, f".fas.fa-square-plus.i-{so_num}").click()
            #tableResults = self.find_element(By.XPATH, f'//*[@class="sales-order-items t-{so_num}"]/tbody/tr')
            rows = self.driver.find_elements(By.CSS_SELECTOR, f'.sales-order-items.t-{so_num} tbody tr')
            print(rows)
            table_itens = []

            #for row in rows:
            #    cells = row.find_elements(By.TAG_NAME, 'td')
            #    row_data = [cell.text for cell in cells]
            #   table_itens.append(row_data)
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')

                item = {
                    'itemName': cells[0].text,
                    'trackingNumber': cells[1].text,
                    'price': cells[2].text,
                    'quantity': cells[3].text,
                    'total': cells[4].text
                }
                table_itens.append(item)

            print(table_itens)

            return table_itens

            
            
        except Exception as e:
            print(f"Ocorreu um erro: {e}")   

    def verificaTracing(self, table_itens, i):
        """ Efetua a verificação no site finalizado em salesorder-tracking.html o status interno de cada item """
        try:
            
            #self.open(SALESORDER_URL_TRACKING)

            handles = self.driver.window_handles
            self.driver.switch_to.window(handles[2])
            self.driver.refresh()

            num_itens = []

            for item in table_itens:
                if len(item) > 1:
                    num = item['trackingNumber']

                    # Digitar o Tracking Number	
                    self.find_element(By.XPATH, "//*[@id='inputTrackingNo']").clear()
                    self.find_element(By.XPATH, "//*[@id='inputTrackingNo']").send_keys(num)
                    print("Tracking Number inserido")            

                    self.find_element(By.XPATH, "//*[@id='btnCheckStatus']").click()
                    print("click Track efetuado")

                    status_trackNum = self.find_element(By.XPATH, "//*[@id='shipmentStatus']/tr[3]/td[2]").text

                    if status_trackNum == "Delivered":

                        gerarInvoice = True
                        print("Status é Delivered")
                        
                    else:
                        gerarInvoice = False
                        print("Status diferente de Delivered")

            if gerarInvoice == True:
 
                #Efetuar a mudança do drive para a aba correta
                handles = self.driver.window_handles
                self.driver.switch_to.window(handles[1])


                #Efetuar o click no Generate Invoice de acordo com item atual
                self.find_element(By.XPATH, f"//*[@id='salesOrderDataTable']/tbody/tr[{i+1}]/td/table/tfoot/tr/td/button[1]").click()
            else:

                print("Status diferente de Delivered não foi gerado a invoice")
                #click Botão Close
                handles = self.driver.window_handles
                self.driver.switch_to.window(handles[1])


                self.find_element(By.XPATH, f"//*[@id='salesOrderDataTable']/tbody/tr[{i+1}]/td/table/tfoot/tr/td/button[2]").click()


        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    def close(self):
        """ Fecha o navegador """
        self.driver.quit()
        print("Navegador fechado")
        

BasePage = DesafioPage()  # Cria uma instância da página
BasePage.open(SALESORDER_URL)   # Abre a URL
BasePage.login()  # Realiza o login
BasePage.nav()  #Navegar para a pagina de coleta
BasePage.verificaItens() #Efetua a verificação de cada item e atriagem dos elegiveis para a pagina tracking
BasePage.close() #Fecha a sessao aberta para o procedimento no chrome