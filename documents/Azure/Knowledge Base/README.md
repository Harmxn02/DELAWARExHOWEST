# How to use your previous estimations to generate new estimations

You can either follow the guide in this [PDF-document](./How%20to%20(re)build%20your%20knowledge%20base%20(search%20index).pdf), or follow the guide in this video: <https://youtu.be/m0qUJbiRds0>

1. Create a storage container, which will contain Excel files with your previous estimations
2. Clone this repository, and run the `build_knowledge_base.py` script
3. Check if your documents were sucessfully added to the knowledge base

## Warning

You will need the following environment variables stored in the `.env` file in the root of your project

```toml

AZURE_STORAGE_CONNECTION_STRING = "placeholder"
# found in resource: Storage account
# path: Security + networking > Access keys > Connection string

AZURE_KNOWLEDGE_BASE_CONTAINER_NAME = "placeholder"
# the name you gave the container inside the storage
# account (we called it `knowledge-base`)

AZURE_SEARCH_ENDPOINT = "placeholder"
# found in the resource: AI Search
# path: Overview > Url
# should end on 'search.windows.net'

AZURE_SEARCH_API_KEY = "placeholder"
# found in resource: AI Search
# path: Settings > Keys > Primary/Secondary admin key (pick one)

AZURE_SEARCH_INDEX_NAME = "placeholder"
# the name you gave the index
# If you used the Python script above, it is `tasks-index-excel`)
# you can find it in the `search_index_configuration.json` file
```
