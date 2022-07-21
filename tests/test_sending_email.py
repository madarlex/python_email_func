import os.path
import pathlib
from unittest import mock
import sending_email
import sys

current_path = str(pathlib.Path(__file__).parent.resolve())
template_path = os.path.join(current_path, "email_template.json")
cus_path = os.path.join(current_path, "customers.csv")
out_path = os.path.join(current_path, "output_emails.json")
err_path = os.path.join(current_path, "errors.csv")
sys_argv = [template_path, cus_path, out_path, err_path]


def test_sending_email(mocker):
    with mock.patch("modules.email_util.send_email") as mock_send_email_func:
        spy_get_template = mocker.spy(sending_email, "get_template")
        spy_get_customers = mocker.spy(sending_email, "get_customers")

        sending_email.sending_email(sys_argv[0], sys_argv[1], sys_argv[2], sys_argv[3])

        spy_get_customers.assert_called()
        spy_get_template.assert_called()

        assert os.path.exists(err_path) is True
        assert os.path.exists(out_path) is True

        os.remove(err_path)
        os.remove(out_path)

