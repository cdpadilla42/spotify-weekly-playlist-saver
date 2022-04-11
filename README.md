# Discover Weekly Playlist Saver

A simple Python script for automatically saving the genereated Discover Weekly Playlist from Spotify.

## Create Integration with Spotify

To use, this application must be authorized with Spotify for Developers. You can create an account and recieve the necessary credentials [here](https://developer.spotify.com/dashboard/login).

You should recieve a client ID, client Secret, and set a redirect URI (a localhost address is fine for this usecase).

## Configuring for AWS with Serverless

the serverless CLI will require an AWS IAM user to deploy.

When creating an account, allow for the following permissions:

- Lambda
- IAM
- S3
- Cloud Formation
- API Gateway
- Event Bridge
- Cloud Watch

Once given the correct credentials, you can link the IAM account with:

```bash
serverless config credentials --provider aws --key AKIA52XT4ILHYF5UR54E --secret xxxxxxxxx
```
