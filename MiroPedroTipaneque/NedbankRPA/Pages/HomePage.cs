using OpenQA.Selenium;
using OpenQA.Selenium.Support.UI;
using SeleniumExtras.WaitHelpers;

namespace NedbankRpa.Pages
{
    /*
     * JUSTIFICATION: Primary constructor syntax (C# 12)
     * - Concise dependency injection pattern
     * - IWebDriver injected from caller
     * - Creates private readonly field automatically
     * - Reduces boilerplate code
     */
    public class BalanceSheetPage(IWebDriver driver)
    {
        private readonly IWebDriver driver = driver;

        /*
         * JUSTIFICATION: WebDriverWait with 10-second timeout
         * - Enables smart waiting (polls until condition met)
         * - Created once, reused for multiple wait operations
         */
        private readonly WebDriverWait wait = new(driver, TimeSpan.FromSeconds(10));

        public void NavigateTo(string url)
        {
            driver.Navigate().GoToUrl(url);
            driver.Manage().Window.Maximize();
            Console.WriteLine($"Navigating to: {url}");
        }

/*
         * JUSTIFICATION: DownloadFiles method returns List<string>
         * - Returns list of successfully downloaded filenames
         * - Allows caller to verify which files were downloaded
         * - Useful for validation or reporting
         */
        public List<string> DownloadFiles(string downloadPath)
        {
            var downloadedFiles = new List<string>();

            // a.btn.btn-success: Anchor tags with green download button styling
            var buttons = driver.FindElements(By.CssSelector("table tbody tr a.btn.btn-success"));
            int counter = 1;

            foreach (var button in buttons)
            {
                string fileName = button.GetAttribute("download") ?? $"Anexo_{counter}.txt";
                ((IJavaScriptExecutor)driver).ExecuteScript("arguments[0].scrollIntoView(true);", button);

                try
                {
                    wait.Until(ExpectedConditions.ElementToBeClickable(button));
                    button.Click();

                    if (Utils.FileHelper.WaitDownload(downloadPath, fileName))
                    {
                        Console.WriteLine($"File downloaded: {fileName}");
                        downloadedFiles.Add(fileName);
                    }
                    else
                    {
                        Console.WriteLine($"File unavailable: {fileName}");
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error while downloading '{fileName}': {ex.Message}");
                }
                counter++;
            }

            return downloadedFiles;
        }
    }
}
