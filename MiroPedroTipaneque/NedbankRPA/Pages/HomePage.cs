using OpenQA.Selenium;
using OpenQA.Selenium.Support.UI;
using SeleniumExtras.WaitHelpers;
using System;
using System.Collections.Generic;

namespace NedbankRpa.Pages
{
    public class BalancetePage
    {
        private IWebDriver driver;
        private WebDriverWait wait;

        public BalancetePage(IWebDriver driver)
        {
            this.driver = driver;
            wait = new WebDriverWait(driver, TimeSpan.FromSeconds(10));
        }

        public void Navegar(string url)
        {
            driver.Navigate().GoToUrl(url);
            driver.Manage().Window.Maximize();
            Console.WriteLine($"Navegando para: {url}");
        }

        public List<string> BaixarArquivos(string downloadPath)
        {
            var arquivosBaixados = new List<string>();
            var botoes = driver.FindElements(By.CssSelector("table tbody tr a.btn.btn-success"));
            int contador = 1;

            foreach (var botao in botoes)
            {
                string fileName = botao.GetAttribute("download") ?? $"Anexo_{contador}.txt";
                ((IJavaScriptExecutor)driver).ExecuteScript("arguments[0].scrollIntoView(true);", botao);

                try
                {
                    wait.Until(ExpectedConditions.ElementToBeClickable(botao));
                    botao.Click();

                    if (Utils.FileHelper.AguardarDownload(downloadPath, fileName))
                    {
                        Console.WriteLine($"Arquivo baixado: {fileName}");
                        arquivosBaixados.Add(fileName);
                    }
                    else
                    {
                        Console.WriteLine($"Arquivo não disponível: {fileName}");
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Erro ao baixar '{fileName}': {ex.Message}");
                }
                contador++;
            }

            return arquivosBaixados;
        }
    }
}
