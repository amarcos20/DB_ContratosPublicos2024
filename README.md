[17:43, 27/11/2025] Afonso Marcos: Public Contracts Database Project (2024 Data)
This project focuses on creating a structured, comprehensive dimensional database from public procurement data for the year 2024. The primary goal is to perform a robust Extract, Transform, Load (ETL) process to normalize and integrate raw data from various sources into a clean, relational structure suitable for advanced analysis and Business Intelligence (BI) tools.

I. Project Objectives
Data Normalization and Transformation
Data Aggregation: Consolidate raw contract records from diverse original CSV files (e.g., adjudicators, awardees, CPV codes, location data).
Unification of Entities: Merge similar tables (e.g., adjudicators and awardees) and apply deduplication rules (based on NIF/Name) to create a single, …
[17:43, 27/11/2025] Afonso Marcos: # Public Contracts Database Project (2024 Data)

This project focuses on creating a structured, comprehensive *dimensional database* from public procurement data for the year *2024. The primary goal is to perform a robust Extract, Transform, Load (ETL*) process to normalize and integrate raw data from various sources into a clean, relational structure suitable for advanced analysis and Business Intelligence (BI) tools.

---

## I. Project Objectives

### Data Normalization and Transformation

* *Data Aggregation:* Consolidate raw contract records from diverse original CSV files (e.g., adjudicators, awardees, CPV codes, location data).
* *Unification of Entities:* Merge similar tables (e.g., adjudicators and awardees) and apply deduplication rules (based on NIF/Name) to create a single, unique *Entities* dimension table.
* *Structural Parsing:* Implement logic to split aggregated data fields into atomic components, such as separating *NIF* and *Name* from combined columns, or extracting *Country, District, and Municipality* from single location strings.
* *Specialized Extraction:* Utilize *Regular Expressions (Regex)* for complex parsing tasks, specifically to extract precise legal components (*Article, Number, Clause*) from the fundamentacao (legal basis) field.
* *Identifier Generation:* Ensure the creation of a unique, sequential integer *ID* column (starting at 1) for every record in each dimensional table, serving as the primary key.

---

## II. Technical Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| *Programming Language* | Python | Core scripting and execution of ETL logic. |
| *Data Manipulation* | *Pandas* | High-performance library essential for data loading, cleaning, transformation, splitting operations, and indexing. |
| *Parsing* | re (Regex Module) | Advanced pattern matching for complex text extraction (e.g., legal clauses). |
| *Data Storage* | [Specify your target database system, e.g., PostgreSQL / SQLite / SQL Server] | Final destination for the structured dimensional and fact tables. |

---

## III. Usage and Deliverables

### Deliverables

1.  *ETL Script (Data_modeling.ipynb):* The master Python script containing the full transformation, validation, and ID generation logic.
2.  *Cleaned Dimensional Files (.csv):* Standardized, deduplicated, and ID-indexed lookup tables (e.g., entities.csv, cpv_codes.csv, local_execution.csv).

### Execution

1.  *Dependencies:* Ensure Python and the Pandas library are installed.
    bash
    pip install pandas
    
2.  *Source Data:* Place all raw 2024 contract CSV files in the designated source directory structure as referenced by the processing script.
3.  *Run:* Execute the main processing script from the command line:
    bash
    python data_modeling.ipynb
    
4.  *Output:* Cleaned and normalized files will be generated, ready for import into the target relational database system.
