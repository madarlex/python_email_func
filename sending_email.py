import os
import pandas as pd
import json
from datetime import datetime
from modules import email_util
import sys

from_email_pass = "ggghavpzwkqpxwcv"


def get_customers(customers_path, output_path, error_path, template):
    """
    Get customers infos
    :param customers_path: path to customers.csv
    :param output_path: path to output_emails.json
    :param error_path: path to errors.csv
    :param template: path to email_template.json
    :return: list of customers infos dict
    """

    cus_path = os.path.join(customers_path)
    df = pd.read_csv(cus_path, delimiter=",")
    err_path = os.path.join(error_path)
    no_email_df = df[df["EMAIL"].isna()]
    out_path = os.path.join(output_path)

    # write customers have no emails to csv
    if not no_email_df.empty:
        no_email_df.to_csv(err_path)

    # get list of customers info dict
    used_df = df[~df["EMAIL"].isna()]
    results = []
    for row in used_df.itertuples():
        result = {}
        result["from"] = template["from"]
        result["to"] = row.EMAIL
        result["subject"] = template["subject"]
        result["mimeType"] = template["mimeType"]
        result["body"] = template["body"].format(row.TITLE, row.FIRST_NAME, row.LAST_NAME, datetime.now().date().strftime("%d %b %Y"))
        results.append(result)

    # write sending customers json
    with open(out_path, 'w') as outfile:
        outs = json.dumps(results)
        outfile.write(outs)
    return results


def get_template(template_path):
    """
    get email_template
    :param template_path: email_template.json path
    :return: template
    """

    path = os.path.join(template_path)
    with open(path, 'r') as outfile:
        template = json.load(outfile)
    return template


def sending_email(template_path, customers_path, output_path, error_path):
    """
    Main function sending email
    :param template_path: path to email_template.json
    :param customers_path: path to customers.csv
    :param output_path: path to output_emails.json
    :param error_path: path to errors.csv
    :return:
    """

    template = get_template(template_path)
    email_templates = get_customers(customers_path, output_path, error_path, template)
    for email_template in email_templates:
        email_util.send_email(email_template, from_email_pass)


if __name__ == "__main__":
    sending_email(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])


