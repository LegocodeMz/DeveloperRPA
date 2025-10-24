using System;
using System.IO;
using System.Threading;

namespace NedbankRpa.Utils
{
    public static class FileHelper
    {
        public static bool AguardarDownload(string downloadPath, string fileName, int timeout = 30)
        {
            string filePath = Path.Combine(downloadPath, fileName);
            string tempFilePath = filePath + ".crdownload";

            var stopwatch = System.Diagnostics.Stopwatch.StartNew();

            while (!File.Exists(filePath))
            {
                // Se o arquivo não existir nem temporário depois de 5s, considera não disponível
                if (!File.Exists(tempFilePath) && stopwatch.Elapsed.TotalSeconds > 5)
                    return false;

                Thread.Sleep(500);

                if (stopwatch.Elapsed.TotalSeconds > timeout)
                    return false;
            }

            return true;
        }

        public static void LimparPasta(string path)
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
