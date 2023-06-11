# CRISP GPT BOT

1. Install Python3.9
```shell
# bash shell
sudo apt-get install python3.9
# optionally, upgrade pip
python3.9 -m pip install --upgrade pip
```

2. Clone the repository:
```shell
git clone https://git01pp.visahq.org/platon/support-bot.git
```

3. Change to the project folder:
```shell
cd support-bot
```

4. Install dependencies:
```shell
python3.9 -m pip install -r requirements.txt
```

5. Prepare your AWS secrets. The lambda function relies on the AWS Secrets Manager to handle things like API keys and credential information. If you're running this function in your own environment, you'll have to provide these pieces of data for it. (If you're running this file using VisaHQ's AWS account, then this account already has the appropriate secrets defined in its AWS Secrets Manager, so you can skip this step.) You'll need to create a `secret.json` file with the following contents. (Fill the appropriate values into this JSON object. This file and these values aren't stored in the repository for what are presumably obvious reasons.)
```secret.json
{
  "PLUGIN_IDENTIFIER": "",
  "CRISP_PLUGIN_KEY": "",
  "WEBSITE_ID": "",
  "GPT_KEY": "",
  "ID_OPERATOR_GPT": ""
}
```
You'll then pass this file to your AWS Secrets Manager as follows. This presumes that you have the AWS CLI installed and you have an active AWS profile.
```shell
aws secretsmanager create-secret --name VisaBotSecret --secret-string file://secret.json
```
FYI, in the future, if you ever need to delete this secret, use the following invocation:
```shell
aws secretsmanager delete-secret --secret-id VisaBotSecret --force-delete-without-recovery
```

6. Run the application:
```shell
python3.9 lambda_function.py
```

The application will run on http://localhost:80/
