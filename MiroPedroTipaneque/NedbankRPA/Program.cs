using OpenQA.Selenium.Chrome;
using NedbankRpa.Pages;
using NedbankRpa.Services;
using NedbankRpa.Utils;

/*
 * JUSTIFICATION: Using top-level statements (C# 9.0+)
 * - Reduces boilerplate code
 * - Cleaner entry point for simple console applications
 * - Still maintains full functionality without explicit Main method
 */


/*
* JUSTIFICATION: Download path construction using Environment.SpecialFolder
* - Avoids hardcoding specific user paths
* - Uses standard Downloads folder that all users have
* - Creates subdirectory "RPA_Balance_Sheet" to isolate application files
*/

string downloadPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), "Downloads", "RPA_Balance_Sheet");

/*
 * JUSTIFICATION: Clear directory before execution
 * - Ensures clean state for each run
 * - Prevents processing old/stale files from previous executions
 */
FileHelper.ClearDirectory(downloadPath);


/*
 * JUSTIFICATION: ChromeOptions configuration
 * - Enables automatic file downloads without user interaction (required for RPA)
 * - Sets custom download directory to control where files are saved
 * - Disables download prompts (prevents automation from hanging)
 * - Disables popup blocking (ensures download dialogs don't interrupt flow)
 */
var options = new ChromeOptions();
options.AddUserProfilePreference("download.default_directory", downloadPath);
options.AddUserProfilePreference("download.prompt_for_download", false);
options.AddUserProfilePreference("disable-popup-blocking", "true");

ChromeDriver driver = new(options);
BalanceSheetPage page = new(driver);
page.NavigateTo("https://rpa.xidondzo.com");

page.DownloadFiles(downloadPath);

ReportService reportService = new(downloadPath);
var records = reportService.ProcessFiles();

reportService.GenerateReport(records);

driver.Quit();
