"""Permissoes IAM somente leitura exigidas pela ferramenta."""

REQUIRED_ACTIONS = [
    "sts:GetCallerIdentity",
    "s3:ListAllMyBuckets",
    "s3:GetBucketPublicAccessBlock",
    "s3:GetEncryptionConfiguration",
    "s3:GetBucketLogging",
    "ec2:DescribeSecurityGroups",
    "iam:ListPolicies",
    "iam:GetPolicyVersion",
    "cloudtrail:DescribeTrails",
    "cloudtrail:GetTrailStatus",
]


def policy_document() -> dict:
    return {
        "Version": "2012-10-17",
        "Statement": [{"Effect": "Allow", "Action": REQUIRED_ACTIONS, "Resource": "*"}],
    }
