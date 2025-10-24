# Nedbank RPA - Balance Sheet Automation

RPA solution in C# with Selenium WebDriver to extract salary data from https://rpa.xidondzo.com and generate consolidated reports.

##  Features

- Automated web navigation and file downloads
- Data extraction using regex patterns
- Report generation (Name, Email, Phone, Marital Status, Net Salary)
- Page Object Model architecture
- Automated tests

##  Prerequisites

- .NET 6.0 SDK or higher
- Google Chrome (latest version)
- Visual Studio 2022 or VS Code (optional)

##  Quick Start

download challendge.zip
extract
```bash
cd NedbankRpa

# Restore packages
dotnet restore

# Build
dotnet build

# Run application
dotnet run
```

# Run tests
```bash
cd NedbankRpa.Tests
dotnet test
```

##  Project Structure

```
NedbankRpa/
├── Program.cs                    # Entry point and orchestration
├── Pages/
│   └── BalanceSheetPage.cs      # Page Object for web interactions
├── Services/
│   └── ReportService.cs         # Data processing and report generation
├── Utils/
│   └── FileHelper.cs            # File system utilities
└── NedbankRpa.Tests/            # Test project (xUnit)
    ├── Utils/FileHelperTests.cs
    ├── Services/ReportServiceTests.cs
    └── Pages/BalanceSheetPageTests.cs
```

##  Output

**Location**: `C:\Users\[Username]\Downloads\RPA_Balance_Sheet\GenericReport.txt`

**Format**:
```
--- Registro: R-1000 ---
Nome: Carla Nhantumbo
E-mail: c.nhantumbo@empresa.mz
Contacto / Tel: 84-123-456
Estado Civil: Solteira
Salário Líquido: MZN 16.050,00 ---
```

##  Testing

```bash
# Run all tests
dotnet test

# Run with details
dotnet test --verbosity detailed
```

**Test Coverage**: 18 tests covering FileHelper, ReportService, and BalanceSheetPage

##  Key Technologies

- **C# / .NET 6.0** - Core language and framework
- **Selenium WebDriver** - Browser automation
- **Page Object Model** - Design pattern for maintainability
- **xUnit** - Testing framework
- **Regex** - Data extraction from text files

##  Workflow

1. Navigate to https://rpa.xidondzo.com
2. Download all .txt salary documents
3. Extract data using regex patterns
4. Generate consolidated GenericReport.txt
5. Clean up and close browser

##  Notes

- Files are downloaded to `~/Downloads/RPA_Balance_Sheet/`
- UTF-8 encoding ensures Portuguese character support
- Download directory is cleaned before each run
- Integration tests use headless Chrome for CI/CD compatibility

---

**Developed for**: Nedbank RPA Challenge  
**Pattern**: Page Object Model  
**License**: Challenge-specific use only
