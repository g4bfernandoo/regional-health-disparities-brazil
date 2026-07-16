# Raw Data Download Instructions

Raw data files are not included in this repository due to file size.
All sources are publicly available under Brazil's Lei de Acesso à Informação (Law 12,527/2011).

After downloading, your `data/raw/` folder should contain exactly these files:

```
data/raw/
├── mortalitybycity.csv
├── proceduresbycity.csv
├── population.csv
├── pib.csv
├── PA_Municipios_2022.cpg
├── PA_Municipios_2022.dbf
├── PA_Municipios_2022.prj
├── PA_Municipios_2022.shp
├── PA_Municipios_2022.shx
└── README.md  ← this file
```

---

## 1. Cardiovascular Mortality by Municipality (`mortalitybycity.csv`)

**Source:** DATASUS — Sistema de Informação sobre Mortalidade (SIM)  
**URL:** http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sim/cnv/obt10pa.def  
**Coverage:** Pará, 2019–2023 | ICD-10: I20–I25

**Steps:**
1. Access the URL above
2. **Linha (Row):** Município
3. **Coluna (Column):** Ano do Óbito
4. **Conteúdo (Content):** Óbitos p/ Residência
5. **Período:** Select 2019, 2020, 2021, 2022, 2023
6. **Capítulo CID-10:** IX. Algumas doenças do aparelho circulatório
7. **Grupo CID-10:** I20-I25 Doenças isquêmicas do coração
8. **Unidade da Federação:** Pará
9. Click **Mostra** → Click **Copia como .CSV**
10. Save as `data/raw/mortalitybycity.csv`

**Encoding:** latin-1 | **Separator:** semicolon (;) | **Header rows to skip:** 4

---

## 2. Cardiac Catheterization Procedures by Municipality (`proceduresbycity.csv`)

**Source:** DATASUS — Sistema de Informações Hospitalares (SIH-SUS)  
**URL:** http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sih/cnv/qipa.def  
**Coverage:** Pará, 2019–2023 | Procedure: cardiac catheterization (AIH)

**Steps:**
1. Access the URL above
2. **Linha:** Município
3. **Coluna:** Ano processamento
4. **Conteúdo:** AIH aprovadas
5. **Período:** Select 2019 through 2023
6. **Procedimento:** Search for "cateterismo cardíaco" and select all related codes
7. **Unidade da Federação:** Pará
8. Click **Mostra** → Click **Copia como .CSV**
9. Save as `data/raw/proceduresbycity.csv`

**Encoding:** latin-1 | **Separator:** semicolon (;) | **Header rows to skip:** 4

---

## 3. Municipal Population Estimates (`population.csv`)

**Source:** IBGE — Estimativas de População (SIDRA Table 6579)  
**URL:** https://sidra.ibge.gov.br/tabela/6579  
**Coverage:** Pará municipalities | Years: 2019, 2020, 2021, 2024

**Steps:**
1. Access the URL above
2. **Variável:** População residente estimada
3. **Ano:** Select 2019, 2020, 2021, 2024
4. **Município:** All municipalities in Pará (filter by UF = Pará)
5. Click **Download** → **CSV (separado por ponto e vírgula)**
6. Save as `data/raw/population.csv`

**Note:** 2022 and 2023 estimates were not available at the time of data extraction.
The 2021 estimate is used as the population baseline throughout the analysis (midpoint
of the 2019–2023 study period).

**Encoding:** utf-8-sig | **Separator:** semicolon (;) | **Header rows to skip:** 3

---

## 4. Municipal GDP (`pib.csv`)

**Source:** IBGE — Produto Interno Bruto dos Municípios (SIDRA)  
**URL:** https://sidra.ibge.gov.br/pesquisa/pib-munic/tabelas  
**Coverage:** Pará municipalities | Years: 2019, 2020, 2021, 2022, 2023  
**Unit:** Thousand reais (mil R$)

**Steps:**
1. Access the URL above
2. Select the most recent municipal GDP table
3. **Variável:** Produto Interno Bruto a preços correntes
4. **Ano:** Select 2019, 2020, 2021, 2022, 2023
5. **Município:** All municipalities in Pará (filter by UF = Pará)
6. Click **Download** → **CSV (separado por ponto e vírgula)**
7. Save as `data/raw/pib.csv`

**Encoding:** utf-8-sig | **Separator:** semicolon (;) | **Header rows to skip:** 3

---

## 5. Municipal Boundary Shapefile (`PA_Municipios_2022.*`)

**Source:** IBGE — Malhas Territoriais Municipais  
**URL:** https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2022/UFs/PA/  
**Coverage:** Pará municipalities | Reference year: 2022

**Steps:**
1. Access the URL above
2. Download `PA_Municipios_2022.zip`
3. Extract all files into `data/raw/`
4. Confirm the following files are present:
   - `PA_Municipios_2022.shp` — polygon geometries
   - `PA_Municipios_2022.shx` — spatial index
   - `PA_Municipios_2022.dbf` — attribute table (includes `CD_MUN` = 7-digit IBGE code)
   - `PA_Municipios_2022.prj` — coordinate reference system
   - `PA_Municipios_2022.cpg` — character encoding

**Note:** The `CD_MUN` field in the shapefile uses 7-digit IBGE codes. The analysis
pipeline truncates to 6 digits to match the DATASUS coding standard:
`mapa['CD_MUN'] = mapa['CD_MUN'].astype(str).str[:6]`

---

## Data Access Dates

All datasets were accessed from publicly available DATASUS and IBGE repositories
in June–July 2025. At no point did the authors have access to information that could
identify individual participants; all data were obtained as aggregate municipality-level
statistics.

---

## Known Data Issues

| Issue | File | How handled in notebook 01 |
|---|---|---|
| latin-1 encoding | mortalitybycity.csv, proceduresbycity.csv | `encoding='latin-1'` |
| utf-8-sig with BOM | population.csv, pib.csv | `encoding='utf-8-sig'` |
| 4 header rows before data | DATASUS files | `skiprows=4` |
| 3 header rows + legal notes | IBGE files | `skiprows=3` |
| Municipality name mismatch | DATASUS vs IBGE | `normalize()` function + `manual_overrides` |
| Eldorado dos/do Carajás spelling | mortalitybycity.csv vs pib.csv | Manual override in `name_to_code` dict |
| 7-digit IBGE codes in shapefile | PA_Municipios_2022.shp | `.str[:6]` truncation |
| Values `"-"` or `"..."` in DATASUS | mortalitybycity.csv | `pd.to_numeric(..., errors='coerce').fillna(0)` |

---

*For questions about data access or pipeline issues, open an issue at:*  
*https://github.com/g4bfernandoo/regional-health-disparities-brazil/issues*
