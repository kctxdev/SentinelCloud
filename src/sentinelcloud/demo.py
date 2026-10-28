"""Dados de exemplo para o comando `sentinelcloud demo`.

Simula uma conta AWS com varios problemas de seguranca, para mostrar o
relatorio sem precisar de credenciais. Nada aqui acessa a AWS.
"""
from __future__ import annotations

from .core.scanner import ScanResult, Scanner

DEMO_ACCOUNT = "123456789012 (DEMO)"
DEMO_REGION = "us-east-1"

_PAB_OK = {
    "BlockPublicAcls": True,
    "IgnorePublicAcls": True,
    "BlockPublicPolicy": True,
    "RestrictPublicBuckets": True,
}

DEMO_DATA: dict[str, list] = {
    "s3": [
        {"name": "empresa-backups-publico", "public_access_block": None,
         "encryption": None, "logging": False},
        {"name": "empresa-site-estatico",
         "public_access_block": {**_PAB_OK, "BlockPublicPolicy": False},
         "encryption": {"SSEAlgorithm": "AES256"}, "logging": False},
        {"name": "empresa-dados-seguros", "public_access_block": _PAB_OK,
         "encryption": {"SSEAlgorithm": "aws:kms"}, "logging": True},
    ],
    "ec2": [
        {"GroupId": "sg-0a1b2c3d (ssh-aberto)", "IpPermissions": [
            {"IpProtocol": "tcp", "FromPort": 22, "ToPort": 22,
             "IpRanges": [{"CidrIp": "0.0.0.0/0"}], "Ipv6Ranges": []}]},
        {"GroupId": "sg-4e5f6a7b (banco-aberto)", "IpPermissions": [
            {"IpProtocol": "tcp", "FromPort": 3306, "ToPort": 3306,
             "IpRanges": [{"CidrIp": "0.0.0.0/0"}], "Ipv6Ranges": []}]},
        {"GroupId": "sg-8c9d0e1f (tudo-liberado)", "IpPermissions": [
            {"IpProtocol": "-1", "IpRanges": [{"CidrIp": "0.0.0.0/0"}], "Ipv6Ranges": []}]},
        {"GroupId": "sg-2a3b4c5d (web-seguro)", "IpPermissions": [
            {"IpProtocol": "tcp", "FromPort": 443, "ToPort": 443,
             "IpRanges": [{"CidrIp": "0.0.0.0/0"}], "Ipv6Ranges": []}]},
    ],
    "iam": [
        {"name": "AdminTotal", "arn": "arn:aws:iam::123456789012:policy/AdminTotal",
         "document": {"Version": "2012-10-17", "Statement": [
             {"Effect": "Allow", "Action": "*", "Resource": "*"}]}},
        {"name": "S3QualquerCoisa", "arn": "arn:aws:iam::123456789012:policy/S3QualquerCoisa",
         "document": {"Version": "2012-10-17", "Statement": [
             {"Effect": "Allow", "Action": "s3:*", "Resource": "*"}]}},
        {"name": "LeituraRelatorios", "arn": "arn:aws:iam::123456789012:policy/LeituraRelatorios",
         "document": {"Version": "2012-10-17", "Statement": [
             {"Effect": "Allow", "Action": "s3:GetObject",
              "Resource": "arn:aws:s3:::empresa-dados-seguros/*"}]}},
    ],
    "cloudtrail": [
        {"name": "trilha-parada", "is_logging": False, "multi_region": False},
    ],
}


def run_demo() -> ScanResult:
    return Scanner().scan(DEMO_DATA, account_id=DEMO_ACCOUNT, region=DEMO_REGION)
