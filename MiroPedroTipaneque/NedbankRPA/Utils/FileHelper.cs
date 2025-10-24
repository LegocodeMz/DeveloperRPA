namespace NedbankRpa.Utils
{
    public static class FileHelper
    {
        public static bool WaitDownload(string downloadPath, string fileName, int timeout = 30)
        {
            string filePath = Path.Combine(downloadPath, fileName);
            string tempFilePath = filePath + ".crdownload";

            var stopwatch = System.Diagnostics.Stopwatch.StartNew();

            while (!File.Exists(filePath))
            {
                 /*
                 * JUSTIFICATION: Early exit check after 5 seconds
                 * - Optimization to avoid waiting full 30 seconds for non-existent files
                 * - If neither final nor temp file exists after 5s, download likely failed
                 * - Saves 25 seconds per failed download
                 * - Improves overall execution time when files unavailable
                 */
                if (!File.Exists(tempFilePath) && stopwatch.Elapsed.TotalSeconds > 5)
                    return false;

                /*
                 * JUSTIFICATION: 500ms sleep interval
                 * - Balance between responsiveness and CPU usage
                 * - Too short (e.g., 100ms) wastes CPU cycles
                 * - Too long (e.g., 2000ms) delays detection of completion
                 * - 500ms is standard polling interval for file operations
                 * - Minimal impact on overall execution time
                 */
                Thread.Sleep(500);

                 /*
                 * JUSTIFICATION: Timeout check after 30 seconds
                 * - Prevents infinite loops on stuck downloads
                 * - 30 seconds sufficient for most file sizes in this context
                 * - Allows application to continue with other files
                 */
                if (stopwatch.Elapsed.TotalSeconds > timeout)
                    return false;
            }

            return true;
        }

        public static void ClearDirectory(string path)
        {
            Directory.CreateDirectory(path);
            foreach (var file in Directory.GetFiles(path, "*.txt"))
            {
                File.Delete(file);
            }
            Console.WriteLine("Pasta de downloads limpa.");
        }
    }
}
