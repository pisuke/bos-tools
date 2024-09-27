# Get UDMI Site Model Metadata

This program facilitates getting metadata files from a source repository containing
a UDMI site model.

# Usage

```
$ ./get_udmi_sitemodel_metadata.py --help

       USAGE: ./get_udmi_sitemodel_metadata.py [flags]
flags:

./get_udmi_sitemodel_metadata.py:
  --destination_path: Destination path for the cloned repository
    (default: './destination_folder')
  --repo_url: URL of the private Git repository
  --site_id: ID of the site

Try --helpfull to get a list of all flags.
```

## Usage example

```
./get_udmi_sitemodel_metadata.py \
  --destination_path ./udmi_sitemodels \
  --repo_url git@github.com:faucetsdn/udmi_site_model.git \
  --site_id COUNTRY-CITY-BUILDINGID 
```