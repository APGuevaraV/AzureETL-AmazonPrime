# AzureETL-AmazonPrime

Proyecto ETL construido con **Azure Data Factory**, **Azure Databricks** y **Azure Data Lake Storage Gen2**, siguiendo una arquitectura moderna basada en _Bronze / Silver / Gold Layers_.



## **Arquitectura General del Proyecto**

Este proyecto implementa un flujo ETL completo:

1.  **Ingesta (Bronze Layer)**
    
    -   Azure Data Factory copia un dataset en CSV desde GitHub hacia ADLS/Bronze.
        
2.  **Transformación (Silver / Gold Layer)**
    
    -   Databricks limpia, estandariza y genera datasets enriquecidos.
        
    -   Silver: Datos limpios y tipados.
        
    -   Gold: Datos listos para consumo analítico.
        
3.  **Orquestación**
    
    -   Pipelines de Databricks controlan la ejecución end-to-end.

**Estructura del Repositorio**

```txt
├── dataset/    
├── adf/                      
│   ├── pipeline/             
│   ├── dataset/              
│   ├── linkedService/                    
│
├── databricks/               
│   ├── notebooks/            
│   │   ├── Silver_Transformation.py
│   │   └── Golden_Transformation.py
│   │
│   ├── workflow/            
│   │   ├── job_etl.json
│   │
│   └── sql/                 
│       ├── create_external_location_bronze.sql
│       ├── create_external_location_silver.sql
│       └── create_external_location_gold.sql
│
├── docs/                     
│   └── arquitectura.png
│
└── README.md
```





## **1. Azure Data Factory – Artefactos**

En la carpeta **/adf** se incluyen los JSON exportados:

-   Pipelines:
    
    -   `CopyPrimeData.json`
        
-   Datasets:
    
    -   `ds_prime.json`
        
    -   `ds_prime_data.json`
        
-   Linked Services (sanitizados, sin credenciales):
    
    -   `ls_github.json`
        
    -   `ls_adlssmart1211.json`
        

## **2. Azure Databricks – Transformaciones**

Los notebooks ejecutan dos transformaciones principales:

###  Bronze → Silver

-   Limpieza
    
-   Eliminación de nulos
    
-   Tipificación de columnas
    
-   Estandarización de formatos
    

###  Silver → Gold

-   Agregaciones
    
-   Enriquecimiento
    
-   Preparación para analítica


## **3. Azure Data Lake – Organización**

El Data Lake se divide en 3 capas:
/bronze   → Datos crudos (ingestados)
/silver   → Datos limpios y estandarizados
/gold     → Datos listos para BI/Analytics



## **Flujo ETL Completo**

1.  ADF copia el dataset de GitHub → ADLS/Bronze.
    
2.  Databricks lee Bronze → genera Silver.
    
3.  Databricks genera el dataset Golden.
    
4.  Automatización con Jobs de Databricks


## Arquitectura propuesta
![Descripción de la imagen](docs/architecture.png)
