using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;

namespace NedbankRpa.Services
{
    public class RelatorioService
    {
        private string downloadPath;
        private string relatorioPath;

        private Dictionary<string, (string Documento, string Dept, string Obs)> dadosComplementares =
            new Dictionary<string, (string Documento, string Dept, string Obs)>
        {
            { "Carla Nhantumbo", ("BI 456789 AA", "Recursos Humanos", "Verificar cálculo de bónus.") },
            { "Tomás Cossa", ("BI 987654 BB", "Financeiro", "Confirmar valor de alimentação.") },
            { "Elsa Mucave", ("BI 123456 CC", "Jurídico", "Sem bónus este mês.") },
            { "Inês Mabunda", ("BI 654321 DD", "Marketing", "Internet incluída como benefício.") },
            { "Júlio Matusse", ("BI 321987 EE", "Logística", "Bónus reduzido por faltas.") }
        };

        public RelatorioService(string downloadPath)
        {
            this.downloadPath = downloadPath;
            relatorioPath = Path.Combine(downloadPath, "balancete_consolidado.txt");
        }

        public List<(string Codigo, string Nome, string Contato, string Email, string EstadoCivil, string Periodo,
                     string Vencimentos, string Bonus, string Seguros, string Outros, string SalarioLiquido,
                     string Pagamento, string Referencia, string Assinatura, string Data)> ProcessarArquivos()
        {
            var registros = new List<(string, string, string, string, string, string, string, string, string, string, string, string, string, string, string)>();
            var arquivos = Directory.GetFiles(downloadPath, "*.txt").Where(f => !f.EndsWith("balancete_consolidado.txt")).ToList();

            foreach (var arquivo in arquivos)
            {
                string conteudo = File.ReadAllText(arquivo, Encoding.UTF8);
                var padrao = @"--- Registro: (R-\d+) \| Mês: .+? ---\s*" +
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

                var match = Regex.Match(conteudo, padrao, RegexOptions.Singleline);

                if (match.Success)
                {
                    registros.Add((
                        match.Groups[1].Value.Trim(),
                        match.Groups[2].Value.Trim(),
                        match.Groups[3].Value.Trim(),
                        match.Groups[4].Value.Trim(),
                        match.Groups[5].Value.Trim(),
                        match.Groups[6].Value.Trim(),
                        match.Groups[7].Value.Trim(),
                        match.Groups[8].Value.Trim(),
                        match.Groups[9].Value.Trim(),
                        match.Groups[10].Value.Trim(),
                        match.Groups[11].Value.Trim(),
                        match.Groups[12].Value.Trim(),
                        match.Groups[13].Value.Trim(),
                        match.Groups[14].Value.Trim(),
                        match.Groups[15].Value.Trim()
                    ));
                    Console.WriteLine($"Registro extraído: {match.Groups[2].Value.Trim()}");
                }
            }

            return registros;
        }

        public void GerarRelatorio(List<(string Codigo, string Nome, string Contato, string Email, string EstadoCivil,
                                           string Periodo, string Vencimentos, string Bonus, string Seguros, string Outros,
                                           string SalarioLiquido, string Pagamento, string Referencia, string Assinatura, string Data)> registros)
        {
            var sb = new StringBuilder();

            foreach (var reg in registros)
            {
                var complementos = dadosComplementares.ContainsKey(reg.Nome)
                    ? dadosComplementares[reg.Nome]
                    : ("N/D", "N/D", "N/D");

                string referenciaFinal = reg.Referencia.Replace(reg.Codigo + "-02", "RCB-" + reg.Codigo.Replace("R-", ""));

                sb.AppendLine($"--- Registro: {reg.Codigo} ---");
                sb.AppendLine($"Nome: {reg.Nome}");
                sb.AppendLine($"Contacto / Tel: {reg.Contato}");
                sb.AppendLine($"E-mail: {reg.Email}");
                sb.AppendLine($"Estado Civil: {reg.EstadoCivil}");
                sb.AppendLine($"Documento: {complementos.Item1}");
                sb.AppendLine($"Dept.: {complementos.Item2}");
                sb.AppendLine($"Período: {reg.Periodo}");
                sb.AppendLine($"Vencimentos brutos: {reg.Vencimentos}");
                sb.AppendLine($"Bónus: {reg.Bonus}");
                sb.AppendLine($"Seguros: {reg.Seguros}");
                sb.AppendLine($"OUTROS: {reg.Outros}");
                sb.AppendLine($"Salário Líquido: {reg.SalarioLiquido}");
                sb.AppendLine($"Pagamento via: {reg.Pagamento}");
                sb.AppendLine($"Referência recibo: {referenciaFinal}");
                sb.AppendLine($"Obs.: {complementos.Item3}");
                sb.AppendLine($"Assinatura gestor: {reg.Assinatura}");
                sb.AppendLine($"Data: {reg.Data}");
                sb.AppendLine($"--- END Registro: {reg.Codigo} ---\n");
            }

            File.WriteAllText(relatorioPath, sb.ToString(), Encoding.UTF8);
            Console.WriteLine($"\nRelatório final salvo em: {relatorioPath}");
        }
    }
}
