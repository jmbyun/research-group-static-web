# Research Group Static Website

This is a static website for a research group, hosted as GitHub Pages. 

This website is designed to update its contents every 30 minutes based on [a Google Sheets document](https://docs.google.com/spreadsheets/d/1EDLlUuY2Ia5MKNbCTOftxxSxBaK3C9pRFOIUvMY30eY/edit?usp=sharing) with scheduled GitHub Actions jobs.

## How does this website work?

This project is designed to update its website contents in *[docs](docs)* folder every 30 minutes with scheduled GitHub Actions jobs defined in this [file](.github/workflows/builder.yml). The website contents also get updated when you push something into the website. 

**Do NOT directly modify the contents in *[docs](docs)* folder**, since the contents of that folder gets auto-updated every 30 minutes.

## How to upload static files to this website

If you need to upload image files or any other static files to use in the website to this repository, please put your files in *[assets](assets)* folder. All files in the folder will be copied to *[docs/assets](docs/assets)* when other website contents get updated. 

## How to create your own website from this

1. Fork this repository to your account.

1. Configure the repository to publish a GitHub Pages site from a *docs* folder onh the *master* branch. Read [this document](https://docs.github.com/en/enterprise/2.14/user/articles/configuring-a-publishing-source-for-github-pages#publishing-your-github-pages-site-from-a-docs-folder-on-your-master-branch) if you need help.

1. Configure a custom domain for your website if you need to. Read [this document](https://docs.github.com/en/free-pro-team@latest/github/working-with-github-pages/configuring-a-custom-domain-for-your-github-pages-site) if you need help.

1. Create a new Google Sheets document to store your website contents. Set `DATA_URL` value in the file *[builder/config.py](builder/config.py)*. Follow the instructions below for this.

1. Get a valid Google API key to use when downloading the website contents. Set the key as a encrypted secret `API_KEY`. Follow the instructions below for this.

1. Voilà! You have 

### Create a data source document

This project automatically downloads contents for the website from a Google Sheets document. Set URL of your document as a value for `DATA_URL` in the file *[builder/config.py](builder/config.py)*. 

An example document is available at [here](https://docs.google.com/spreadsheets/d/1EDLlUuY2Ia5MKNbCTOftxxSxBaK3C9pRFOIUvMY30eY/edit?usp=sharing).

To create your own document, follow the instructions below. 

1. Use [this link](https://docs.google.com/spreadsheets/d/1EDLlUuY2Ia5MKNbCTOftxxSxBaK3C9pRFOIUvMY30eY/copy#gid=1676718498) to make a copy of the example Sheets document. 

1. Set your document's sharing settings as: *Public on the web - Anyone on the Internet can find and view*. Read [this document](https://support.google.com/docs/answer/183965?co=GENIE.Platform%3DDesktop&hl=en) if you need help.

1. Copy the URL of your document and paste in the file *[builder/config.py](builder/config.py)* as a value of `DATA_URL`.

### Get a Google API Key

The website builder in this project needs a valid Google API key to download website contents from the Google Sheets document. Add the key to the repository as a *encrypted secret* value `API_KEY`.

1. Get an API key from [Google Developers Console](https://console.developers.google.com/). Read [this answer](https://stackoverflow.com/questions/46583052/http-google-sheets-api-v4-how-to-access-without-oauth-2-0/46583300#46583300) from a question in Stack Overflow to see how to create an API key and enable its use for Google Sheets APIs.

1. Set your API key as a secret value `API_KEY`. Read [this doucment](https://docs.github.com/en/free-pro-team@latest/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository) to see how to add encrypted secrets for a GitHub repository.

## Acknowledgements

This work was supported and funded by [JinYeong Bak](https://github.com/nosyu).