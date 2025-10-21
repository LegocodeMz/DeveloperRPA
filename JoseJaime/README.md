# RPA Automation - .NET Selenium

![Logo do Projeto](/Screenshot 2025-10-21 235538.png)

## Introdução


> Este projeto é uma automação RPA desenvolvida em C# com Selenium, que acessa o website `rpa.xidondzo.com`, faz download de ficheiros de balancete salarial, extrai apenas os campos necessários (Nome, Email, Contacto, Estado Civil, Salário Líquido) e gera um CSV limpo e padronizado.

---

## Funcionalidades

- Navegar até o site alvo automaticamente.
- Identificar e baixar ficheiros de balancete salarial.
- Ler ficheiros `.txt` e extrair apenas os campos obrigatórios.
- Validar dados extraídos.
- Exportar os dados limpos para CSV.
- Logs detalhados do processamento.

---

## Pré-requisitos

Antes de correr o projeto, certifique-se de ter:

- [.NET SDK 7 ou superior](https://dotnet.microsoft.com/download)
- Google Chrome instalado
- Permissões de escrita na pasta de downloads temporária e na pasta `Exports` do projeto
- Conexão à internet

---

## Estrutura do Projeto

```
NBK_RPA_CS/
│
├── Config/           -> Configurações do projeto
├── Helpers/          -> Classes utilitárias (espera de elementos, alertas)
├── Services/         -> BotService, ExportService, LoggerService, Record.cs
├── Processors/       -> FileProcessor.cs
├── Program.cs        -> Ponto de entrada da aplicação
└── README.md
```

---

## Como Executar

1. Clone o projeto:

```bash
git clone https://github.com/thatgeekdev/NBK_RPA_CS.git
cd NBK_RPA_CS
```

2. Restaurar pacotes NuGet:

```bash
dotnet restore
```

3. Build do projeto:

```bash
dotnet build
```

4. Correr o projeto:

```bash
dotnet run
```

5. O bot irá:

- Abrir o Chrome em modo headless.
- Navegar até `https://rpa.xidondzo.com/`.
- Ler a tabela de balancete salarial.
- Fazer download dos ficheiros `.txt`.
- Extrair Nome, Email, Contacto, Estado Civil e Salário Líquido.
- Criar o CSV final em `Exports/BalanceteNedbank.csv`.

---

## Logs

Todos os logs são gravados em:

```
Logs/log.txt
```

Você pode abrir esse ficheiro para acompanhar passo a passo o que o bot realizou.

---

## Customização

- Para alterar a URL do site, abra `Config/ConfigService.cs` e edite a propriedade:

```csharp
public string StartUrl { get; private set; } = "https://rpa.xidondzo.com/";
```

- Para alterar a pasta de exportação, altere:

```csharp
public string ExportsPath { get; private set; } = "Exports";
```

---

## Captura de Tela / Imagem

Você pode adicionar uma imagem explicativa ou screenshot do projeto executando aqui:

```markdown
![Descrição da Imagem](\Screenshot 2025-10-21 235538.png)
```

---

## Autor

- José Jaime Matsimbe

---

## Licença
```
MIT License
```

