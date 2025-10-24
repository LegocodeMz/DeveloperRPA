using System.Text;
using System.Text.RegularExpressions;

namespace NedbankRpa.Services
{
    /*
     * JUSTIFICATION: Primary constructor syntax (C# 12)
     * - Concise parameter declaration
     * - Automatically creates private field
     * - Reduces boilerplate code
     * - Modern C# feature for cleaner code
     */
    public class ReportService(string downloadPath)
    {
        private readonly string downloadPath = downloadPath;

        /*
         * JUSTIFICATION: Report path derived from download path
         * - Keeps all output in same directory
         * - Path.Combine ensures correct path separators
         */
        private readonly string reportPath = Path.Combine(downloadPath, "GenericReport.txt");

        /*
         * JUSTIFICATION: ProcessFiles returns List of tuples
         * - Simple data structure for temporary data
         * - No need for full class definition for intermediate processing
         * - Efficient for read-only data transfer
         */
        public List<(string code, string name, string contact, string email, string maritalState, string netSalary)> ProcessFiles()
        {
            var records = new List<(string, string, string, string, string, string)>();

            /*
             * JUSTIFICATION: Directory.GetFiles with pattern filter
             * - Gets only .txt files (downloaded files)
             * - Returns array which is converted to List
             * - Ensures we only process relevant files
             */
            var files = Directory.GetFiles(downloadPath, "*.txt").ToList();
            foreach (var file in files)
            {
                string content = File.ReadAllText(file, Encoding.UTF8);

                 /*
                 * JUSTIFICATION: Comprehensive Regex pattern
                 * - Single pattern extracts all required fields at once
                 * - Named capture groups would improve readability but aren't used here
                 * - \s* handles variable whitespace (robust against formatting variations)
                 * - .+? uses non-greedy matching (stops at next field)
                 * - Matches multi-line content with RegexOptions.Singleline
                 * 
                 * PATTERN BREAKDOWN:
                 * - Group 1: Registration code (R-\d+)
                 * - Group 2: Employee name
                 * - Group 3: Phone contact
                 * - Group 4: Email address
                 * - Group 5: Marital status
                 * - Groups 6-10: Other fields (not used in final output)
                 * - Group 11: Net salary (the key field needed)
                 */
                var pattern = @"--- Registro: (R-\d+) \| Mês: .+? ---\s*" +
                              @"Nome:\s*(.+?)\s*" +
                              @"Contacto / Tel:\s*(.+?)\s*" +
                              @"E-mail:\s*(.+?)\s*" +
                              @"Estado Civil:\s*(.+?)\s*" +
                              @"Período:\s*(.+?)\s*" +
                              @"Vencimentos brutos:\s*(.+?)\s*" +
                              @"Bónus:\s*(.+?)\s*" +
                              @"Seguros:\s*(.+?)\s*" +
                              @"OUTROS:\s*(.+?)\s*" +
                              @"Salário Líquido:\s*(.+?)\s*" +
                              @"Pagamento via:\s*(.+?)\s*" +
                              @"Referência recibo:\s*(.+?)\s*" +
                              @"Assinatura gestor:\s*(.+?)\s*" +
                              @"Data:\s*(.+?)\s*(?=---|$)";

                var match = Regex.Match(content, pattern, RegexOptions.Singleline);

                if (match.Success)
                {
                    /*
                     * JUSTIFICATION: Tuple construction with Trim()
                     * - Trim() removes leading/trailing whitespace
                     * - Essential because regex .+? may capture extra spaces
                     */
                    records.Add((
                        match.Groups[1].Value.Trim(), 
                        match.Groups[2].Value.Trim(),
                        match.Groups[3].Value.Trim(),
                        match.Groups[4].Value.Trim(),
                        match.Groups[5].Value.Trim(),
                        match.Groups[11].Value.Trim()
                    ));
                    Console.WriteLine($"Record extracted: {match.Groups[2].Value.Trim()}");
                }
            }

            return records;
        }

        /*
         * JUSTIFICATION: GenerateReport method with typed parameters
         * - Reuses same tuple structure from ProcessFiles
         * - Parameter names in tuple provide self-documentation
         * - Clear method signature shows exactly what data is expected
         * - Named tuple fields improve readability in method body
         */
        public void GenerateReport(List<(string code, string name, string email, string contact, string maritalStatus,
                                           string SalarioLiquido)> records)
        {
            var sb = new StringBuilder();

            foreach (var (code, name, email, contact, maritalState, netSalary) in records)
            {
                

                sb.AppendLine($"--- Registro: {code} ---");
                sb.AppendLine($"Nome: {name}");
                sb.AppendLine($"E-mail: {email}");
                sb.AppendLine($"Contacto / Tel: {contact}");
                sb.AppendLine($"Estado Civil: {maritalState}");
                sb.AppendLine($"Salário Líquido: {netSalary} ---\n");

            }

            /*
             * JUSTIFICATION: File.WriteAllText with UTF-8 encoding
             * - Single operation writes entire content
             * - UTF-8 encoding ensures Portuguese characters preserved
             * - Overwrites existing file (clean slate each run)
             * - ToString() converts StringBuilder to final string
             * 
             * ALTERNATIVE: StreamWriter for very large reports (not needed here)
             */
            File.WriteAllText(reportPath, sb.ToString(), Encoding.UTF8);
            
            Console.WriteLine($"\nFinal report saved in: {reportPath}");
        }
    }
}
