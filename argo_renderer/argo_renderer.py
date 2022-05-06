import sys
import argparse
import json
import requests
import katsu_ingest

"""
An ingest script that automates the initial data ingest for katsu service and outputs a file in ARGO format.

You should run the script in an active virtualenv that has `requests` installed. You may also use Katsu's virtualenv for this purpose, if that's more convenient.

Please note that the data_file you supply must be available for Katsu to read. In other words, it should be located on the same server or within the same container as the Katsu instance.
"""

def render_argo(katsu_server_url, argo_file):
    """
    Render an output file in argo format 
    """

    r6 = requests.get(
        katsu_server_url + "/api/mcodepackets?format=argo"
    )

    argo_data = requests.get(
        katsu_server_url + "/api/mcodepackets?format=argo"
    ).json()


    if r6.status_code == 200 or r6.status_code == 201 or r6.status_code == 204:
        print("Data has been rendered in argo format!")

        with open(f"{argo_file}.json", 'w') as json_file:
            json.dump(argo_data, json_file, indent=4)

    elif r6.status_code == 400:
        print(r6.text)
        sys.exit()
    else:
        print(
            "Something else went wrong when rendering data."
        )
        print(
            "Exception messages from Katsu printed below."
        )
        print(r6.text)
        sys.exit()



def main():

    parser = argparse.ArgumentParser(description="A script that facilitates initial data ingestion of Katsu service and coverts the mcodepacket into argo.")

    parser.add_argument("project", help="Project name.")
    parser.add_argument("dataset", help="Dataset name.")
    parser.add_argument("table", help="Table name.")
    parser.add_argument("server_url", help="The URL of Katsu instance.")
    parser.add_argument("data_file", help="The absolute path to the local data file, readable by Katsu.")
    parser.add_argument("argo_output_file", help="The name of the output ARGO file")

    args = parser.parse_args()
    project_title = args.project
    dataset_title = args.dataset
    table_name = args.table
    katsu_server_url = args.server_url
    data_file = args.data_file
    argo_file = args.argo_output_file


    project_uuid = katsu_ingest.create_project(katsu_server_url, project_title)
    dataset_uuid = katsu_ingest.create_dataset(katsu_server_url, project_uuid, dataset_title)
    table_uuid = katsu_ingest.create_table(katsu_server_url, dataset_uuid, table_name, 'mcodepacket')
    katsu_ingest.ingest_data(katsu_server_url, table_uuid, data_file, 'mcodepacket')
    render_argo(katsu_server_url, argo_file)

if __name__ == "__main__":
    main()