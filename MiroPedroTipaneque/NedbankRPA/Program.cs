using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using NedbankRpa.Pages;
using NedbankRpa.Services;
using NedbankRpa.Utils;
using System;

namespace RPABalancete
{
    class Program
    {
        static void Main(string[] args)
        {
            string downloadPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), "Downloads", "RPA_Balancete");
            FileHelper.LimparPasta(downloadPath);

            var options = new ChromeOptions();
            options.AddUserProfilePreference("download.default_directory", downloadPath);
            options.AddUserProfilePreference("download.prompt_for_download", false);
            options.AddUserProfilePreference("disable-popup-blocking", "true");

            using (var driver = new ChromeDriver(options))
            {
                var pagina = new BalancetePage(driver);
                pagina.Navegar("https://rpa.xidondzo.com");

                var arquivosBaixados = pagina.BaixarArquivos(downloadPath);

                var relatorioService = new RelatorioService(downloadPath);
                var registros = relatorioService.ProcessarArquivos();
                relatorioService.GerarRelatorio(registros);

                driver.Quit();
            }

            Console.WriteLine("\nPressione qualquer tecla para sair...");
            Console.ReadKey();
        }
    }
}
