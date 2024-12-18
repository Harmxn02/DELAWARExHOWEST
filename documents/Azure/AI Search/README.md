# Creating the `AI Search` resource on Azure

Get started by navigating to the Azure Portal (<https://portal.azure.com>), and log into your account.

## Steps

Search for "AI Search" in the search bar, and click on the "AI Search" option under the 'Services' section.

![1_SearchBar](./images/1_SearchBar.png)

This will bring you to a screen that shows you all AI Search services linked to your account

Press the `+ Create` button to create a new AI Search service

![2_Create](./images/2_Create.png)

This will bring you to a screen where you need to fill in some details about your AI Search service. Here is how you proceed:

- `Subscription`: select the subscription you want to use in the drop-down list
- `Resource group`: select the resource group you want to add the AI Search service to
- `Service name`: choose a name for the AI Search service
- `Location` (**important!!**): choose your region. This is a very important choice, because it affects your estimated cost quite a lot (and also how much storage you get). Choosing the wrong location will be a costly mistake, so make sure to choose the correct one.
- `Pricing tier`: press the blue text saying `Change pricing tier` so you see all available pricing tiers. Pick the one you think fits best. You can start off with the free tier and upgrade later if needed

Press `Next: Scale` to go the next screen where you can play around with the amount of replicas and partitions. Change these according to what your company requires. Proceed by pressing `Next: Networking` and choose either Public or Private. Followed by pressing `Next: Tags`, which you can leave empty

After this press `Next: Review + create` to create the resource, and then the blue `Create` button on the next screen to actually make the resource.

Wait for the deployment to complete.

## After creating the resource

> There is a video explaining the entire process. If this guide is not clear enough, you can follow that instead.

After creating the resource you need to create an index which will contain the knowledge base's data. To do this follow these steps:

1. Navigate to the Azure portal
2. Search for the `Storage accounts` resource, and click on it
3. Create a new storage account called "knowledge-base"
4. Upload the Excel files you would like to use to make estimations with (your historical data)

Now you have a storage account filled with the data we will add to the Search index. All you need to do now, is to run the `build_knowledge_base.py` script, and that's it.

<!-- markdownlint-disable MD029 -->
5. Go to the code repository, and navigate to the path `...../scripts/`
6. Type this in the terminal and press enter: `python build_knowledge_base.py`
7. Verify if there was in fact a Search Index built, and that it has several documents inside it (click on the search-box and press `Enter`)
