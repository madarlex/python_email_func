import os
import pandas as pd
import json
from datetime import datetime
from modules import email_util
import sys
from_email_pass = "ggghavpzwkqpxwcv"


def get_customers(customers_path, output_path, error_path, template):
    cus_path = os.path.join(customers_path)
    df = pd.read_csv(cus_path, delimiter=",")
    err_path = os.path.join(error_path)
    no_email_df = df[df["EMAIL"].isna()]
    out_path = os.path.join(output_path)
    if not no_email_df.empty:
        no_email_df.to_csv(err_path)
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
    with open(out_path, 'w') as outfile:
        outs = json.dumps(results)
        outfile.write(outs)
    return results


def get_template(template_path):
    path = os.path.join(template_path)
    with open(path, 'r') as outfile:
        template = json.load(outfile)
    return template


def sending_email(template_path, customers_path, output_path, error_path):
    template = get_template(template_path)
    email_templates = get_customers(customers_path, output_path, error_path, template)
    for email_template in email_templates:
        email_util.send_email(email_template, from_email_pass)


if __name__ == "__main__":
    sending_email(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])


