# All necessary environment variables and where to find them

You will need to store a `secrets.toml` file in the `/app/.streamlit/` directory, which will contain all your environment variables. Besides that file, you will also need a `.env` file in the root of this project with the exact same keys.

The reason they are seperate files, is because when deploying a Streamlit application you have the option to store secret keys in the app itself, and that is what we did.

> `.toml` files require you to use " " around the values, whereas `.env` files do not

**note**: you will need to have made all resources before looking for these variables. Finding all keys will follow the same basic steps: go to the resource, and do 'XYZ'.

## Categories

We will split up every resource's keys so you can find them easier.

### Document Intelligence

`(in the sidebar) Resource Management` > `Keys and Endpoint`

- **DOC_INTEL_API_KEY**:  KEY 1 or KEY 2 (pick one)

- **DOC_INTEL_ENDPOINT**: Endpoint (formatted as the name of your Document Intelligence service + `.cognitiveservices.azure.com/`)

### Azure OpenAI

`(in the sidebar) Resource Management` > `Keys and Endpoint`

- **OPENAI_API_KEY**:  KEY 1 or KEY 2 (pick one)

- **OPENAI_ENDPOINT**: Endpoint (formatted as the name of your Azure OpenAI service + `.openai.azure.com/`)

### Storage Account

- **AZURE_STORAGE_ACCOUNT_NAME**: the name of your Storage account resource

`(in the sidebar) Data storage > Containers`

- **AZURE_CONTAINER_NAME**: the name of the container where you want to save the uploaded PDF files
- **AZURE_KNOWLEDGE_BASE_CONTAINER_NAME**: the name of the container where you historical data is stored

`(in the sidebar) Security + networking > Access keys`

- **AZURE_STORAGE_CONNECTION_STRING**: Connection string (starts with 'DefaultEndpointsProtocol...')

### Search service

`(in the sidebar) Overview > (in the main content) Essentials`

- **AZURE_SEARCH_ENDPOINT**: the url formatted as: the name of your Search service resource + `.search.windows.net`

`(in the sidebar) Settings > Keys`

- **AZURE_SEARCH_API_KEY**: Primary/Secondary admin key (pick one)

`(in the sidebar) Search management > Indexes`

- **AZURE_SEARCH_INDEX_NAME**: the name of the search index. If you used the `build_knowledge_base.py` script to create your knowledge base, you can find the name you need in the [`search_index_configuration.json`](../Azure/AI%20Search/search_index_configuration.json) file on the first line.

### Azure Database for MySQL flexible server

- **AZ_db_host**: the url formatted as the name of your Azure Database for MySQL flexible server resource + `.mysql.database.azure.com`
- **AZ_db_user**: chosen by you when you created the resource
- **AZ_db_password**: chosen by you when you created the resource
- **AZ_db_port**: usually it is `3306`

`(in the sidebar) Settings > Databases`

- **AZ_db_name**: the name of the database which contains the tables we need. You can try opening it in Power BI, but

## Template

### .env

<!-- markdownlint-disable MD040  -->
```
# Azure Document Intelligence
DOC_INTEL_ENDPOINT = 
DOC_INTEL_API_KEY = 

# Azure OpenAI
OPENAI_ENDPOINT = 
OPENAI_API_KEY = 

# Azure Blob Storage
AZURE_STORAGE_ACCOUNT_NAME = 
AZURE_CONTAINER_NAME = 
AZURE_KNOWLEDGE_BASE_CONTAINER_NAME = 
AZURE_STORAGE_CONNECTION_STRING = 

# Azure AI Search
AZURE_SEARCH_ENDPOINT = 
AZURE_SEARCH_API_KEY = 
AZURE_SEARCH_INDEX_NAME = 

# Azure Database for MySQL 
AZ_db_host = 
AZ_db_user = 
AZ_db_password = 
AZ_db_port = 
AZ_db_name = 
```

### /app/.streamlit/secrets.toml

```toml
# Azure Document Intelligence
DOC_INTEL_ENDPOINT = ""
DOC_INTEL_API_KEY = ""

# Azure OpenAI
OPENAI_ENDPOINT = ""
OPENAI_API_KEY = ""

# Azure Blob Storage
AZURE_STORAGE_ACCOUNT_NAME = ""
AZURE_CONTAINER_NAME = ""
AZURE_KNOWLEDGE_BASE_CONTAINER_NAME = ""
AZURE_STORAGE_CONNECTION_STRING = ""

# Azure AI Search
AZURE_SEARCH_ENDPOINT = ""
AZURE_SEARCH_API_KEY = ""
AZURE_SEARCH_INDEX_NAME = ""

# Azure Database for MySQL 
AZ_db_host = ""
AZ_db_user = ""
AZ_db_password = ""
AZ_db_port = ""
AZ_db_name = ""
```

## Make sure to add both these files to your `.gitignore` so you don't accidentally push your keys to GitHub, where they will be stolen

```
secrets.toml
.env
```

Verify manually the files are not included before commiting changes. If you do accidentally push your keys to GitHub, you can reset your keys on Azure, often right next to where you found the keys.
